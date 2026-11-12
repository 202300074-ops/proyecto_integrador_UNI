export const CATEGORY_LABELS = {
  honey: 'Miel',
  soap: 'Jabón',
  cosmetic: 'Cosmético',
  candle: 'Vela'
};

export const PRODUCT_IMAGES = {
  'miel-de-melipona': '/productos/miel-de-melipona.webp',
  'jabon-sak-po': '/productos/jabon-sak-po.webp',
  'balsamo-xunan': '/productos/balsamo-xunan.webp',
  'vela-jobon': '/productos/vela-jobon.webp'
};

const currency = new Intl.NumberFormat('es-MX', {
  style: 'currency',
  currency: 'MXN',
  maximumFractionDigits: 0
});

function ProductGlyph({ category }) {
  const common = {
    fill: 'none',
    stroke: 'currentColor',
    strokeWidth: 1.5,
    strokeLinecap: 'round',
    strokeLinejoin: 'round'
  };

  if (category === 'soap') {
    return (
      <svg viewBox="0 0 64 64" className="h-20 w-20 text-forest-800/70" aria-hidden="true">
        <rect x="12" y="27" width="40" height="21" rx="8" {...common} />
        <path d="M22 27c0-6 4-10 10-10s10 4 10 10" {...common} />
        <circle cx="24" cy="18" r="2.5" {...common} />
        <circle cx="40" cy="14" r="2" {...common} />
        <circle cx="46" cy="22" r="1.5" {...common} />
      </svg>
    );
  }

  if (category === 'candle') {
    return (
      <svg viewBox="0 0 64 64" className="h-20 w-20 text-forest-800/70" aria-hidden="true">
        <rect x="22" y="26" width="20" height="24" rx="4" {...common} />
        <path d="M32 26V18" {...common} />
        <path d="M32 18c-4-3-4-7 0-10 4 3 4 7 0 10Z" {...common} />
        <path d="M18 50h28" {...common} />
      </svg>
    );
  }

  if (category === 'cosmetic') {
    return (
      <svg viewBox="0 0 64 64" className="h-20 w-20 text-forest-800/70" aria-hidden="true">
        <rect x="24" y="20" width="16" height="30" rx="6" {...common} />
        <path d="M28 20v-6h8v6" {...common} />
        <path d="M28 34h8" {...common} />
      </svg>
    );
  }

  return (
    <svg viewBox="0 0 64 64" className="h-20 w-20 text-forest-800/70" aria-hidden="true">
      <path d="M32 10 50 20.5v21L32 52 14 41.5v-21L32 10Z" {...common} />
      <path d="M32 22c-5 6-7 10-7 14a7 7 0 0 0 14 0c0-4-2-8-7-14Z" {...common} />
    </svg>
  );
}

export default function ProductCard({ product, onSelect }) {
  const prices = product.variants.map((variant) => Number(variant.price));
  const fromPrice = prices.length ? Math.min(...prices) : Number(product.base_price);
  const totalStock = product.variants.reduce(
    (sum, variant) => sum + Number(variant.stock),
    0
  );
  const image = PRODUCT_IMAGES[product.slug];
  const imageFit = product.slug === 'jabon-sak-po' ? 'object-cover' : 'object-contain';

  return (
    <article className="card group flex flex-col overflow-hidden transition duration-300 hover:-translate-y-1 hover:shadow-xl">
      <div className={`relative flex ${image ? 'h-56' : 'h-44'} items-center justify-center overflow-hidden bg-cream`}>
        {image ? (
          <img
            src={image}
            alt={`${product.name} de Sak P'o' Kaab`}
            className={`h-full w-full ${imageFit} transition duration-500 group-hover:scale-[1.03]`}
            loading="lazy"
          />
        ) : (
          <>
            <div className="absolute inset-0 opacity-50 [background-image:radial-gradient(circle_at_20%_20%,rgba(201,130,42,0.35),transparent_45%),radial-gradient(circle_at_80%_70%,rgba(31,59,44,0.18),transparent_40%)]" />
            <div className="relative transition duration-300 group-hover:scale-105">
              <ProductGlyph category={product.category} />
            </div>
          </>
        )}
        {product.has_ar ? (
          <span className="absolute right-4 top-4 rounded-full bg-forest-800 px-3 py-1 text-[10px] font-semibold uppercase tracking-widest text-cream">
            Etiqueta AR
          </span>
        ) : null}
      </div>

      <div className="flex flex-1 flex-col gap-3 p-5">
        <div className="flex items-center justify-between gap-3">
          <span className="eyebrow">{CATEGORY_LABELS[product.category] ?? product.category}</span>
          <span
            className={`text-[11px] font-medium ${
              totalStock > 0 ? 'text-forest-700' : 'text-red-700'
            }`}
          >
            {totalStock > 0 ? `${totalStock} disponibles` : 'Agotado'}
          </span>
        </div>

        <h3 className="font-display text-2xl leading-tight text-forest-900">
          {product.name}
        </h3>
        <p className="line-clamp-3 text-sm leading-relaxed text-charcoal/70">
          {product.description}
        </p>

        <div className="mt-auto flex items-end justify-between gap-3 pt-2">
          <div>
            <p className="text-[11px] uppercase tracking-widest text-charcoal/50">Desde</p>
            <p className="font-display text-xl text-forest-900">
              {currency.format(fromPrice)}
            </p>
          </div>
          <button
            type="button"
            onClick={() => onSelect(product)}
            className="btn-ghost !px-4 !py-2 text-xs"
          >
            Ver variantes
          </button>
        </div>
      </div>
    </article>
  );
}
