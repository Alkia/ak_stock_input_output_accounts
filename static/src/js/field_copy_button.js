/** @odoo-module **/

(function() {
    'use strict';

    // Simple copy function
    window.copyWhtValue = function(value, button) {
        if (!value) {
            alert('No value to copy');
            return;
        }

        // Copy to clipboard
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(value).then(() => {
                // Change button text temporarily
                const originalHTML = button.innerHTML;
                button.innerHTML = '<i class="oi oi-check text-success"></i> Copied!';
                button.classList.add('btn-success');
                button.classList.remove('btn-outline-primary');
                
                setTimeout(() => {
                    button.innerHTML = originalHTML;
                    button.classList.remove('btn-success');
                    button.classList.add('btn-outline-primary');
                }, 2000);
            }).catch(() => {
                fallbackCopy(value, button);
            });
        } else {
            fallbackCopy(value, button);
        }
    };

    function fallbackCopy(value, button) {
        const textArea = document.createElement('textarea');
        textArea.value = value;
        textArea.style.position = 'fixed';
        textArea.style.left = '-9999px';
        document.body.appendChild(textArea);
        textArea.select();
        
        try {
            document.execCommand('copy');
            const originalHTML = button.innerHTML;
            button.innerHTML = '<i class="oi oi-check text-success"></i> Copied!';
            button.classList.add('btn-success');
            button.classList.remove('btn-outline-primary');
            
            setTimeout(() => {
                button.innerHTML = originalHTML;
                button.classList.remove('btn-success');
                button.classList.add('btn-outline-primary');
            }, 2000);
        } catch (err) {
            alert('Failed to copy: ' + value);
        }
        
        document.body.removeChild(textArea);
    }
})();
