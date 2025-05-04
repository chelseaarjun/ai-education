// Reusable module sidebar and section navigation logic
const sectionIds = ['fundamentals', 'memory', 'tools', 'decision-cycle'];

function showSection(id) {
    sectionIds.forEach(sid => {
        document.getElementById(sid).style.display = (sid === id) ? '' : 'none';
    });
    // Update hash if needed
    if (window.location.hash !== '#' + id) {
        history.replaceState(null, '', '#' + id);
    }
    // Highlight module nav bar
    document.querySelectorAll('.module-nav-btn').forEach(btn => {
        if (btn.getAttribute('data-section') === id) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    // Update sidebar
    updateSidebar(id);
}

function updateSidebar(sectionId) {
    const sidebar = document.querySelector('.module-sidebar');
    const section = document.getElementById(sectionId);
    if (!sidebar || !section) return;
    // Find all h3/h4 in the section
    const headings = section.querySelectorAll('h3, h4');
    let html = '';
    if (headings.length > 0) {
        html += '<ul>';
        headings.forEach(h => {
            // Ensure heading has an id for anchor
            if (!h.id) {
                h.id = sectionId + '-' + h.textContent.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-');
            }
            html += `<li><a href="#${h.id}">${h.textContent}</a></li>`;
        });
        html += '</ul>';
    } else {
        html = '<div style="color:#888;font-size:0.95em;">No sub-sections</div>';
    }
    sidebar.innerHTML = `<h4>On this page</h4>${html}`;
    // Add click listeners for smooth scroll
    sidebar.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.getElementById(this.getAttribute('href').slice(1));
            if (target) {
                window.scrollTo({
                    top: target.getBoundingClientRect().top + window.scrollY - 130,
                    behavior: 'smooth'
                });
            }
            // Immediately highlight the clicked link
            sidebar.querySelectorAll('a').forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

function highlightSidebar() {
    const sidebar = document.querySelector('.module-sidebar');
    if (!sidebar) return;
    const links = sidebar.querySelectorAll('a');
    if (!links.length) return;
    let currentId = null;
    let minDist = Infinity;
    links.forEach(link => {
        const target = document.getElementById(link.getAttribute('href').slice(1));
        if (target) {
            const rect = target.getBoundingClientRect();
            // Only consider headings above the top nav, but closest to it
            if (rect.top - 135 <= 0 && Math.abs(rect.top - 135) < minDist) {
                minDist = Math.abs(rect.top - 135);
                currentId = target.id;
            }
        }
    });
    links.forEach(link => {
        if (link.getAttribute('href').slice(1) === currentId) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}
window.addEventListener('scroll', highlightSidebar);

function scrollToSectionTop(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        window.scrollTo({
            top: section.getBoundingClientRect().top + window.scrollY - 130,
            behavior: 'smooth'
        });
    }
}

// Button event listeners for section nav btns
sectionIds.forEach((id, idx) => {
    const backBtn = document.getElementById('back-' + id);
    const nextBtn = document.getElementById('next-' + id);
    if (backBtn) {
        backBtn.addEventListener('click', () => {
            if (idx > 0) {
                showSection(sectionIds[idx-1]);
                scrollToSectionTop(sectionIds[idx-1]);
            }
        });
    }
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            if (idx < sectionIds.length-1) {
                showSection(sectionIds[idx+1]);
                scrollToSectionTop(sectionIds[idx+1]);
            }
        });
    }
});

// Module nav bar event listeners
if (document.querySelectorAll('.module-nav-btn').length) {
    document.querySelectorAll('.module-nav-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const section = this.getAttribute('data-section');
            if (sectionIds.includes(section)) {
                showSection(section);
            }
        });
    });
}

// Hash navigation
function handleHash() {
    const hash = window.location.hash.replace('#','');
    if (sectionIds.includes(hash)) {
        showSection(hash);
    } else {
        showSection(sectionIds[0]);
    }
    setTimeout(highlightSidebar, 200);
}
window.addEventListener('hashchange', handleHash);
document.addEventListener('DOMContentLoaded', handleHash); 