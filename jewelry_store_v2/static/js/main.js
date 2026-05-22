// Auto-dismiss flash messages
document.addEventListener('DOMContentLoaded', function () {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(function (flash) {
        setTimeout(function () {
            flash.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(20px)';
            setTimeout(() => flash.remove(), 500);
        }, 4000);
    });
});
