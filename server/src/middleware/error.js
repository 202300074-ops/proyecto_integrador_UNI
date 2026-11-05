export function notFound(req, res) {
  res.status(404).json({
    error: 'not_found',
    path: req.originalUrl
  });
}

export function errorHandler(error, req, res, next) {
  console.error('[api:error]', error);
  res.status(500).json({ error: 'internal_error' });
}
