/* =============================================
   TATTOO STUDIO - MAIN JAVASCRIPT
   ============================================= */

'use strict';

document.addEventListener('DOMContentLoaded', function () {

  /* --- Navbar Scroll Effect --- */
  const navbar = document.getElementById('main-navbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });
  }

  /* --- Mobile Navbar Toggle --- */
  const toggler = document.getElementById('navbar-toggler');
  const navLinks = document.getElementById('navbar-links');
  if (toggler && navLinks) {
    toggler.addEventListener('click', function () {
      const isOpen = navLinks.classList.toggle('open');
      toggler.setAttribute('aria-expanded', isOpen);
    });

    // Close on link click
    navLinks.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        navLinks.classList.remove('open');
        toggler.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* --- Dropdown Toggle --- */
  window.toggleDropdown = function (e) {
    e.preventDefault();
    const menu = document.getElementById('user-dropdown');
    if (menu) {
      menu.classList.toggle('open');
    }
  };

  // Close dropdown on outside click
  document.addEventListener('click', function (e) {
    const dropdown = document.getElementById('user-dropdown');
    const trigger = e.target.closest('.dropdown-trigger');
    if (dropdown && !trigger && !dropdown.contains(e.target)) {
      dropdown.classList.remove('open');
    }
  });

  /* --- Flash Messages Auto Dismiss --- */
  const toasts = document.querySelectorAll('#flash-container .toast');
  toasts.forEach(function (toast) {
    setTimeout(function () {
      if (toast.parentNode) {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(function () {
          if (toast.parentNode) toast.remove();
        }, 300);
      }
    }, 5000);
  });

  /* --- Modal Functions --- */
  window.openModal = function (modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
  };

  window.closeModal = function (modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.remove('active');
      document.body.style.overflow = '';
    }
  };

  // Close modal on overlay click
  document.querySelectorAll('.modal-overlay').forEach(function (overlay) {
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) {
        overlay.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  });

  // Close modal on escape key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-overlay.active').forEach(function (m) {
        m.classList.remove('active');
      });
      document.body.style.overflow = '';
    }
  });

  /* --- Smooth Scroll for Anchor Links --- */
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const href = anchor.getAttribute('href');
      if (href && href !== '#') {
        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    });
  });

  /* --- Image Upload Preview --- */
  document.querySelectorAll('.upload-zone input[type="file"]').forEach(function (input) {
    input.addEventListener('change', function (e) {
      const preview = input.closest('.upload-zone').querySelector('.upload-preview');
      if (preview) {
        preview.innerHTML = '';
        Array.from(e.target.files).forEach(function (file) {
          const reader = new FileReader();
          reader.onload = function (ev) {
            const img = document.createElement('img');
            img.src = ev.target.result;
            img.alt = file.name;
            preview.appendChild(img);
          };
          reader.readAsDataURL(file);
        });
      }
    });
  });

  /* --- Drag & Drop Upload Zone --- */
  document.querySelectorAll('.upload-zone').forEach(function (zone) {
    zone.addEventListener('dragover', function (e) {
      e.preventDefault();
      zone.classList.add('dragover');
    });

    zone.addEventListener('dragleave', function () {
      zone.classList.remove('dragover');
    });

    zone.addEventListener('drop', function (e) {
      e.preventDefault();
      zone.classList.remove('dragover');
      const input = zone.querySelector('input[type="file"]');
      if (input && e.dataTransfer.files.length) {
        input.files = e.dataTransfer.files;
        const changeEvent = new Event('change', { bubbles: true });
        input.dispatchEvent(changeEvent);
      }
    });
  });

  /* --- Form Validation Helper --- */
  window.validateForm = function (formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    let isValid = true;
    form.querySelectorAll('[required]').forEach(function (field) {
      const errorEl = field.closest('.form-group').querySelector('.error-text');
      if (errorEl) errorEl.textContent = '';

      if (!field.value.trim()) {
        isValid = false;
        field.classList.add('error');
        if (errorEl) {
          errorEl.textContent = 'Field ini wajib diisi';
        }
      } else {
        field.classList.remove('error');
      }
    });

    return isValid;
  };

  /* --- Confirm Dialog --- */
  window.confirmAction = function (message, callback) {
    if (confirm(message || 'Apakah Anda yakin?')) {
      if (typeof callback === 'function') callback();
      return true;
    }
    return false;
  };

  /* --- Copy to Clipboard --- */
  window.copyToClipboard = function (text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () {
        showToast('Copied!', 'success');
      });
    } else {
      // Fallback
      const textarea = document.createElement('textarea');
      textarea.value = text;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
      showToast('Copied!', 'success');
    }
  };

  /* --- Toast Notification --- */
  window.showToast = function (message, type) {
    type = type || 'info';
    const container = document.getElementById('flash-container');
    if (!container) {
      const newContainer = document.createElement('div');
      newContainer.className = 'toast-container';
      newContainer.id = 'flash-container';
      document.body.appendChild(newContainer);
    }

    const toast = document.createElement('div');
    toast.className = 'toast toast-' + type;
    const icons = {
      success: 'check-circle',
      error: 'exclamation-circle',
      warning: 'exclamation-triangle',
      info: 'info-circle'
    };
    toast.innerHTML = '<i class="fas fa-' + (icons[type] || 'info-circle') + '"></i><span>' + message + '</span>';
    toast.onclick = function () { toast.remove(); };

    const c = document.getElementById('flash-container');
    c.appendChild(toast);

    setTimeout(function () {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(function () {
        if (toast.parentNode) toast.remove();
      }, 300);
    }, 5000);
  };

  /* --- Loading State --- */
  window.showLoading = function () {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.id = 'loading-overlay';
    overlay.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(overlay);
  };

  window.hideLoading = function () {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) overlay.remove();
  };

  /* --- AJAX Form Submit Helper --- */
  window.ajaxSubmit = function (url, data, onSuccess, onError) {
    showLoading();
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify(data)
    })
    .then(function (response) {
      return response.json().then(function (json) {
        return { status: response.status, json: json };
      });
    })
    .then(function (result) {
      hideLoading();
      if (result.status >= 200 && result.status < 300) {
        if (typeof onSuccess === 'function') onSuccess(result.json);
      } else {
        if (typeof onError === 'function') onError(result.json);
        else showToast(result.json.message || 'Terjadi kesalahan', 'error');
      }
    })
    .catch(function (err) {
      hideLoading();
      showToast('Network error: ' + err.message, 'error');
      if (typeof onError === 'function') onError(err);
    });
  };

  /* --- Scroll Animation: fade-in-up on viewport enter --- */
  const animateOnScroll = function () {
    const elements = document.querySelectorAll('.animate-on-scroll');
    if (!elements.length) return;

    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('fade-in-up');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    elements.forEach(function (el) {
      observer.observe(el);
    });
  };
  animateOnScroll();

  /* --- Service Pricing Toggle --- */
  const initServiceToggle = function () {
    const toggle = document.getElementById('pricing-toggle');
    if (!toggle) return;

    const monthlyPrices = document.querySelectorAll('.price-monthly');
    const yearlyPrices = document.querySelectorAll('.price-yearly');

    toggle.addEventListener('change', function () {
      const isYearly = toggle.checked;
      monthlyPrices.forEach(function (el) {
        el.style.display = isYearly ? 'none' : 'block';
      });
      yearlyPrices.forEach(function (el) {
        el.style.display = isYearly ? 'block' : 'none';
      });
    });
  };
  initServiceToggle();

  /* --- Booking Date Picker --- */
  const initDatePicker = function () {
    const dateInput = document.getElementById('booking-date');
    const timeSelect = document.getElementById('booking-time');
    const artistSelect = document.getElementById('booking-artist');

    if (dateInput && timeSelect) {
      dateInput.addEventListener('change', function () {
        // Enable time slots that are available for the selected date
        const selectedDate = dateInput.value;
        const selectedArtist = artistSelect ? artistSelect.value : '';

        if (selectedDate && selectedArtist) {
          fetchAvailableSlots(selectedDate, selectedArtist);
        }
      });
    }
  };
  initDatePicker();

  window.fetchAvailableSlots = function (date, artistId) {
    const timeSelect = document.getElementById('booking-time');
    if (!timeSelect) return;

    fetch('/api/slots?date=' + encodeURIComponent(date) + '&artist_id=' + encodeURIComponent(artistId))
      .then(function (res) { return res.json(); })
      .then(function (data) {
        timeSelect.innerHTML = '';
        if (data.slots && data.slots.length) {
          data.slots.forEach(function (slot) {
            const opt = document.createElement('option');
            opt.value = slot;
            opt.textContent = slot;
            timeSelect.appendChild(opt);
          });
        } else {
          timeSelect.innerHTML = '<option value="">Tidak ada slot tersedia</option>';
        }
      })
      .catch(function () {
        // Fallback: show default times
      });
  };

  /* --- Initialize all tooltips --- */
  if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
      new bootstrap.Tooltip(el);
    });
  }

  console.log('%c InkMaster Studio ', 'background:#d4a853;color:#000;font-size:14px;font-weight:bold;padding:4px 8px;border-radius:4px;');
  console.log('%c Built with passion for tattoo art. ', 'color:#888;font-size:12px;');
});
