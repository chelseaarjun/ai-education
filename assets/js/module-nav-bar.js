// Minimize/expand module nav bar on mobile and adjust content padding

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.module-nav').forEach(nav => {
    // Add toggle button if not present
    if (!nav.querySelector('.module-nav-toggle')) {
      const btn = document.createElement('button');
      btn.className = 'module-nav-toggle';
      btn.setAttribute('aria-label', 'Toggle navigation');
      btn.textContent = '−';
      nav.insertBefore(btn, nav.firstChild);
      btn.addEventListener('click', function() {
        nav.classList.toggle('minimized');
        btn.textContent = nav.classList.contains('minimized') ? '+' : '−';
        adjustContentPadding(nav);
      });
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
});

// Add smooth transition to .content-inner
(function() {
  const style = document.createElement('style');
  style.textContent = `.content-inner { transition: padding-top 0.3s cubic-bezier(0.4,0,0.2,1); }`;
  document.head.appendChild(style);
})(); 