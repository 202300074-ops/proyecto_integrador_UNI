import { createReadStream, readFileSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vite';

const appRoot = path.dirname(fileURLToPath(import.meta.url));
const modelRoot = path.resolve(appRoot, '../../assets/models');
const targetRoot = path.resolve(appRoot, '../../assets/targets');
const videoRoot = path.resolve(appRoot, '../../assets/video');
const audioRoot = path.resolve(appRoot, '../../assets/audio');

const staticFiles = new Map([
  ['/models/abeja.glb', { filePath: path.join(modelRoot, 'abeja.glb'), contentType: 'model/gltf-binary' }],
  ['/models/jobon.glb', { filePath: path.join(modelRoot, 'jobon.glb'), contentType: 'model/gltf-binary' }],
  ['/targets/etiqueta-sakpokaab.mind', {
    filePath: path.join(targetRoot, 'etiqueta-sakpokaab.mind'),
    contentType: 'application/octet-stream'
  }],
  ['/targets/etiqueta-sakpokaab.png', {
    filePath: path.join(targetRoot, 'etiqueta-sakpokaab.png'),
    contentType: 'image/png'
  }],
  ['/video/cosecha-melipona-recreacion.mp4', {
    filePath: path.join(videoRoot, 'cosecha-melipona-recreacion.mp4'),
    contentType: 'video/mp4'
  }],
  ['/video/cosecha-melipona-recreacion-mobile.mp4', {
    filePath: path.join(videoRoot, 'cosecha-melipona-recreacion-mobile.mp4'),
    contentType: 'video/mp4'
  }],
  ['/video/cosecha-poster.png', {
    filePath: path.join(videoRoot, 'cosecha-poster.png'),
    contentType: 'image/png'
  }],
  ['/audio/narracion-recorrido-vr.mp3', {
    filePath: path.join(audioRoot, 'narracion-recorrido-vr.mp3'),
    contentType: 'audio/mpeg'
  }]
]);

function projectAssets() {
  return {
    name: 'sak-po-kaab-project-assets',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const pathname = new URL(req.url ?? '/', 'http://localhost').pathname;
        const entry = staticFiles.get(pathname);
        if (!entry) return next();

        let size;
        try {
          size = statSync(entry.filePath).size;
        } catch (error) {
          return next(error);
        }

        res.setHeader('Content-Type', entry.contentType);
        res.setHeader('Cache-Control', 'no-cache');

        if (entry.contentType === 'video/mp4') {
          res.setHeader('Accept-Ranges', 'bytes');
          const range = req.headers.range;
          if (range) {
            const match = /^bytes=(\d+)-(\d*)$/.exec(range);
            if (!match) {
              res.statusCode = 416;
              res.setHeader('Content-Range', `bytes */${size}`);
              return res.end();
            }
            const start = Number(match[1]);
            const requestedEnd = match[2] ? Number(match[2]) : size - 1;
            if (start >= size || requestedEnd < start) {
              res.statusCode = 416;
              res.setHeader('Content-Range', `bytes */${size}`);
              return res.end();
            }
            const end = Math.min(requestedEnd, size - 1);
            res.statusCode = 206;
            res.setHeader('Content-Range', `bytes ${start}-${end}/${size}`);
            res.setHeader('Content-Length', end - start + 1);
            if (req.method === 'HEAD') return res.end();
            return createReadStream(entry.filePath, { start, end }).on('error', next).pipe(res);
          }
        }

        res.statusCode = 200;
        res.setHeader('Content-Length', size);
        if (req.method === 'HEAD') return res.end();

        createReadStream(entry.filePath).on('error', next).pipe(res);
      });
    },
    generateBundle() {
      for (const [urlPath, entry] of staticFiles) {
        this.emitFile({
          type: 'asset',
          fileName: urlPath.slice(1),
          source: readFileSync(entry.filePath)
        });
      }
    }
  };
}

export default defineConfig({
  root: appRoot,
  server: {
    allowedHosts: ['.trycloudflare.com']
  },
  plugins: [projectAssets()],
  build: {
    outDir: path.join(appRoot, 'dist'),
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: path.join(appRoot, 'index.html'),
        ar: path.join(appRoot, 'ar.html'),
        vr: path.join(appRoot, 'vr.html')
      }
    }
  }
});
