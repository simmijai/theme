// static/js/utils/api.js
import { getCSRFToken } from './csrf.js';

async function post(url, options = {}) {
    const res = await fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            ...options.headers,
        },
        body: options.body || null,
    });

    if (!res.ok) {
        let message = 'Request failed';
        try {
            const data = await res.json();
            message = data.error || message;
        } catch (_) {}
        throw new Error(message);
    }

    return res;
}

export const api = { post };
