const form = document.getElementById('contact-form');
const status = document.getElementById('form-status');

form.addEventListener('submit', event => {
  event.preventDefault();
  const name = form.name.value.trim();
  const email = form.email.value.trim();
  const message = form.message.value.trim();

  if (!name || !email || !message) {
    status.textContent = 'Please complete all fields before sending.';
    return;
  }

  status.textContent = 'Message ready to send! This demo page does not submit data.';
  form.reset();
});
