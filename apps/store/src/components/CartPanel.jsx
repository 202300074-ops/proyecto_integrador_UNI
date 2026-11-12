import { useEffect, useMemo, useState } from 'react';
import { createOrder, validateCoupon } from '../api.js';

const currency = new Intl.NumberFormat('es-MX', {
  style: 'currency',
  currency: 'MXN',
  maximumFractionDigits: 2
});

const EMPTY_FORM = {
  customerName: '',
  email: '',
  phone: '',
  shippingAddress: '',
  city: '',
  state: '',
  postalCode: ''
};

const ERROR_MESSAGES = {
  coupon_unavailable: 'El cupón no está disponible.',
  coupon_not_started: 'El cupón todavía no está vigente.',
  coupon_expired: 'El cupón ya venció.',
  coupon_limit_reached: 'El cupón alcanzó su límite de usos.',
  coupon_minimum_not_met: 'El subtotal no alcanza el mínimo de $200 para este cupón.',
  variant_unavailable: 'Una variante del carrito ya no está disponible.',
  insufficient_stock: 'No hay suficiente inventario para completar el pedido.',
  invalid_request: 'Revisa los datos del formulario e inténtalo de nuevo.'
};

function errorMessage(code) {
  return ERROR_MESSAGES[code] ?? 'No se pudo completar la solicitud. Inténtalo de nuevo.';
}

function Field({ label, name, value, onChange, ...props }) {
  return (
    <label className="block text-xs font-semibold text-forest-900">
      {label}
      <input
        name={name}
        value={value}
        onChange={onChange}
        className="mt-1.5 w-full rounded-xl border border-charcoal/15 bg-white px-3 py-2.5 text-sm font-normal text-charcoal outline-none transition focus:border-forest-700 focus:ring-2 focus:ring-forest-700/10"
        {...props}
      />
    </label>
  );
}

