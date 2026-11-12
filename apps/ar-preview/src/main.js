import './components.js';

const status = document.querySelector('#status');
const bees = [...document.querySelectorAll('.bee')];
const hive = document.querySelector('#hive');
let beesLoaded = 0;
let hiveLoaded = false;
let hasError = false;

function refreshStatus() {
  if (hasError) return;
  if (hiveLoaded && beesLoaded === bees.length) {
    status.textContent = `Escena lista: ${beesLoaded} abejas, mariposas, libélula, colibrí y lagartija.`;
    status.dataset.state = 'ready';
    return;
  }
  status.textContent = `Cargando escena… abejas ${beesLoaded}/${bees.length}${hiveLoaded ? ' · jobón listo' : ''}`;
  status.dataset.state = 'loading';
}

function reportError(message) {
  hasError = true;
  status.textContent = `${message} Revisa la consola y la ruta del GLB.`;
  status.dataset.state = 'error';
}

for (const bee of bees) {
  if (bee.getObject3D('mesh')) beesLoaded += 1;
  bee.addEventListener('model-loaded', (event) => {
    beesLoaded += 1;
    const animations = event.detail.model?.animations?.map((clip) => clip.name) ?? [];
    if (animations.length) console.log(`[${bee.id}] animaciones: ${animations.join(', ')}`);
    refreshStatus();
  });
  bee.addEventListener('model-error', () => reportError(`No se pudo cargar ${bee.id}.`));
}

if (hive.getObject3D('mesh')) hiveLoaded = true;
hive.addEventListener('model-loaded', () => {
  hiveLoaded = true;
  refreshStatus();
});
hive.addEventListener('model-error', () => reportError('No se pudo cargar el jobón.'));

refreshStatus();

window.setTimeout(() => {
  if (!hasError && (beesLoaded < bees.length || !hiveLoaded)) {
    status.textContent = 'La escena sigue cargando. A-Frame y aframe-extras se descargan desde CDN; revisa tu conexión.';
    status.dataset.state = 'waiting';
  }
}, 9000);
