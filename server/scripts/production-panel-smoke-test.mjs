import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import net from 'node:net';
import { fileURLToPath } from 'node:url';

const serverRoot = fileURLToPath(new URL('../', import.meta.url));

async function getAvailablePort() {
  const listener = net.createServer();
  await new Promise((resolve, reject) => {
    listener.once('error', reject);
    listener.listen(0, '127.0.0.1', resolve);
  });
  const { port } = listener.address();
  await new Promise((resolve, reject) => listener.close((error) => error ? reject(error) : resolve()));
  return port;
}

const port = await getAvailablePort();
const server = spawn(process.execPath, ['src/start-production.js'], {
  cwd: serverRoot,
  env: { ...process.env, NODE_ENV: 'production', PORT: String(port) },
  stdio: 'ignore'
});

try {
  let response;
  const deadline = Date.now() + 10_000;
  while (Date.now() < deadline) {
    try {
      response = await fetch(`http://127.0.0.1:${port}/api/orders/demo`);
      break;
    } catch {
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
  }

  assert.ok(response, 'production API should start');
  assert.equal(response.status, 404, 'demo orders endpoint must be disabled in production');
  assert.deepEqual(await response.json(), { error: 'not_found' });
  console.log('ORDERS_PANEL_PRODUCTION_DISABLED_OK');
} finally {
  server.kill();
}
