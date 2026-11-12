import './components.js';

const scene = document.querySelector('#ar-scene');
const target = document.querySelector('#ar-target');
const status = document.querySelector('#ar-status');
const hint = document.querySelector('#ar-hint');
const retry = document.querySelector('#ar-retry');
const targetPanel = document.querySelector('#target-panel');
const targetButton = document.querySelector('#target-button');
const targetClose = document.querySelector('#target-close');
const videoButton = document.querySelector('#video-button');
const videoPanel = document.querySelector('#video-panel');
const videoClose = document.querySelector('#video-close');
const harvestVideo = document.querySelector('#harvest-video');
const videoPlayHint = document.querySelector('#video-play-hint');
let arReady = false;
let videoReady = false;
let videoLoadPromise = null;
let videoObjectUrl = null;
let hasVideoHistoryEntry = false;

function setStatus(message, state) {
  status.textContent = message;
  status.dataset.state = state;
}

function showError(message) {
  setStatus(message, 'error');
  retry.hidden = false;
  closeVideoPanel();
  videoButton.disabled = true;
  document.body.classList.remove('target-visible');
}

function openTargetPanel() {
  targetPanel.hidden = false;
}

function closeTargetPanel() {
  targetPanel.hidden = true;
}

function closeVideoPanel() {
  if (!videoPanel || !harvestVideo) return;
  const wasOpen = !videoPanel.hidden;
  if (!wasOpen) return;

  harvestVideo.pause();
  videoPanel.hidden = true;
  videoPlayHint.hidden = true;
  videoButton.disabled = !window.__AR_DEBUG__?.targetFound || !videoReady;
  if (arReady) scene.systems['mindar-image-system']?.unpause();

  if (!hasVideoHistoryEntry) return;
  hasVideoHistoryEntry = false;
  window.history.back();
}

async function prepareHarvestVideo() {
  if (videoReady) return;
  if (!videoLoadPromise) {
    videoLoadPromise = (async () => {
      const response = await fetch(harvestVideo.dataset.src);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const blob = await response.blob();
      videoObjectUrl = URL.createObjectURL(blob);

      await new Promise((resolve, reject) => {
        const onCanPlay = () => {
          cleanup();
          videoReady = true;
          resolve();
        };
        const onError = () => {
          cleanup();
          if (videoObjectUrl) URL.revokeObjectURL(videoObjectUrl);
          videoObjectUrl = null;
          reject(new Error('El navegador no pudo decodificar el MP4.'));
        };
        const cleanup = () => {
          harvestVideo.removeEventListener('canplay', onCanPlay);
          harvestVideo.removeEventListener('error', onError);
        };

        harvestVideo.addEventListener('canplay', onCanPlay, { once: true });
        harvestVideo.addEventListener('error', onError, { once: true });
        harvestVideo.src = videoObjectUrl;
        harvestVideo.load();
        if (harvestVideo.readyState >= HTMLMediaElement.HAVE_FUTURE_DATA) onCanPlay();
      });
    })().catch((error) => {
      videoLoadPromise = null;
      throw error;
    });
  }
  return videoLoadPromise;
}

function openVideoPanel() {
  if (videoButton.disabled || !videoReady) return;
  closeTargetPanel();
  scene.systems['mindar-image-system']?.pause();
  videoPanel.hidden = false;
  videoPlayHint.hidden = true;
  harvestVideo.currentTime = 0;
  if (!hasVideoHistoryEntry) {
    window.history.pushState({ sakPokaabVideo: true }, '', `${window.location.pathname}${window.location.search}#cosecha`);
    hasVideoHistoryEntry = true;
  }

  // Llega como gesto directo del usuario; el archivo ya está descargado y listo.
  harvestVideo.play().catch((error) => {
    videoPlayHint.hidden = false;
    console.warn('[AR] El video quedó listo para reproducirse con los controles.', error);
  });
}

targetButton.addEventListener('click', openTargetPanel);
targetClose.addEventListener('click', closeTargetPanel);
targetPanel.addEventListener('click', (event) => {
  if (event.target === targetPanel) closeTargetPanel();
});
videoButton.addEventListener('click', openVideoPanel);
videoClose.addEventListener('click', closeVideoPanel);
videoPanel.addEventListener('click', (event) => {
  if (event.target === videoPanel) closeVideoPanel();
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    closeTargetPanel();
    closeVideoPanel();
  }
});
window.addEventListener('popstate', () => {
  // El botón Atrás del teléfono cierra el reproductor sin salir de la experiencia AR.
  if (!videoPanel.hidden) {
    hasVideoHistoryEntry = false;
    closeVideoPanel();
  }
});
retry.addEventListener('click', () => window.location.reload());

