console.log("categories.js loadeddddddddddddddd");

import { api } from '../utils/api.js';

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.delete-subcategory-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const url = btn.dataset.url;
            const name = btn.dataset.name;

            if (!confirm(`Delete "${name}"? This cannot be undone.`)) return;

            btn.disabled = true;
            try {
                await api.post(url);  // data-url se call
                const row = btn.closest('tr');
                row.remove();
            } catch (err) {
                alert(err.message);
            } finally {
                btn.disabled = false;
            }
        });
    });
});
