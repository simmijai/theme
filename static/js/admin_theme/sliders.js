import { api } from '../utils/api.js';

document.addEventListener('click', async (e) => {
    const btn = e.target.closest('.js-delete-slider');
    if (!btn) return;

    const url = btn.dataset.url;
    const title = btn.dataset.title;

    if (!confirm(`Are you sure you want to delete '${title}'?\n\nThis action cannot be undone.`)) {
        return;
    }

    try {
        await api.post(url);
        window.location.reload();
    } catch (err) {
        alert(err.message || 'Failed to delete slider');
    }
});
