// ── Email validator ───────────────────────────────────────────
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

const CSRF = $('[name=csrfmiddlewaretoken]').val() ||
  document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';

// ── Spinner helpers ──────────────────────────────────────────
function showSpinner(spinnerId, btnId) {
  $('#' + spinnerId).removeClass('d-none');
  $('#' + btnId).prop('disabled', true);
}
function hideSpinner(spinnerId, btnId) {
  $('#' + spinnerId).addClass('d-none');
  $('#' + btnId).prop('disabled', false);
}

// ── Login ────────────────────────────────────────────────────
function handleLogin() {
  const email    = $('#loginEmail').val().trim();
  const password = $('#loginPassword').val();
  const errorBox = $('#loginError');

  errorBox.addClass('d-none').text('');

  if (!email || !password) {
    errorBox.removeClass('d-none').text('Please fill in all fields.');
    return;
  }
    // ── NEW: validate email format ──
  if (!isValidEmail(email)) {
    errorBox.removeClass('d-none').text('Please enter a valid email address.');
    return;
  }

  showSpinner('loginSpinner', 'loginBtn');

  $.ajax({
    url: '/ajax/login/',
    type: 'POST',
    contentType: 'application/json',
    headers: { 'X-CSRFToken': CSRF },
    data: JSON.stringify({ email, password }),
    success(res) {
      if (res.success) {
        window.location.href = res.redirect;
      } else {
        errorBox.removeClass('d-none').text(res.error);
        hideSpinner('loginSpinner', 'loginBtn');
      }
    },
    error() {
      errorBox.removeClass('d-none').text('Something went wrong. Please try again.');
      hideSpinner('loginSpinner', 'loginBtn');
    }
  });
}

// ── Register ─────────────────────────────────────────────────
function handleRegister() {
  const username = $('#regUsername').val().trim();
  const email    = $('#regEmail').val().trim();
  const password = $('#regPassword').val();
  const errorBox   = $('#registerError');
  const successBox = $('#registerSuccess');

  errorBox.addClass('d-none').text('');
  successBox.addClass('d-none').text('');

  if (!username || !email || !password) {
    errorBox.removeClass('d-none').text('All fields are required.');
    return;
  }
  // ── NEW: validate email format ──
  if (!isValidEmail(email)) {
    errorBox.removeClass('d-none').text('Please enter a valid email address.');
    return;
  }

  if (password.length < 6) {
    errorBox.removeClass('d-none').text('Password must be at least 6 characters.');
    return;
  }

  showSpinner('registerSpinner', 'registerBtn');

  $.ajax({
    url: '/ajax/register/',
    type: 'POST',
    contentType: 'application/json',
    headers: { 'X-CSRFToken': CSRF },
    data: JSON.stringify({ username, email, password }),
    success(res) {
      if (res.success) {
        successBox.removeClass('d-none').text('Account created! Redirecting...');
        setTimeout(() => window.location.href = res.redirect, 800);
      } else {
        errorBox.removeClass('d-none').text(res.error);
        hideSpinner('registerSpinner', 'registerBtn');
      }
    },
    error() {
      errorBox.removeClass('d-none').text('Something went wrong. Please try again.');
      hideSpinner('registerSpinner', 'registerBtn');
    }
  });
}

// ── Enter key support ─────────────────────────────────────────
$(document).on('keypress', '#loginPassword', function(e) {
  if (e.which === 13) handleLogin();
});
$(document).on('keypress', '#regPassword', function(e) {
  if (e.which === 13) handleRegister();
});