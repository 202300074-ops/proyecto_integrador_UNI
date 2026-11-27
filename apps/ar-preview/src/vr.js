import './components.js';
import { canOccupy, FARM_NAVIGATION, normalizeInput, resolvePosition } from './vr-navigation.js';

const AFRAME = window.AFRAME;
const status = document.querySelector('#vr-status');

function setStatus(message, state = 'message') {
  if (!status) return;
  status.textContent = message;
  status.dataset.state = state;
}

function setInfoPanelVisible(visible) {
  const panel = document.querySelector('#vr-scene #info-panel');
  if (panel) panel.setAttribute('visible', visible);
  const closeButton = document.querySelector('#vr-info-close');
  if (closeButton) closeButton.hidden = !visible;
}

function closeInfoPanel(message = 'Recorrido listo. Mira otro punto de interés.') {
  setInfoPanelVisible(false);
  setStatus(message);
}

AFRAME.registerComponent('vr-explore', {
  schema: {
    speed: { type: 'number', default: 2.8 }
  },

  init() {
    this.camera = this.el.sceneEl.querySelector('#vr-camera');
    this.keys = new Set();
    this.headPosition = new AFRAME.THREE.Vector3();
    this.lastSafeHead = new AFRAME.THREE.Vector3();
    this.wasBlocked = false;

    this.onKeyDown = (event) => {
      if (event.target?.closest?.('button, a, input, textarea, select, [contenteditable="true"]')) return;
      if (!['KeyW', 'KeyA', 'KeyS', 'KeyD', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(event.code)) return;
      event.preventDefault();
      this.keys.add(event.code);
    };
    this.onKeyUp = (event) => this.keys.delete(event.code);
    window.addEventListener('keydown', this.onKeyDown);
    window.addEventListener('keyup', this.onKeyUp);

    this.touch = { forward: 0, strafe: 0 };
    this.activePointer = null;
    this.bindTouch();

    this.camera?.object3D.getWorldPosition(this.lastSafeHead);
  },

  bindTouch() {
    this.touchPad = document.querySelector('#vr-touch-pad');
    this.touchKnob = document.querySelector('#vr-touch-knob');
    if (!this.touchPad || !this.touchKnob) return;
    if (!window.matchMedia('(pointer: coarse)').matches) return;

    const updateFromPointer = (event) => {
      const rect = this.touchPad.getBoundingClientRect();
      const radius = rect.width / 2;
      let dx = (event.clientX - (rect.left + radius)) / radius;
      let dy = (event.clientY - (rect.top + radius)) / radius;
      const length = Math.hypot(dx, dy);
      if (length > 1) {
        dx /= length;
        dy /= length;
      }
      this.touch.strafe = dx;
      this.touch.forward = -dy;
      this.touchKnob.style.transform = `translate(${dx * radius * 0.55}px, ${dy * radius * 0.55}px)`;
    };

    const resetTouch = () => {
      this.touch.forward = 0;
      this.touch.strafe = 0;
      this.activePointer = null;
      this.touchKnob.style.transform = '';
    };

    this.onTouchDown = (event) => {
      this.activePointer = event.pointerId;
      this.touchPad.setPointerCapture?.(event.pointerId);
      updateFromPointer(event);
      event.preventDefault();
    };
    this.onTouchMove = (event) => {
      if (event.pointerId !== this.activePointer) return;
      updateFromPointer(event);
      event.preventDefault();
    };
    this.onTouchUp = () => resetTouch();

    this.touchPad.addEventListener('pointerdown', this.onTouchDown);
    this.touchPad.addEventListener('pointermove', this.onTouchMove);
    this.touchPad.addEventListener('pointerup', this.onTouchUp);
    this.touchPad.addEventListener('pointercancel', this.onTouchUp);
    this.touchPad.addEventListener('lostpointercapture', this.onTouchUp);
  },

  tick(_time, delta) {
    if (!this.camera) this.camera = this.el.sceneEl?.querySelector('#vr-camera');
    if (!this.camera) return;

    const input = normalizeInput(
      Number(this.keys.has('KeyW') || this.keys.has('ArrowUp'))
        - Number(this.keys.has('KeyS') || this.keys.has('ArrowDown'))
        + this.touch.forward,
      Number(this.keys.has('KeyD') || this.keys.has('ArrowRight'))
        - Number(this.keys.has('KeyA') || this.keys.has('ArrowLeft'))
        + this.touch.strafe
    );

    if (input.magnitude > 0) {
      const yaw = this.camera.object3D.rotation.y;
      const step = this.data.speed * Math.min(delta / 1000, 0.05);
      const position = this.el.object3D.position;
      const candidate = {
        x: position.x + (-Math.sin(yaw) * input.forward + Math.cos(yaw) * input.strafe) * step,
        z: position.z + (-Math.cos(yaw) * input.forward - Math.sin(yaw) * input.strafe) * step
      };
      const next = resolvePosition(position, candidate, FARM_NAVIGATION);
      position.x = next.x;
      position.z = next.z;
    }


    this.el.object3D.updateMatrixWorld(true);
    this.camera.object3D.getWorldPosition(this.headPosition);
    if (canOccupy(this.headPosition.x, this.headPosition.z, FARM_NAVIGATION)) {
      this.lastSafeHead.copy(this.headPosition);
      this.wasBlocked = false;
      return;
    }

    const rigPosition = this.el.object3D.position;
    rigPosition.x += this.lastSafeHead.x - this.headPosition.x;
    rigPosition.z += this.lastSafeHead.z - this.headPosition.z;
    this.el.object3D.updateMatrixWorld(true);
    this.camera.object3D.getWorldPosition(this.lastSafeHead);
    if (!this.wasBlocked) setStatus('Hay un obstáculo cerca. Rodea el árbol o el lago.', 'message');
    this.wasBlocked = true;
  },

  teleportTo(x, z) {
    const current = this.el.object3D.position;
    const next = resolvePosition(current, { x, z }, FARM_NAVIGATION);
    if (next.x !== x || next.z !== z) return false;

    current.set(x, 0, z);
    this.el.object3D.updateMatrixWorld(true);
    this.camera?.object3D.getWorldPosition(this.lastSafeHead);
    this.wasBlocked = false;
    return true;
  },

  remove() {
    window.removeEventListener('keydown', this.onKeyDown);
    window.removeEventListener('keyup', this.onKeyUp);
    if (this.touchPad) {
      this.touchPad.removeEventListener('pointerdown', this.onTouchDown);
      this.touchPad.removeEventListener('pointermove', this.onTouchMove);
      this.touchPad.removeEventListener('pointerup', this.onTouchUp);
      this.touchPad.removeEventListener('pointercancel', this.onTouchUp);
      this.touchPad.removeEventListener('lostpointercapture', this.onTouchUp);
    }
  }
});

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
      setInfoPanelVisible(true);
      setStatus(`Punto de interés: ${this.data.title}`);
    });

    this.el.addEventListener('mouseenter', () => this.el.setAttribute('scale', '1.25 1.25 1.25'));
    this.el.addEventListener('mouseleave', () => this.el.setAttribute('scale', '1 1 1'));
  }
});

AFRAME.registerComponent('vr-close-info', {
  init() {
    this.el.addEventListener('click', () => closeInfoPanel());
  }
});

const infoCloseButton = document.querySelector('#vr-info-close');
if (infoCloseButton) {
  infoCloseButton.addEventListener('click', () => closeInfoPanel());
}

window.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closeInfoPanel();
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
    z: { type: 'number', default: 0 },
    zone: { type: 'string', default: 'otra zona' }
  },

  init() {
    this.rig = this.el.sceneEl.querySelector('#camera-rig');

    this.el.addEventListener('click', () => {
      const navigator = this.rig.components['vr-explore'];
      const moved = navigator
        ? navigator.teleportTo(this.data.x, this.data.z)
        : (this.rig.setAttribute('position', { x: this.data.x, y: 0, z: this.data.z }), true);
      if (moved) {
        closeInfoPanel(`Explorando: ${this.data.zone}.`);
      } else {
        setInfoPanelVisible(false);
        setStatus('Ese punto está ocupado. Elige otra zona.');
      }
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
