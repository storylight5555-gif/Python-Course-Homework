const menuToggle = document.getElementById('menu-toggle');
const mobileNav = document.getElementById('mobile-nav');
if (menuToggle && mobileNav) {
  menuToggle.addEventListener('click', () => {
    const open = mobileNav.classList.toggle('open');
    menuToggle.setAttribute('aria-expanded', String(open));
    menuToggle.textContent = open ? '×' : '☰';
  });
}

let toastTimer;
function showToast(message) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 2400);
}

document.querySelectorAll('.add-to-cart').forEach((button) => {
  button.closest('form').addEventListener('submit', async (event) => {
    event.preventDefault();
    try {
      const response = await fetch('/cart/add', {
        method: 'POST',
        headers: {'X-Requested-With': 'XMLHttpRequest'}
      });
      const data = await response.json();
      const count = document.getElementById('cart-count');
      if (count) count.textContent = data.count;
      showToast(data.message);
    } catch (error) {
      button.closest('form').submit();
    }
  });
});
