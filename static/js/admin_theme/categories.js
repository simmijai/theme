console.log("categories.js loaded");
import { api } from '../utils/api.js';

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.delete-category-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            if (!confirm(`Delete "${btn.dataset.name}"?`)) return;

            btn.disabled = true;

            try {
                await api.post(btn.dataset.url);
                location.reload();
            } catch (err) {
                alert(err.message);
                btn.disabled = false;
            }
        });
    });
});

