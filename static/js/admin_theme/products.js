export function deleteProduct(productId, productName) {
    if (confirm(`Are you sure you want to delete '${productName}'?\n\nThis action cannot be undone.`)) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/admin_panel/products/delete/${productId}/`;

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken;

        form.appendChild(csrfInput);
        document.body.appendChild(form);
        form.submit();
    }
}
