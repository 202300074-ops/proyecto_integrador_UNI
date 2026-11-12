import express from 'express';
import cors from 'cors';
import { config } from './env.js';
import { pingDb } from './db.js';
import productsRouter from './routes/products.js';
import commerceRouter from './routes/commerce.js';
import { notFound, errorHandler } from './middleware/error.js';

const app = express();

app.disable('x-powered-by');
app.use(cors({ origin: config.corsOrigin }));
app.use(express.json({ limit: '1mb' }));

app.get('/api/health', async (req, res) => {
  try {
    const dbUp = await pingDb();
    res.json({
      ok: true,
      service: 'sak-po-kaab-api',
      db: dbUp ? 'up' : 'down',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(503).json({
      ok: false,
      service: 'sak-po-kaab-api',
      db: 'down',
      error: 'database_unavailable'
    });
  }
});

app.use('/api/products', productsRouter);
app.use('/api', commerceRouter);

app.use(notFound);
app.use(errorHandler);

app.listen(config.port, () => {
  console.log(`[api] Sak P'o' Kaab en http://localhost:${config.port}`);
});
