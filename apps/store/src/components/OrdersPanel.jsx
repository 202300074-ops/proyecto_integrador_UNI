import { useEffect, useRef, useState } from 'react';
import { getDemoOrders } from '../api.js';

const currency = new Intl.NumberFormat('es-MX', {
  style: 'currency',
  currency: 'MXN',
  maximumFractionDigits: 0
});

const STATUS_LABELS = {
  pending: 'Pendiente',
  paid: 'Pagado',
  preparing: 'En preparación',
  shipped: 'Enviado',
  delivered: 'Entregado',
  cancelled: 'Cancelado'
};

function formatDate(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return 'Fecha no disponible';
  return new Intl.DateTimeFormat('es-MX', {
    dateStyle: 'medium',
    timeStyle: 'short'
  }).format(date);
}

export default function OrdersPanel({ onClose }) {
  const [orders, setOrders] = useState([]);
  const [status, setStatus] = useState('loading');
  const closeButtonRef = useRef(null);
  const previousFocusRef = useRef(null);

  useEffect(() => {
    previousFocusRef.current = document.activeElement;
    closeButtonRef.current?.focus();

    const onKeyDown = (event) => {
      if (event.key === 'Escape') onClose();
      if (event.key === 'Tab') {
        event.preventDefault();
        closeButtonRef.current?.focus();
      }
    };
    document.addEventListener('keydown', onKeyDown);
    document.body.style.overflow = 'hidden';

    let active = true;
    getDemoOrders()
      .then((data) => {
        if (!active) return;
        setOrders(data);
        setStatus('ready');
      })
      .catch(() => {
        if (!active) return;
        setStatus('error');
      });

    return () => {
      active = false;
      document.removeEventListener('keydown', onKeyDown);
      document.body.style.overflow = '';
      previousFocusRef.current?.focus?.();
    };
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-end justify-center bg-charcoal/55 p-3 backdrop-blur-sm sm:items-center sm:p-6"
      onClick={onClose}
    >
      <section
        role="dialog"
        aria-modal="true"
        aria-labelledby="orders-panel-title"
        className="card max-h-[90vh] w-full max-w-2xl overflow-y-auto p-5 sm:p-7"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="eyebrow">Solo demostración local</p>
            <h2 id="orders-panel-title" className="mt-2 font-display text-3xl text-forest-900">
              Pedidos simulados
            </h2>
            <p className="mt-2 max-w-lg text-sm leading-relaxed text-charcoal/65">
              Vista de solo lectura. No muestra datos de contacto ni permite cambiar estados.
            </p>
          </div>
          <button
            ref={closeButtonRef}
            type="button"
            onClick={onClose}
            className="btn-ghost shrink-0 !px-4 !py-2 text-xs"
          >
            Cerrar
          </button>
        </div>

        {status === 'loading' ? (
          <p className="mt-7 rounded-2xl bg-honey-50 p-4 text-sm text-charcoal/70" role="status">
            Cargando pedidos de demostración…
          </p>
        ) : null}

        {status === 'error' ? (
          <p className="mt-7 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-800" role="alert">
            No se pudo cargar el panel. Verifica que la API y MySQL estén activos.
          </p>
        ) : null}

        {status === 'ready' && orders.length === 0 ? (
          <p className="mt-7 rounded-2xl bg-honey-50 p-4 text-sm text-charcoal/70">
            Todavía no hay pedidos simulados.
          </p>
        ) : null}

        {status === 'ready' && orders.length > 0 ? (
          <ul className="mt-6 divide-y divide-charcoal/10" aria-label="Pedidos de demostración">
            {orders.map((order) => (
              <li key={order.orderNumber} className="grid grid-cols-[1fr_auto] gap-x-4 gap-y-2 py-4 sm:grid-cols-[1fr_auto_auto] sm:items-center">
                <div>
                  <p className="text-sm font-semibold text-forest-900">Pedido {order.orderNumber}</p>
                  <p className="mt-1 text-xs text-charcoal/55">
                    {formatDate(order.createdAt)} · {order.itemCount} {order.itemCount === 1 ? 'artículo' : 'artículos'}
                  </p>
                </div>
                <span className="justify-self-start rounded-full bg-honey-100 px-3 py-1 text-[10px] font-semibold uppercase tracking-widest text-honey-900 sm:justify-self-center">
                  {STATUS_LABELS[order.status] ?? 'Estado registrado'}
                </span>
                <p className="col-start-2 row-start-1 text-right font-display text-lg text-forest-900 sm:col-start-auto sm:row-start-auto">
                  {currency.format(order.total)}
                </p>
              </li>
            ))}
          </ul>
        ) : null}

        <p className="mt-5 border-t border-charcoal/10 pt-4 text-xs leading-relaxed text-charcoal/50">
          El panel solo se habilita en desarrollo. Los pedidos usan pago simulado y no representan ventas reales.
        </p>
      </section>
    </div>
  );
}