export default function CartPanel({ items, onChangeQuantity, onRemove, onClose, onOrderCreated }) {
  const [couponInput, setCouponInput] = useState('');
  const [coupon, setCoupon] = useState(null);
  const [couponStatus, setCouponStatus] = useState('idle');
  const [couponError, setCouponError] = useState('');
  const [form, setForm] = useState(EMPTY_FORM);
  const [submitting, setSubmitting] = useState(false);
  const [orderError, setOrderError] = useState('');
  const [orderResult, setOrderResult] = useState(null);

  const subtotal = useMemo(
    () => Math.round(items.reduce((sum, item) => sum + item.price * item.quantity, 0) * 100) / 100,
    [items]
  );
  const discount = coupon ? Number(coupon.discount) : 0;
  const total = Math.max(0, subtotal - discount);

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

  useEffect(() => {
    if (!coupon?.code || items.length === 0) return undefined;
    let active = true;
    validateCoupon(coupon.code, subtotal)
      .then(({ data }) => {
        if (active) {
          setCoupon(data);
          setCouponError('');
          setCouponStatus('ready');
        }
      })
      .catch((error) => {
        if (active) {
          setCoupon(null);
          setCouponStatus('error');
          setCouponError(errorMessage(error.message));
        }
      });
    return () => {
      active = false;
    };
  }, [coupon?.code, items.length, subtotal]);

  function handleFormChange(event) {
    setForm((current) => ({ ...current, [event.target.name]: event.target.value }));
  }

  async function handleApplyCoupon(event) {
    event.preventDefault();
    if (!couponInput.trim() || subtotal <= 0) return;
    setCouponStatus('loading');
    setCouponError('');
    try {
      const { data } = await validateCoupon(couponInput.trim(), subtotal);
      setCoupon(data);
      setCouponInput(data.code);
      setCouponStatus('ready');
    } catch (error) {
      setCoupon(null);
      setCouponStatus('error');
      setCouponError(errorMessage(error.message));
    }
  }

  async function handleSubmitOrder(event) {
    event.preventDefault();
    if (!items.length || submitting) return;
    setSubmitting(true);
    setOrderError('');
    try {
      const { data } = await createOrder({
        ...form,
        couponCode: coupon?.code ?? null,
        items: items.map((item) => ({ variantId: item.variantId, quantity: item.quantity }))
      });
      setOrderResult(data);
      setCoupon(null);
      onOrderCreated();
    } catch (error) {
      setOrderError(errorMessage(error.message));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div
      className="fixed inset-0 z-[60] flex justify-end bg-charcoal/50 backdrop-blur-sm"
      role="dialog"
      aria-modal="true"
      aria-labelledby="cart-title"
      onClick={onClose}
    >
      <section
        className="flex h-full w-full max-w-xl flex-col overflow-hidden bg-cream shadow-2xl"
        onClick={(event) => event.stopPropagation()}
      >
        <header className="flex items-center justify-between border-b border-charcoal/10 px-5 py-4 sm:px-7">
          <div>
            <p className="eyebrow">Compra simulada</p>
            <h2 id="cart-title" className="font-display text-2xl text-forest-900">
              {orderResult ? 'Pedido confirmado' : 'Tu carrito'}
            </h2>
          </div>
          <button type="button" onClick={onClose} className="btn-ghost !px-4 !py-2 text-xs">
            Cerrar
          </button>
        </header>

        {orderResult ? (
          <div className="flex-1 overflow-y-auto p-6 sm:p-8">
            <div className="rounded-3xl border border-forest-700/15 bg-white/75 p-6">
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-forest-700">
                Pedido registrado
              </p>
              <h3 className="mt-3 break-all font-display text-xl text-forest-900 sm:text-3xl">
                {orderResult.orderNumber}
              </h3>
              <p className="mt-3 text-sm leading-relaxed text-charcoal/70">
                El pedido quedó pendiente como demostración académica. No se realizó ningún cobro.
              </p>
              <dl className="mt-6 space-y-2 border-t border-charcoal/10 pt-4 text-sm">
                <div className="flex justify-between"><dt>Subtotal</dt><dd>{currency.format(orderResult.subtotal)}</dd></div>
                <div className="flex justify-between"><dt>Descuento</dt><dd>−{currency.format(orderResult.discount)}</dd></div>
                <div className="flex justify-between font-semibold text-forest-900"><dt>Total simulado</dt><dd>{currency.format(orderResult.total)}</dd></div>
              </dl>
            </div>
            <button type="button" onClick={onClose} className="btn-primary mt-6 w-full justify-center">
              Volver a la tienda
            </button>
          </div>
        ) : (
          <div className="flex-1 overflow-y-auto p-5 sm:p-7">
            {items.length === 0 ? (
              <div className="rounded-3xl border border-dashed border-charcoal/20 bg-white/50 p-8 text-center">
                <p className="font-display text-2xl text-forest-900">Tu carrito está vacío</p>
                <p className="mt-2 text-sm text-charcoal/65">Elige una variante del catálogo para comenzar.</p>
                <button type="button" onClick={onClose} className="btn-primary mt-5">
                  Seguir explorando
                </button>
              </div>
            ) : (
              <>
                <ul className="divide-y divide-charcoal/10 rounded-2xl border border-charcoal/10 bg-white/65 px-4">
                  {items.map((item) => (
                    <li key={item.variantId} className="flex gap-3 py-4">
                      <div className="min-w-0 flex-1">
                        <p className="font-semibold text-forest-900">{item.productName}</p>
                        <p className="mt-0.5 text-xs text-charcoal/60">{item.variantName} · {item.sku}</p>
                        <p className="mt-1 text-sm">{currency.format(item.price)} c/u</p>
                      </div>
                      <div className="flex flex-col items-end justify-between gap-2">
                        <p className="font-semibold text-forest-900">{currency.format(item.price * item.quantity)}</p>
                        <div className="flex items-center gap-2">
                          <button
                            type="button"
                            aria-label={`Quitar una unidad de ${item.productName}`}
                            onClick={() => onChangeQuantity(item.variantId, item.quantity - 1)}
                            className="grid h-8 w-8 place-items-center rounded-full border border-charcoal/15 text-lg"
                          >−</button>
                          <span className="min-w-5 text-center text-sm">{item.quantity}</span>
                          <button
                            type="button"
                            aria-label={`Agregar una unidad de ${item.productName}`}
                            disabled={item.quantity >= item.stock}
                            onClick={() => onChangeQuantity(item.variantId, item.quantity + 1)}
                            className="grid h-8 w-8 place-items-center rounded-full border border-charcoal/15 text-lg disabled:opacity-35"
                          >+</button>
                          <button
                            type="button"
                            onClick={() => onRemove(item.variantId)}
                            className="ml-1 text-xs font-semibold text-red-700 underline underline-offset-2"
                          >Quitar</button>
                        </div>
                        <p className="text-[10px] text-charcoal/50">Inventario: {item.stock}</p>
                      </div>
                    </li>
                  ))}
                </ul>

                <form onSubmit={handleApplyCoupon} className="mt-5 rounded-2xl border border-charcoal/10 bg-white/65 p-4">
                  <label htmlFor="coupon-code" className="text-xs font-semibold text-forest-900">Cupón de descuento</label>
                  <div className="mt-2 flex gap-2">
                    <input
                      id="coupon-code"
                      value={couponInput}
                      onChange={(event) => {
                        const value = event.target.value.toUpperCase();
                        setCouponInput(value);
                        if (coupon && value.trim() !== coupon.code) {
                          setCoupon(null);
                          setCouponError('');
                          setCouponStatus('idle');
                        }
                      }}
                      placeholder="BIENVENIDA10"
                      autoComplete="off"
                      className="min-w-0 flex-1 rounded-xl border border-charcoal/15 bg-white px-3 py-2 text-sm outline-none focus:border-forest-700"
                    />
                    <button type="submit" disabled={couponStatus === 'loading'} className="btn-ghost !px-4 !py-2 text-xs disabled:opacity-50">
                      {couponStatus === 'loading' ? 'Revisando…' : coupon ? 'Actualizar' : 'Aplicar'}
                    </button>
                  </div>
                  {couponError ? <p role="alert" className="mt-2 text-xs text-red-700">{couponError}</p> : null}
                  {coupon ? <p className="mt-2 text-xs font-medium text-forest-700">{coupon.code} aplicado: −{currency.format(discount)}</p> : null}
                </form>

                <div className="mt-5 space-y-2 rounded-2xl bg-forest-900 p-4 text-sm text-cream">
                  <div className="flex justify-between"><span>Subtotal</span><span>{currency.format(subtotal)}</span></div>
                  <div className="flex justify-between text-cream/70"><span>Descuento</span><span>−{currency.format(discount)}</span></div>
                  <div className="flex justify-between border-t border-cream/15 pt-2 text-xs text-cream/65"><span>Envío (simulado)</span><span>Gratis</span></div>
                  <div className="flex justify-between border-t border-cream/15 pt-3 font-semibold"><span>Total</span><span>{currency.format(total)}</span></div>
                </div>

                <form onSubmit={handleSubmitOrder} className="mt-7">
                  <div className="mb-4">
                    <p className="eyebrow">Datos de entrega</p>
                    <h3 className="mt-1 font-display text-2xl text-forest-900">Finalizar pedido</h3>
                  </div>
                  <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                    <Field label="Nombre completo" name="customerName" value={form.customerName} onChange={handleFormChange} autoComplete="name" required />
                    <Field label="Correo electrónico" name="email" type="email" value={form.email} onChange={handleFormChange} autoComplete="email" required />
                    <Field label="Teléfono (opcional)" name="phone" type="tel" value={form.phone} onChange={handleFormChange} autoComplete="tel" />
                    <Field label="Código postal" name="postalCode" value={form.postalCode} onChange={handleFormChange} autoComplete="postal-code" required />
                    <div className="sm:col-span-2"><Field label="Calle y número" name="shippingAddress" value={form.shippingAddress} onChange={handleFormChange} autoComplete="street-address" required /></div>
                    <Field label="Ciudad" name="city" value={form.city} onChange={handleFormChange} autoComplete="address-level2" required />
                    <Field label="Estado" name="state" value={form.state} onChange={handleFormChange} autoComplete="address-level1" required />
                  </div>
                  {orderError ? <p role="alert" className="mt-3 rounded-xl bg-red-50 p-3 text-xs text-red-800">{orderError}</p> : null}
                  <p className="mt-4 text-[11px] leading-relaxed text-charcoal/55">
                    Ejercicio académico: se guarda el pedido con estado pendiente y pago simulado. No se cobra ni se envía el producto.
                  </p>
                  <button type="submit" disabled={submitting || !items.length} className="btn-primary mt-4 w-full justify-center disabled:cursor-wait disabled:opacity-60">
                    {submitting ? 'Registrando pedido…' : `Crear pedido · ${currency.format(total)}`}
                  </button>
                </form>
              </>
            )}
          </div>
        )}
      </section>
    </div>
  );
}
