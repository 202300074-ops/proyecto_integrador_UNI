import './components.js';

const AFRAME = window.AFRAME;
const status = document.querySelector('#vr-status');

function setStatus(message, state = 'message') {
  if (!status) return;
  status.textContent = message;
  status.dataset.state = state;
}

AFRAME.registerComponent('vr-hotspot', {
  schema: {
    title: { type: 'string', default: '' },
    body: { type: 'string', default: '' }
  },

  init() {
    this.el.addEventListener('click', () => {
      const scene = this.el.sceneEl;
      const panel = scene.querySelector('#info-panel');
      panel.querySelector('#info-title').setAttribute('text', 'value', this.data.title);
      panel.querySelector('#info-body').setAttribute('text', 'value', this.data.body);
      panel.setAttribute('visible', true);
      setStatus(`Punto de interés: ${this.data.title}`);
    });

    this.el.addEventListener('mouseenter', () => this.el.setAttribute('scale', '1.25 1.25 1.25'));
    this.el.addEventListener('mouseleave', () => this.el.setAttribute('scale', '1 1 1'));
  }
});

AFRAME.registerComponent('vr-close-info', {
  init() {
    this.el.addEventListener('click', () => {
      this.el.sceneEl.querySelector('#info-panel').setAttribute('visible', false);
      setStatus('Recorrido listo. Mira otro punto de interés.');
    });
  }
});

const narration = document.querySelector('#vr-tour-audio');
const narrationLabel = document.querySelector('#vr-audio-label');
const narrationButton = document.querySelector('#vr-audio-button');
let narrationOperation = 0;
let narrationStarting = false;

function updateNarrationControls() {
  const playing = narration && !narration.paused && !narration.ended;
  const label = playing ? 'PAUSA' : 'AUDIO';
  if (narrationLabel) narrationLabel.setAttribute('value', label);
  if (narrationButton) narrationButton.textContent = playing ? 'Pausar recorrido' : 'Escuchar recorrido';
}

async function toggleNarration() {
  if (!narration) return;
  if (narration.paused || narration.ended) {
    if (narrationStarting) {
      narrationOperation += 1;
      narrationStarting = false;
      narration.pause();
      setStatus('Narración en pausa.');
      updateNarrationControls();
      return;
    }
    if (narration.ended) narration.currentTime = 0;
    narrationStarting = true;
    const operation = ++narrationOperation;
    setStatus('Iniciando narración…');
    try {
      await narration.play();
      if (operation === narrationOperation && !narration.paused) {
        setStatus('Narración del recorrido en reproducción.');
      }
    } catch {
      if (operation === narrationOperation && narration.paused) {
        setStatus('No se pudo iniciar el audio. Pulsa Escuchar recorrido otra vez.', 'error');
      }
    } finally {
      if (operation === narrationOperation) narrationStarting = false;
    }
  } else {
    narrationOperation += 1;
    narrationStarting = false;
    narration.pause();
    setStatus('Narración en pausa.');
  }
  updateNarrationControls();
}

AFRAME.registerComponent('vr-audio-toggle', {
  init() {
    this.el.addEventListener('click', toggleNarration);
  }
});

if (narrationButton) narrationButton.addEventListener('click', toggleNarration);
if (narration) {
  narration.addEventListener('play', updateNarrationControls);
  narration.addEventListener('pause', updateNarrationControls);
  narration.addEventListener('ended', () => {
    updateNarrationControls();
    narrationStarting = false;
    setStatus('Narración terminada. Puedes volver a escucharla.');
  });
}

AFRAME.registerComponent('vr-teleport', {
  schema: {
    x: { type: 'number', default: 0 },
    z: { type: 'number', default: 0 }
  },

  init() {
    this.rig = this.el.sceneEl.querySelector('#camera-rig');

    this.el.addEventListener('click', () => {
      this.rig.setAttribute('position', { x: this.data.x, y: 0, z: this.data.z });
      setStatus('Te moviste a otra zona del meliponario.');
    });
  }
});

const scene = document.querySelector('#vr-scene');
const hive = document.querySelector('#vr-hive');
const bees = [...document.querySelectorAll('.vr-bee')];

let hiveLoaded = false;
let beesLoaded = 0;
let failed = false;

if (status) status.dataset.state = 'loading';

function updateStatus() {
  if (failed || !status) return;
  if (hiveLoaded && beesLoaded === bees.length) {
    if (status.dataset.state === 'loading') {
      setStatus('Recorrido listo: jobón, abejas y fauna cargados.', 'ready');
    }
    return;
  }
  if (status.dataset.state === 'loading') {
    status.textContent = `Cargando recorrido… abejas ${beesLoaded}/${bees.length}${hiveLoaded ? ' · jobón listo' : ''}`;
  }
}

hive.addEventListener('model-loaded', () => {
  hiveLoaded = true;
  updateStatus();
});
hive.addEventListener('model-error', () => {
  failed = true;
  setStatus('No se pudo cargar el jobón. Revisa la conexión y recarga.', 'error');
});

for (const bee of bees) {
  bee.addEventListener('model-loaded', () => {
    beesLoaded += 1;
    updateStatus();
  });
  bee.addEventListener('model-error', () => {
    failed = true;
    setStatus(`No se pudo cargar ${bee.id}. Revisa la conexión y recarga.`, 'error');
  });
}

scene.addEventListener('loaded', () => {
  updateStatus();
});
