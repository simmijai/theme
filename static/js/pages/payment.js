// Payment method selection
document.querySelectorAll('.payment-option').forEach(option => {
    option.addEventListener('click', function() {
        // Remove selected class from all options
        document.querySelectorAll('.payment-option').forEach(opt => {
            opt.classList.remove('selected');
        });
        
        // Add selected class to clicked option
        this.classList.add('selected');
        
        // Check the radio button
        const radio = this.querySelector('input[type="radio"]');
        radio.checked = true;
        
        // Show/hide additional details
        const method = this.dataset.method;
        document.querySelectorAll('[id$="-details"]').forEach(detail => {
            detail.style.display = 'none';
        });
        
        if (method !== 'COD') {
            const details = document.getElementById(method.toLowerCase() + '-details');
            if (details) details.style.display = 'block';
        }
        
        // Update button text
        const btn = document.getElementById('place-order-btn');
        if (method === 'COD') {
            btn.innerHTML = '<i class="bi bi-truck me-2"></i>Place Order (COD)';
            btn.disabled = false;
            btn.classList.add('btn-success');
            btn.classList.remove('btn-secondary');
        } else {
            btn.innerHTML = '<i class="bi bi-credit-card me-2"></i>Proceed to Pay';
            btn.disabled = true;
            btn.classList.add('btn-secondary');
            btn.classList.remove('btn-success');
        }
    });
});

// Form submission handling
document.getElementById('payment-form').addEventListener('submit', function(e) {
    const selectedMethod = document.querySelector('input[name="payment_method"]:checked').value;
    
    if (selectedMethod !== 'COD') {
        e.preventDefault();
        alert('This payment method will be available soon. Please use Cash on Delivery for now.');
        return false;
    }
    
    // Show loading state
    const btn = document.getElementById('place-order-btn');
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
    btn.disabled = true;
});