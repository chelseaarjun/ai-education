// Minimize/expand module nav bar on mobile and adjust content padding

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.module-nav').forEach(nav => {
    // Minimize by default on mobile
    if (window.innerWidth <= 600) {
      nav.classList.add('minimized');
    }
    // Add toggle button if not present
    if (!nav.querySelector('.module-nav-toggle')) {
      const btn = document.createElement('button');
      btn.className = 'module-nav-toggle';
      btn.setAttribute('aria-label', 'Toggle navigation');
      btn.textContent = nav.classList.contains('minimized') ? '+' : '−';
      nav.insertBefore(btn, nav.firstChild);
      btn.addEventListener('click', function() {
        nav.classList.toggle('minimized');
        btn.textContent = nav.classList.contains('minimized') ? '+' : '−';
        adjustContentPadding(nav);
        updateModuleNavVisibility();
      });
    } else {
      // Update toggle button symbol if minimized by default
      const btn = nav.querySelector('.module-nav-toggle');
      btn.textContent = nav.classList.contains('minimized') ? '+' : '−';
    }
    // Initial adjustment
    adjustContentPadding(nav);
  });

  // Adjust on window resize as well
  window.addEventListener('resize', function() {
    document.querySelectorAll('.module-nav').forEach(nav => adjustContentPadding(nav));
  });

  function adjustContentPadding(nav) {
    const content = document.querySelector('.content-inner');
    const courseNav = document.querySelector('.course-nav');
    let pad = 0;
    if (courseNav && getComputedStyle(courseNav).position === 'fixed') {
      pad += courseNav.offsetHeight;
    }
    // Only add module nav height if it's fixed and not minimized
    if (nav && getComputedStyle(nav).position === 'fixed' && !nav.classList.contains('minimized')) {
      pad += nav.offsetHeight;
    } else if (nav && getComputedStyle(nav).position === 'fixed' && nav.classList.contains('minimized')) {
      pad += 44; // Height of minimized nav bar (adjust if needed)
    }
    if (content) content.style.paddingTop = pad + 'px';
  }

  // Lab button launch logic (reusable for any page)
  const labBtn = document.querySelector('.lab-nav-btn[data-notebook]');
  if (labBtn) {
    labBtn.addEventListener('click', function() {
      const notebookPath = labBtn.getAttribute('data-notebook');
      // Replace with your actual GitHub repo and branch if needed
      const binderUrl = `https://mybinder.org/v2/gh/chelseaarjun/ai-education/main?filepath=${encodeURIComponent(notebookPath)}`;
      window.open(binderUrl, '_blank');
    });
  }

  updateModuleNavVisibility();
});

// Add smooth transition to .content-inner
(function() {
  const style = document.createElement('style');
  style.textContent = `.content-inner { transition: padding-top 0.3s cubic-bezier(0.4,0,0.2,1); }`;
  document.head.appendChild(style);
})();

function updateModuleNavVisibility() {
  document.querySelectorAll('.module-nav').forEach(nav => {
    const minimized = nav.classList.contains('minimized');
    const btns = nav.querySelectorAll('.module-nav-btn');
    btns.forEach(btn => {
      if (minimized) {
        btn.style.display = btn.classList.contains('active') ? '' : 'none';
      } else {
        btn.style.display = '';
      }
    });
  });
}
window.updateModuleNavVisibility = updateModuleNavVisibility; 