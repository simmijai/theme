document.addEventListener('click', async (e) => {
    const btn = e.target.closest('.remove-from-wishlist');
    if (!btn) return;

    e.preventDefault();
    const row = btn.closest('tr');
    const url = btn.dataset.url;

    try {
        const csrftoken = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest',
            },
            credentials: 'same-origin',
        });

        const data = await response.json();

        if (data.success) {
            if (row) row.remove();
        } else {
            console.error('Failed to remove wishlist item:', data.message);
        }
    } catch (err) {
        console.error('Error removing wishlist item:', err);
    }
});
