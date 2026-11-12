import { useEffect, useMemo, useState } from 'react';
import { getProducts } from './api.js';
import ProductCard, { CATEGORY_LABELS, PRODUCT_IMAGES } from './components/ProductCard.jsx';
import CartPanel from './components/CartPanel.jsx';

const FILTERS = [
  { id: 'all', label: 'Todo' },
  { id: 'honey', label: 'Miel' },
  { id: 'soap', label: 'Jabones' },
  { id: 'cosmetic', label: 'Cosméticos' },
  { id: 'candle', label: 'Velas' }
];

const currency = new Intl.NumberFormat('es-MX', {
  style: 'currency',
  currency: 'MXN',
  maximumFractionDigits: 0
});

function BrandMark({ className = 'h-10 w-10' }) {
  return (
    <svg viewBox="0 0 64 64" className={className} aria-hidden="true">
      <path
        d="M32 6 53 18v24L32 54 11 42V18L32 6Z"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
      />
      <path
        d="M32 20c-6 7-9 12-9 17a9 9 0 0 0 18 0c0-5-3-10-9-17Z"
        fill="currentColor"
        opacity="0.9"
      />
    </svg>
  );
}

function ProductDialog({ product, onClose, onAddToCart, onOpenCart }) {
  const [notice, setNotice] = useState('');
  const image = PRODUCT_IMAGES[product.slug];

  useEffect(() => {
    const onKeyDown = (event) => {
      if (event.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', onKeyDown);
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', onKeyDown);
      document.body.style.overflow = '';
    };
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-end justify-center bg-charcoal/50 p-4 backdrop-blur-sm sm:items-center"
      role="dialog"
      aria-modal="true"
      aria-labelledby="product-dialog-title"
      onClick={onClose}
    >
      <div
        className="card max-h-[90vh] w-full max-w-lg overflow-y-auto p-6"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="eyebrow">{CATEGORY_LABELS[product.category] ?? product.category}</p>
            <h2
              id="product-dialog-title"
              className="mt-2 font-display text-3xl leading-tight text-forest-900"
            >
              {product.name}
            </h2>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="rounded-full border border-charcoal/15 px-3 py-1 text-xs font-semibold text-charcoal/70 transition hover:bg-charcoal/5"
          >
            Cerrar
          </button>
        </div>

        {image ? (
          <img
            src={image}
            alt={`${product.name} de Sak P'o' Kaab`}
            className="mt-4 h-56 w-full rounded-2xl bg-cream object-contain sm:h-64"
          />
        ) : null}

        <p className="mt-4 text-sm leading-relaxed text-charcoal/75">
          {product.description}
        </p>
        {product.story ? (
          <p className="mt-3 rounded-2xl bg-honey-50 p-4 text-sm leading-relaxed text-charcoal/70">
            {product.story}
          </p>
        ) : null}

        <h3 className="mt-6 text-xs font-semibold uppercase tracking-[0.24em] text-charcoal/50">
          Variantes
        </h3>
        <ul className="mt-3 divide-y divide-charcoal/10">
          {product.variants.map((variant) => (
            <li
              key={variant.id}
              className="flex flex-wrap items-center justify-between gap-3 py-3"
            >
              <div>
                <p className="text-sm font-semibold text-forest-900">{variant.name}</p>
                <p className="text-xs text-charcoal/55">
                  {variant.sku} · {variant.stock} en inventario
                </p>
              </div>
              <div className="flex items-center gap-3">
                <p className="font-display text-lg text-forest-900">
                  {currency.format(Number(variant.price))}
                </p>
                <button
                  type="button"
                  data-add-variant={variant.id}
                  disabled={Number(variant.stock) < 1}
                  onClick={() => {
                    const added = onAddToCart(product, variant);
                    setNotice(added ? `${variant.name} agregado al carrito.` : 'No queda inventario disponible de esa variante.');
                  }}
                  className="btn-primary !px-3 !py-2 text-[11px] disabled:cursor-not-allowed disabled:opacity-45"
                >
                  {Number(variant.stock) > 0 ? 'Agregar' : 'Agotado'}
                </button>
              </div>
            </li>
          ))}
        </ul>

        {notice ? <p role="status" className="mt-4 rounded-xl bg-honey-50 p-3 text-xs text-forest-900">{notice}</p> : null}
        <div className="mt-5 flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-honey-300/60 bg-honey-50 p-4">
          <p className="max-w-xs text-xs leading-relaxed text-honey-900">
            El inventario se vuelve a validar en el servidor al registrar el pedido. El pago es simulado.
          </p>
          <button type="button" data-open-cart onClick={onOpenCart} className="btn-ghost !px-4 !py-2 text-xs">
            Ver carrito
          </button>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [products, setProducts] = useState([]);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('all');
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [cart, setCart] = useState([]);
  const [cartOpen, setCartOpen] = useState(false);

  function addToCart(product, variant) {
    const variantId = Number(variant.id);
    const existing = cart.find((item) => item.variantId === variantId);
    if (existing && existing.quantity >= Number(variant.stock)) return false;

    setCart((current) => {
      const currentItem = current.find((item) => item.variantId === variantId);
      if (currentItem) {
        return current.map((item) => item.variantId === variantId
          ? { ...item, quantity: Math.min(item.quantity + 1, Number(variant.stock)) }
          : item);
      }
      return [...current, {
        variantId,
        productId: Number(product.id),
        productName: product.name,
        variantName: variant.name,
        sku: variant.sku,
        price: Number(variant.price),
        stock: Number(variant.stock),
        quantity: 1
      }];
    });
    return true;
  }

  function changeCartQuantity(variantId, quantity) {
    if (quantity < 1) {
      setCart((current) => current.filter((item) => item.variantId !== variantId));
      return;
    }
    setCart((current) => current.map((item) => item.variantId === variantId
      ? { ...item, quantity: Math.min(quantity, item.stock) }
      : item));
  }

  const cartCount = cart.reduce((sum, item) => sum + item.quantity, 0);

  useEffect(() => {
    let active = true;

    getProducts()
      .then((data) => {
        if (!active) return;
        setProducts(data);
        setStatus('ready');
      })
      .catch((requestError) => {
        if (!active) return;
        setError(requestError.message);
        setStatus('error');
      });

    return () => {
      active = false;
    };
  }, []);

  const filteredProducts = useMemo(() => {
    if (filter === 'all') return products;
    return products.filter((product) => product.category === filter);
  }, [products, filter]);

  const variantCount = products.reduce(
    (sum, product) => sum + product.variants.length,
    0
  );
  const arCount = products.filter((product) => product.has_ar).length;

  return (
    <div className="min-h-screen overflow-x-hidden">
      <header className="sticky top-0 z-40 border-b border-charcoal/10 bg-cream/85 backdrop-blur">
        <div className="container-page flex items-center justify-between gap-4 py-4">
          <a href="#inicio" className="flex min-w-0 items-center gap-3">
            <BrandMark className="h-9 w-9 shrink-0 text-forest-800" />
            <span className="truncate font-display text-xl text-forest-900">
              Sak P'o' Kaab
            </span>
          </a>

          <nav className="hidden items-center gap-8 text-sm font-medium text-charcoal/70 md:flex">
            <a className="transition hover:text-forest-900" href="#catálogo">
              Catálogo
            </a>
            <a className="transition hover:text-forest-900" href="#experiencia">
              Experiencia
            </a>
            <a className="transition hover:text-forest-900" href="#historia">
              Historia
            </a>
          </nav>

          <button
            type="button"
            onClick={() => setCartOpen(true)}
            className="btn-primary shrink-0 !px-5 !py-2.5 text-xs"
            aria-label={`Abrir carrito, ${cartCount} artículos`}
          >
            Carrito ({cartCount})
          </button>
        </div>
      </header>

      <main>
        <section id="inicio" className="relative overflow-hidden">
          <div className="container-page grid grid-cols-1 items-center gap-12 py-16 lg:grid-cols-[1.05fr_0.95fr] lg:py-24">
            <div className="min-w-0">
              <p className="eyebrow">Cooperativa melipona · Yucatán</p>
              <h1 className="mt-5 max-w-2xl break-words font-display text-4xl leading-[1.02] text-forest-900 sm:text-5xl lg:text-6xl">
                Miel y jabón de la abeja melipona
              </h1>
              <p className="mt-6 max-w-xl break-words text-base leading-relaxed text-charcoal/70">
                Sak P'o' Kaab reúne la miel de la abeja sin aguijón, el jabón
                artesanal y la memoria del jobón. Un catálogo con historia,
                etiqueta interactiva y meliponario virtual.
              </p>

              <div className="mt-8 flex flex-wrap gap-3">
                <a href="#catálogo" className="btn-primary">
                  Ver el catálogo
                </a>
                <a href="#experiencia" className="btn-ghost">
                  Explorar la experiencia
                </a>
              </div>

              <dl className="mt-10 grid max-w-lg grid-cols-3 gap-4 border-t border-charcoal/10 pt-6">
                <div>
                  <dt className="text-[11px] uppercase tracking-widest text-charcoal/50">
                    Productos
                  </dt>
                  <dd className="font-display text-2xl text-forest-900">
                    {products.length || '—'}
                  </dd>
                </div>
                <div>
                  <dt className="text-[11px] uppercase tracking-widest text-charcoal/50">
                    Variantes
                  </dt>
                  <dd className="font-display text-2xl text-forest-900">
                    {variantCount || '—'}
                  </dd>
                </div>
                <div>
                  <dt className="text-[11px] uppercase tracking-widest text-charcoal/50">
                    Con AR
                  </dt>
                  <dd className="font-display text-2xl text-forest-900">
                    {arCount || '—'}
                  </dd>
                </div>
              </dl>
            </div>

            <div className="relative mx-auto w-full min-w-0 max-w-md">
              <div className="absolute -inset-6 rounded-[3rem] bg-gradient-to-br from-honey-200/70 via-honey-100/40 to-transparent blur-2xl" />
              <div className="card relative overflow-hidden p-6">
                <div className="flex items-center justify-between">
                  <span className="eyebrow">Jobón</span>
                  <span className="rounded-full border border-forest-800/15 px-3 py-1 text-[10px] font-semibold uppercase tracking-widest text-forest-800">
                    Melipona beecheii
                  </span>
                </div>

                <div className="mt-6 grid grid-cols-3 gap-3">
                  {Array.from({ length: 9 }).map((_, index) => (
                    <div
                      key={index}
                      className="aspect-[0.86] rounded-[42%] border border-forest-800/15 bg-gradient-to-br from-honey-100 to-honey-200/70"
                    />
                  ))}
                </div>

                <div className="mt-6 rounded-2xl bg-forest-800 p-4 text-cream">
                  <p className="text-[10px] uppercase tracking-[0.24em] text-cream/60">
                    Etiqueta interactiva
                  </p>
                  <p className="mt-1 text-sm leading-relaxed text-cream/85">
                    Escanea la etiqueta y observa la abeja animada y el proceso de
                    cosecha en realidad aumentada.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section id="catálogo" className="border-y border-charcoal/10 bg-white/40 py-16">
          <div className="container-page">
            <div className="flex flex-col justify-between gap-6 md:flex-row md:items-end">
              <div>
                <p className="eyebrow">Catálogo</p>
                <h2 className="mt-3 font-display text-4xl text-forest-900">
                  Lo que produce la colmena
                </h2>
                <p className="mt-3 max-w-xl text-sm leading-relaxed text-charcoal/65">
                  Precios y existencias leídos desde MySQL. Cada producto tiene
                  variantes con inventario propio.
                </p>
              </div>

              <div className="flex flex-wrap gap-2">
                {FILTERS.map((item) => (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => setFilter(item.id)}
                    className={`rounded-full px-4 py-2 text-xs font-semibold transition ${
                      filter === item.id
                        ? 'bg-forest-800 text-cream'
                        : 'border border-charcoal/15 bg-white/60 text-charcoal/65 hover:border-forest-800/30 hover:text-forest-900'
                    }`}
                  >
                    {item.label}
                  </button>
                ))}
              </div>
            </div>

            {status === 'loading' ? (
              <div className="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
                {Array.from({ length: 4 }).map((_, index) => (
                  <div
                    key={index}
                    className="h-80 animate-pulse rounded-3xl bg-white/60"
                  />
                ))}
              </div>
            ) : null}

            {status === 'error' ? (
              <div className="mt-10 rounded-3xl border border-red-200 bg-red-50 p-6 text-sm text-red-800">
                No se pudo cargar el catálogo: {error}. Verifica que la API y MySQL
                estén corriendo.
              </div>
            ) : null}

            {status === 'ready' ? (
              <div className="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
                {filteredProducts.map((product) => (
                  <ProductCard
                    key={product.id}
                    product={product}
                    onSelect={setSelectedProduct}
                  />
                ))}
              </div>
            ) : null}
          </div>
        </section>

        <section id="experiencia" className="py-16">
          <div className="container-page">
            <div className="max-w-2xl">
              <p className="eyebrow">Experiencia</p>
              <h2 className="mt-3 font-display text-4xl text-forest-900">
                La historia se puede tocar
              </h2>
              <p className="mt-3 text-sm leading-relaxed text-charcoal/65">
                Las experiencias de realidad aumentada y realidad virtual se
                integran al catálogo en los siguientes sprints.
              </p>
            </div>

            <div className="mt-8 grid grid-cols-1 gap-6 md:grid-cols-2">
              <article className="card overflow-hidden p-6">
                <div className="flex items-center justify-between">
                  <h3 className="font-display text-2xl text-forest-900">
                    Etiqueta con AR
                  </h3>
                  <span className="rounded-full bg-honey-100 px-3 py-1 text-[10px] font-semibold uppercase tracking-widest text-honey-800">
                    Sprint 2
                  </span>
                </div>
                <p className="mt-3 text-sm leading-relaxed text-charcoal/65">
                  Al escanear la etiqueta con el navegador aparece la abeja
                  animada y el video del proceso de cosecha.
                </p>
                <div className="mt-6 flex h-32 items-center justify-center rounded-2xl border border-dashed border-forest-800/20 bg-honey-50 text-xs font-medium text-forest-800/60">
                  MindAR + A-Frame 1.6
                </div>
              </article>

              <article className="card overflow-hidden p-6">
                <div className="flex items-center justify-between">
                  <h3 className="font-display text-2xl text-forest-900">
                    Meliponario virtual
                  </h3>
                  <span className="rounded-full bg-honey-100 px-3 py-1 text-[10px] font-semibold uppercase tracking-widest text-honey-800">
                    Sprint 3
                  </span>
                </div>
                <p className="mt-3 text-sm leading-relaxed text-charcoal/65">
                  Un recorrido navegable por el jobón, con hotspots, narración y
                  la abeja melipona en el centro.
                </p>
                <div className="mt-6 flex h-32 items-center justify-center rounded-2xl border border-dashed border-forest-800/20 bg-honey-50 text-xs font-medium text-forest-800/60">
                  A-Frame + WebXR 1.8
                </div>
              </article>
            </div>
          </div>
        </section>

        <section id="historia" className="border-t border-charcoal/10 bg-forest-800 py-16 text-cream">
          <div className="container-page grid grid-cols-1 gap-10 lg:grid-cols-[0.9fr_1.1fr]">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.28em] text-honey-300">
                Sak P'o' Kaab
              </p>
              <h2 className="mt-3 font-display text-4xl leading-tight">
                Jabón de miel, memoria de la colmena
              </h2>
            </div>
            <div className="space-y-4 text-sm leading-relaxed text-cream/75">
              <p>
                <strong className="text-cream">Sak p'o'</strong> significa jabón en
                maya yucateco; <strong className="text-cream">kaab</strong> nombra
                a la abeja y a la miel. La marca une ambos oficios: el cuidado
                cotidiano y el trabajo de la melipona.
              </p>
              <p>
                Este sitio es un proyecto académico de la materia Multimedia y
                Diseño Digital. La cooperativa y la marca son un caso de estudio
                simulado; los datos de mercado se citan desde fuentes reales.
              </p>
              <p className="text-xs text-cream/50">
                Fuentes de la lengua: Arqueología Mexicana, diccionario de
                Bastarrachea (AULEX) y diccionario de la UQROO.
              </p>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t border-charcoal/10 py-8">
        <div className="container-page flex flex-col items-start justify-between gap-4 text-xs text-charcoal/55 sm:flex-row sm:items-center">
          <div className="flex items-center gap-3">
            <BrandMark className="h-7 w-7 text-forest-800" />
            <span>Sak P'o' Kaab · Proyecto integrador 2026</span>
          </div>
          <span>Multimedia y Diseño Digital · Ingeniería en Software</span>
        </div>
      </footer>

      {selectedProduct ? (
        <ProductDialog
          product={selectedProduct}
          onClose={() => setSelectedProduct(null)}
          onAddToCart={addToCart}
          onOpenCart={() => {
            setSelectedProduct(null);
            setCartOpen(true);
          }}
        />
      ) : null}
      {cartOpen ? (
        <CartPanel
          items={cart}
          onChangeQuantity={changeCartQuantity}
          onRemove={(variantId) => setCart((current) => current.filter((item) => item.variantId !== variantId))}
          onClose={() => setCartOpen(false)}
          onOrderCreated={() => setCart([])}
        />
      ) : null}
    </div>
  );
}
