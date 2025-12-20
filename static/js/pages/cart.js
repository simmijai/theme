import { api } from '../utils/api.js';
import { getCSRFToken } from '../utils/csrf.js';

document.addEventListener('click', async (e) => {
    const removeBtn = e.target.closest('.cart__remove');
    if (!removeBtn) return;

    e.preventDefault();

    const productId = removeBtn.dataset.id;
    const row = removeBtn.closest('tr');

    const config = document.getElementById('cart-config');
    const url = buildUrl(config.dataset.removeUrl, productId);

    try {
        const res = await api.post(url);
        const data = await res.json();
        row.remove();
        updateTotals(data);
    } catch (err) {
        console.error(err.message);
    }
});

/* ======================= */

document.addEventListener('click', async (e) => {
    const qtyBtn = e.target.closest('.cart-qty-btn');
    if (!qtyBtn) return;

    const productId = qtyBtn.dataset.id;
    const input = document.querySelector(`input[data-id="${productId}"]`);

    let qty = parseInt(input.value) || 0;
    qty = qtyBtn.classList.contains('plus') ? qty + 1 : Math.max(0, qty - 1);
    input.value = qty;

    await updateQuantity(productId, qty, input);
});

/* ======================= */

document.addEventListener('change', async (e) => {
    if (!e.target.classList.contains('cart-qty-input')) return;

    const productId = e.target.dataset.id;
    let qty = Math.max(0, parseInt(e.target.value) || 0);
    e.target.value = qty;

    await updateQuantity(productId, qty, e.target);
});

/* ======================= */

async function updateQuantity(productId, qty, input) {
    const config = document.getElementById('cart-config');
    const url = buildUrl(config.dataset.updateUrl, productId);

    const formData = new FormData();
    formData.append('quantity', qty);

    try {
        const res = await fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
            },
            body: formData,
        });

        const data = await res.json();

        if (qty === 0 || data.removed) {
            input.closest('tr')?.remove();
        }

        if (data.item_total !== undefined) {
            const itemTotalElement = document.getElementById(`item-total-${productId}`);
            if (itemTotalElement) {
                itemTotalElement.textContent = `$${data.item_total}`;
            }
        }

        updateTotals(data);
    } catch (err) {
        console.error(err.message);
    }
}

/* ======================= */

function updateTotals(data) {
    if (data.cart_total !== undefined) {
        document.getElementById('cart-subtotal').textContent = `$${data.cart_total}`;
        document.getElementById('cart-grand-total').textContent = `$${data.cart_total}`;
    }
}

function buildUrl(template, id) {
    return template.replace(/0\/$/, `${id}/`);
}