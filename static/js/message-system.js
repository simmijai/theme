/**
 * Enhanced Message System for Belle E-commerce
 * Provides consistent, accessible, and user-friendly notifications
 */

class MessageSystem {
    constructor() {
        this.init();
    }

    init() {
        this.createToastContainer();
        this.setupSweetAlert();
        this.handleAjaxMessages();
    }

    // Create toast container for non-intrusive notifications
    createToastContainer() {
        if (!document.getElementById('toast-container')) {
            const container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container position-fixed top-0 end-0 p-3';
            container.style.zIndex = '9999';
            container.setAttribute('aria-live', 'polite');
            container.setAttribute('aria-atomic', 'true');
            document.body.appendChild(container);
        }
    }

    // Enhanced SweetAlert configuration
    setupSweetAlert() {
        // Default SweetAlert settings
        this.swalDefaults = {
            timer: 3000,
            timerProgressBar: true,
            showConfirmButton: false,
            position: 'top-end',
            toast: true,
            showClass: {
                popup: 'animate__animated animate__fadeInDown'
            },
            hideClass: {
                popup: 'animate__animated animate__fadeOutUp'
            }
        };
    }

    // Show different types of messages
    showMessage(type, message, options = {}) {
        const config = { ...this.swalDefaults, ...options };
        
        // Map message types to SweetAlert icons
        const iconMap = {
            'success': 'success',
            'error': 'error',
            'warning': 'warning',
            'info': 'info',
            'danger': 'error'
        };

        config.icon = iconMap[type] || 'info';
        config.title = message;

        return Swal.fire(config);
    }

    // Show toast notification (non-intrusive)
    showToast(type, message, duration = 5000) {
        const toast = this.createToastElement(type, message);
        const container = document.getElementById('toast-container');
        container.appendChild(toast);

        // Auto-dismiss
        setTimeout(() => {
            this.dismissToast(toast);
        }, duration);

        return toast;
    }

    createToastElement(type, message) {
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${this.getBootstrapClass(type)} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');

        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="${this.getIcon(type)}"></i> ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" 
                        data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;

        // Initialize Bootstrap toast
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();

        return toast;
    }

    dismissToast(toast) {
        const bsToast = bootstrap.Toast.getInstance(toast);
        if (bsToast) {
            bsToast.hide();
        }
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }

    // Show confirmation dialog
    showConfirmation(title, text, confirmText = 'Yes', cancelText = 'No') {
        return Swal.fire({
            title: title,
            text: text,
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: confirmText,
            cancelButtonText: cancelText,
            reverseButtons: true
        });
    }

    // Show loading message
    showLoading(message = 'Processing...') {
        return Swal.fire({
            title: message,
            allowOutsideClick: false,
            allowEscapeKey: false,
            showConfirmButton: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });
    }

    // Handle AJAX responses with consistent messaging
    handleAjaxResponse(response, options = {}) {
        if (response.success) {
            if (options.useToast) {
                this.showToast('success', response.message || 'Operation successful');
            } else {
                this.showMessage('success', response.message || 'Operation successful');
            }
        } else {
            if (options.useToast) {
                this.showToast('error', response.message || 'Operation failed');
            } else {
                this.showMessage('error', response.message || 'Operation failed');
            }
        }
    }

    // Handle AJAX errors
    handleAjaxError(error, customMessage = null) {
        console.error('AJAX Error:', error);
        const message = customMessage || 'An error occurred. Please try again.';
        this.showMessage('error', message);
    }

    // Utility methods
    getBootstrapClass(type) {
        const classMap = {
            'success': 'success',
            'error': 'danger',
            'warning': 'warning',
            'info': 'info',
            'danger': 'danger'
        };
        return classMap[type] || 'info';
    }

    getIcon(type) {
        const iconMap = {
            'success': 'icon anm anm-check',
            'error': 'icon anm anm-times',
            'warning': 'icon anm anm-exclamation-triangle',
            'info': 'icon anm anm-info-circle',
            'danger': 'icon anm anm-times'
        };
        return iconMap[type] || 'icon anm anm-info-circle';
    }

    // Handle AJAX messages from server
    handleAjaxMessages() {
        // Listen for custom events
        document.addEventListener('showMessage', (e) => {
            const { type, message, options } = e.detail;
            this.showMessage(type, message, options);
        });

        document.addEventListener('showToast', (e) => {
            const { type, message, duration } = e.detail;
            this.showToast(type, message, duration);
        });
    }
}

// Initialize message system
const messageSystem = new MessageSystem();

// Make it globally available
window.MessageSystem = messageSystem;

// Helper functions for easy access
window.showMessage = (type, message, options) => messageSystem.showMessage(type, message, options);
window.showToast = (type, message, duration) => messageSystem.showToast(type, message, duration);
window.showConfirmation = (title, text, confirmText, cancelText) => messageSystem.showConfirmation(title, text, confirmText, cancelText);
window.showLoading = (message) => messageSystem.showLoading(message);