window.addEventListener('pagehide', () => {
  if (videoObjectUrl) URL.revokeObjectURL(videoObjectUrl);
});

if (!navigator.mediaDevices?.getUserMedia) {
  showError('Este navegador no expone la cámara. Abre la experiencia con HTTPS o en localhost.');
} else {
  setStatus('Iniciando cámara…', 'loading');
}

scene.addEventListener('arReady', () => {
  arReady = true;
  retry.hidden = true;
  setStatus('Cámara lista. Apunta al centro de la etiqueta.', 'ready');
  hint.textContent = 'Mantén la etiqueta completa dentro de la pantalla y evita reflejos.';
});

scene.addEventListener('arError', (event) => {
  arReady = false;
  const detail = event.detail?.error?.message ?? event.detail?.message ?? 'Error desconocido';
  console.error('[AR] arError', event.detail);
  showError(`No se pudo iniciar la cámara: ${detail}. Revisa permisos y usa HTTPS o localhost.`);
});

const bees = [...document.querySelectorAll('.ar-bee')];
window.__AR_DEBUG__ = { scene, target, status, bees, targetFound: false, foundCount: 0, lostCount: 0 };
let trackingSettleTimer;

target.addEventListener('targetFound', () => {
  retry.hidden = true;
  videoButton.disabled = true;
  window.__AR_DEBUG__.targetFound = true;
  window.__AR_DEBUG__.foundCount += 1;
  document.body.classList.add('target-visible');
  document.body.classList.remove('ar-tracking-settled');
  window.clearTimeout(trackingSettleTimer);

  if (videoReady) {
    videoButton.disabled = false;
    setStatus('Etiqueta y video listos.', 'tracking');
    hint.textContent = 'Toca Ver cosecha; seguirá reproduciéndose aunque muevas el teléfono.';
    trackingSettleTimer = window.setTimeout(() => {
      if (window.__AR_DEBUG__.targetFound) document.body.classList.add('ar-tracking-settled');
    }, 2400);
    return;
  }

  setStatus('Etiqueta detectada · preparando el video…', 'loading');
  hint.textContent = 'Descargando el video una vez para reproducirlo sin cortes.';
  prepareHarvestVideo().then(() => {
    if (!window.__AR_DEBUG__.targetFound) return;
    videoButton.disabled = false;
    setStatus('Etiqueta y video listos.', 'tracking');
    hint.textContent = 'Toca Ver cosecha; seguirá reproduciéndose aunque muevas el teléfono.';
    trackingSettleTimer = window.setTimeout(() => {
      if (window.__AR_DEBUG__.targetFound) document.body.classList.add('ar-tracking-settled');
    }, 2400);
  }).catch((error) => {
    console.error('[AR] No se pudo preparar el video.', error);
    if (window.__AR_DEBUG__.targetFound) {
      setStatus('No se pudo cargar el video. Revisa la conexión.', 'error');
      hint.textContent = 'Vuelve a apuntar a la etiqueta para reintentar la descarga.';
    }
  });
});

target.addEventListener('targetLost', () => {
  window.__AR_DEBUG__.targetFound = false;
  window.__AR_DEBUG__.lostCount += 1;
  // Una vez abierto, el video debe terminar aunque el tracking pierda el target
  // mientras la cámara está tapada por el reproductor o el usuario mueve el teléfono.
  videoButton.disabled = videoPanel.hidden;
  window.clearTimeout(trackingSettleTimer);
  document.body.classList.remove('target-visible');
  document.body.classList.remove('ar-tracking-settled');
  setStatus('Sigue apuntando al centro de la etiqueta.', 'searching');
  hint.textContent = 'La etiqueta debe estar completa, plana y con buena iluminación.';
});

for (const bee of bees) {
  bee.addEventListener('model-error', () => {
    showError(`No se pudo cargar la abeja ${bee.id}. Revisa /models/abeja.glb.`);
  });
}

document.querySelector('#ar-hive')?.addEventListener('model-error', () => {
  showError('No se pudo cargar el jobón. Revisa /models/jobon.glb.');
});

harvestVideo.addEventListener('error', () => {
  setStatus('No se pudo cargar el video de cosecha.', 'error');
  videoButton.disabled = true;
  videoReady = false;
  videoLoadPromise = null;
});

window.setTimeout(() => {
  if (status.dataset.state === 'loading') {
    setStatus('La cámara sigue iniciando. Revisa los permisos del navegador.', 'waiting');
    retry.hidden = false;
  }
}, 12000);
