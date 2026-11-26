import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { createServer } from 'vite';

const server = await createServer({
  configFile: fileURLToPath(new URL('../vite.config.js', import.meta.url)),
  logLevel: 'error',
  server: { host: '127.0.0.1', port: 0, strictPort: false }
});

try {
  await server.listen();
  const address = server.httpServer.address();
  const origin = `http://127.0.0.1:${address.port}`;

  const page = await fetch(origin);
  assert.equal(page.status, 200, 'visor HTML debe responder 200');
  const html = await page.text();
  assert.match(html, /Abejas y jobón/, 'visor debe presentar ambos modelos');
  assert.match(html, /bee-wander/, 'visor debe incluir el movimiento de las abejas');
  assert.match(html, /grass-clump/, 'visor debe incluir vegetación');
  assert.match(html, /butterfly-a/, 'visor debe incluir mariposas');
  assert.match(html, /dragonfly/, 'visor debe incluir una libélula');
  assert.match(html, /hummingbird/, 'visor debe incluir un colibrí');
  assert.match(html, /lizard/, 'visor debe incluir una lagartija');
  assert.match(html, /href="\/vr\.html"/, 'visor debe enlazar el recorrido VR');

  const vrPage = await fetch(`${origin}/vr.html`);
  assert.equal(vrPage.status, 200, 'página VR debe responder 200');
  const vrHtml = await vrPage.text();
  assert.match(vrHtml, /releases\/1\.8\.0\/aframe\.min\.js/, 'página VR debe usar A-Frame 1.8');
  assert.match(vrHtml, /vr-mode-ui="enabled: true"/, 'página VR debe habilitar entrada a VR');
  assert.match(vrHtml, /cursor="fuse: true; fuseTimeout: 900"/, 'página VR debe incluir interacción por mirada');
  assert.match(vrHtml, /vr-hotspot=/, 'página VR debe incluir hotspots informativos');
  assert.match(vrHtml, /vr-teleport=/, 'página VR debe incluir navegación por zonas');
  assert.match(vrHtml, /vr-butterfly-a/, 'página VR debe incluir fauna adicional');
  assert.match(vrHtml, /vr-lizard/, 'página VR debe incluir una lagartija');
  assert.match(vrHtml, /vr-audio-toggle/, 'página VR debe incluir control de narración');
  assert.match(vrHtml, /narracion-recorrido-vr\.mp3/, 'página VR debe cargar narración');
  assert.match(vrHtml, /id="vr-farm-ground"/, 'página VR debe tener terreno que rodea al visitante');
  assert.match(vrHtml, /id="vr-pond"/, 'página VR debe incluir el lago');
  assert.match(vrHtml, /id="vr-fish-a"/, 'página VR debe incluir peces visibles en el lago');
  assert.match(vrHtml, /id="vr-easter-egg"/, 'página VR debe incluir un detalle escondido');
  assert.match(vrHtml, /vr-explore=/, 'cámara debe permitir explorar con colisiones');
  assert.match(vrHtml, /id="vr-touch-pad"/, 'página VR debe ofrecer joystick táctil');
  assert.match(vrHtml, /id="vr-touch-knob"/, 'joystick táctil debe tener perilla visible');
  assert.ok((vrHtml.match(/class="vr-tree"/g) ?? []).length >= 8, 'escena debe distribuir árboles alrededor del visitante');
  assert.ok((vrHtml.match(/class="vr-ambient-bee"/g) ?? []).length >= 4, 'escena debe añadir abejas ambientales ligeras');
  assert.equal((vrHtml.match(/vr-hotspot=/g) ?? []).length, 5, 'página VR debe incluir cuatro hotspots y el huevo escondido');
  assert.equal((vrHtml.match(/vr-teleport=/g) ?? []).length, 5, 'página VR debe incluir cinco zonas de teletransporte');

  const vrAudio = await fetch(`${origin}/audio/narracion-recorrido-vr.mp3`);
  assert.equal(vrAudio.status, 200, 'audio narrado VR debe responder 200');
  assert.match(vrAudio.headers.get('content-type') ?? '', /audio\/mpeg/);
  const vrAudioBytes = new Uint8Array(await vrAudio.arrayBuffer());
  assert.ok(vrAudioBytes.length > 100000, 'audio VR debe contener la narración completa');

  for (const name of ['abeja.glb', 'jobon.glb']) {
    const response = await fetch(`${origin}/models/${name}`);
    assert.equal(response.status, 200, `${name} debe responder 200`);
    assert.match(response.headers.get('content-type') ?? '', /model\/gltf-binary/);
    const bytes = new Uint8Array(await response.arrayBuffer());
    assert.equal(new TextDecoder().decode(bytes.slice(0, 4)), 'glTF', `${name} debe tener firma GLB`);
    assert.ok(bytes.length > 1000, `${name} debe contener datos de modelo`);
  }

  const arPage = await fetch(`${origin}/ar.html`);
  assert.equal(arPage.status, 200, 'página AR debe responder 200');
  const arHtml = await arPage.text();
  assert.match(arHtml, /mindar-image/, 'página AR debe incluir MindAR');
  assert.match(arHtml, /etiqueta-sakpokaab\.mind/, 'página AR debe apuntar al target compilado');
  assert.match(arHtml, /ar-bee-a/, 'página AR debe incluir abejas animadas');
  assert.match(arHtml, /video-button/, 'página AR debe ofrecer el video de cosecha');
  assert.match(arHtml, /cosecha-melipona-recreacion-mobile\.mp4/, 'página AR debe usar el MP4 móvil');

  const mind = await fetch(`${origin}/targets/etiqueta-sakpokaab.mind`);
  assert.equal(mind.status, 200, 'target .mind debe responder 200');
  assert.match(mind.headers.get('content-type') ?? '', /application\/octet-stream/);
  const mindBytes = new Uint8Array(await mind.arrayBuffer());
  assert.ok(mindBytes.length > 100000, 'target .mind debe contener datos de seguimiento');

  const targetImage = await fetch(`${origin}/targets/etiqueta-sakpokaab.png`);
  assert.equal(targetImage.status, 200, 'imagen de etiqueta debe responder 200');
  assert.match(targetImage.headers.get('content-type') ?? '', /image\/png/);
  const targetBytes = new Uint8Array(await targetImage.arrayBuffer());
  assert.equal(
    [...targetBytes.slice(0, 8)].map((value) => value.toString(16).padStart(2, '0')).join(''),
    '89504e470d0a1a0a',
    'etiqueta debe ser un PNG válido'
  );

  for (const name of ['cosecha-melipona-recreacion.mp4', 'cosecha-melipona-recreacion-mobile.mp4']) {
    const videoRange = await fetch(`${origin}/video/${name}`, {
      headers: { Range: 'bytes=0-31' }
    });
    assert.equal(videoRange.status, 206, `${name} debe soportar solicitudes por rango`);
    assert.match(videoRange.headers.get('content-range') ?? '', /^bytes 0-31\//);
    const videoHeader = new Uint8Array(await videoRange.arrayBuffer());
    assert.equal(new TextDecoder().decode(videoHeader.slice(4, 8)), 'ftyp', `${name} debe tener cabecera MP4`);

    const video = await fetch(`${origin}/video/${name}`);
    assert.equal(video.status, 200, `${name} debe responder 200`);
    assert.match(video.headers.get('content-type') ?? '', /video\/mp4/);
    const videoBytes = new Uint8Array(await video.arrayBuffer());
    assert.equal(new TextDecoder().decode(videoBytes.slice(4, 8)), 'ftyp', `${name} debe tener contenedor MP4`);
    assert.ok(videoBytes.length > 500000, `${name} debe contener audio y animación`);
  }

  const poster = await fetch(`${origin}/video/cosecha-poster.png`);
  assert.equal(poster.status, 200, 'poster del video debe responder 200');
  assert.match(poster.headers.get('content-type') ?? '', /image\/png/);

  console.log('AR_PREVIEW_SMOKE_OK: visor, VR con hotspots/fauna/audio, MindAR, etiqueta y videos.');
} finally {
  await server.close();
}
