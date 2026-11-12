/**
 * AI STUDY MATE - Core Frontend Script
 */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initSidebar();
  initGlobalSearch();
});

/* Theme Management */
function initTheme() {
  const savedTheme = localStorage.getItem('study_mate_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);

  const toggleBtn = document.getElementById('themeToggleBtn');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      const nextTheme = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', nextTheme);
      localStorage.setItem('study_mate_theme', nextTheme);
      updateThemeIcon(nextTheme);
    });
  }
}

function updateThemeIcon(theme) {
  const icon = document.querySelector('#themeToggleBtn i');
  if (icon) {
    if (theme === 'light') {
      icon.className = 'bi bi-moon-stars-fill text-primary';
    } else {
      icon.className = 'bi bi-sun-fill text-warning';
    }
  }
}

/* Mobile Sidebar Toggle */
function initSidebar() {
  const toggleBtn = document.getElementById('sidebarToggleBtn');
  const sidebar = document.querySelector('.app-sidebar');
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('show');
    });

    // Close when clicking outside on mobile
    document.addEventListener('click', (e) => {
      if (window.innerWidth < 992) {
        if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target) && sidebar.classList.contains('show')) {
          sidebar.classList.remove('show');
        }
      }
    });
  }
}

/* Unified Global Search */
function initGlobalSearch() {
  const searchInput = document.getElementById('globalSearchInput');
  const resultsBox = document.getElementById('globalSearchResults');
  if (!searchInput || !resultsBox) return;

  let debounceTimer;

  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.trim();
    clearTimeout(debounceTimer);

    if (query.length < 2) {
      resultsBox.classList.remove('show');
      resultsBox.innerHTML = '';
      return;
    }

    debounceTimer = setTimeout(async () => {
      try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const json = await res.json();
        if (json.success) {
          renderSearchResults(json.data, resultsBox);
        }
      } catch (err) {
        console.error('Search error:', err);
      }
    }, 280);
  });

  // Hide search on outside click
  document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !resultsBox.contains(e.target)) {
      resultsBox.classList.remove('show');
    }
  });
}

function renderSearchResults(data, container) {
  const { documents, questions, answers, notes } = data;
  const total = documents.length + questions.length + answers.length + notes.length;

  if (total === 0) {
    container.innerHTML = `<div class="p-3 text-muted text-center"><i class="bi bi-search me-1"></i> No matching materials found</div>`;
    container.classList.add('show');
    return;
  }

  let html = '';

  if (answers.length > 0) {
    html += `<div class="sidebar-section-title px-3 pt-2 pb-1 text-primary">Generated Answers</div>`;
    answers.forEach(a => {
      html += `
        <a href="/answers?id=${a.id}" class="search-item text-decoration-none">
          <i class="bi bi-chat-left-text text-primary"></i>
          <div class="text-truncate">
            <div class="fw-semibold text-truncate">${escapeHtml(a.question_text)}</div>
            <small class="text-muted">${a.marks} Marks • ${a.created_at}</small>
          </div>
        </a>`;
    });
  }

  if (documents.length > 0) {
    html += `<div class="sidebar-section-title px-3 pt-2 pb-1 text-secondary">Documents</div>`;
    documents.forEach(d => {
      html += `
        <a href="/upload" class="search-item text-decoration-none">
          <i class="bi bi-file-earmark-text text-secondary"></i>
          <div class="text-truncate">
            <div class="fw-semibold text-truncate">${escapeHtml(d.original_filename)}</div>
            <small class="text-muted">${d.file_type.toUpperCase()} • ${d.file_size_formatted}</small>
          </div>
        </a>`;
    });
  }

  if (notes.length > 0) {
    html += `<div class="sidebar-section-title px-3 pt-2 pb-1 text-warning">Study Notes</div>`;
    notes.forEach(n => {
      html += `
        <a href="/notes" class="search-item text-decoration-none">
          <i class="bi bi-journal-text text-warning"></i>
          <div class="text-truncate">
            <div class="fw-semibold text-truncate">${escapeHtml(n.title)}</div>
            <small class="text-muted">${n.created_at}</small>
          </div>
        </a>`;
    });
  }

  container.innerHTML = html;
  container.classList.add('show');
}

/* UI Notification Helper */
function showToast(message, type = 'info') {
  let toastContainer = document.getElementById('toastContainer');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'toastContainer';
    toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    toastContainer.style.zIndex = '9999';
    document.body.appendChild(toastContainer);
  }

  const bgClass = type === 'success' ? 'bg-success' : type === 'danger' ? 'bg-danger' : type === 'warning' ? 'bg-warning text-dark' : 'bg-primary';
  const icon = type === 'success' ? 'bi-check-circle' : type === 'danger' ? 'bi-exclamation-triangle' : 'bi-info-circle';

  const toastEl = document.createElement('div');
  toastEl.className = `toast align-items-center text-white ${bgClass} border-0 show animate-fade-in`;
  toastEl.role = 'alert';
  toastEl.innerHTML = `
    <div class="d-flex">
      <div class="toast-body d-flex align-items-center gap-2">
        <i class="bi ${icon} fs-5"></i>
        <span>${message}</span>
      </div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
    </div>
  `;

  toastContainer.appendChild(toastEl);
  setTimeout(() => {
    toastEl.classList.remove('show');
    setTimeout(() => toastEl.remove(), 300);
  }, 4000);
}

/* HTML Escaper utility */
function escapeHtml(str) {
  if (!str) return '';
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
