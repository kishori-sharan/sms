function toggleUserDropdown() {
    var dropdown = document.querySelector('.user-dropdown');
    dropdown.classList.toggle('active');
}
window.onclick = function(event) {
    if (!event.target.closest('.user-dropdown')) {
        var dropdown = document.querySelector('.user-dropdown');
        if (dropdown) dropdown.classList.remove('active');
    }
}