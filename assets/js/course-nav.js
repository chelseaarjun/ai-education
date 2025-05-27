// Course Navigation JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Create the navigation HTML based on current path
    // Determine if we're in the root or pages directory
    const isInPagesDir = window.location.pathname.includes('/pages/');
    const rootPath = isInPagesDir ? '../' : '';
    
    const navHTML = `
    <nav class="course-nav">
        <div class="course-nav-container">
            <div class="course-nav-logo-container">
                <a href="${rootPath}index.html#introduction" class="course-nav-logo">AI Foundations Course</a>
            </div>
            <button class="course-nav-mobile-toggle" aria-label="Toggle navigation menu">☰</button>
            <div class="course-nav-menu">
                <a href="${rootPath}index.html#introduction" class="course-nav-home">Home</a>
                
                <div class="course-nav-dropdown">
                    <button class="course-nav-dropdown-btn">Part 1: Foundational Concepts</button>
                    <div class="course-nav-dropdown-content">
                        <a href="${rootPath}pages/llm.html" class="course-nav-dropdown-item available">LLM Concepts</a>
                        <a href="${rootPath}pages/prompts.html" class="course-nav-dropdown-item available">Prompt Engineering</a>
                        <a href="${rootPath}pages/agents.html" class="course-nav-dropdown-item available">Agents</a>
                        <a href="${rootPath}pages/mcp.html" class="course-nav-dropdown-item available">Model Context Protocol (MCP)</a>
                    </div>
                </div>
                
                <div class="course-nav-dropdown">
                    <button class="course-nav-dropdown-btn">Part 2: Building AI Applications</button>
                    <div class="course-nav-dropdown-content">
                        <a href="${rootPath}pages/aws-bedrock.html" class="course-nav-dropdown-item available">AWS Bedrock</a>
                        <a href="${rootPath}pages/open-source.html" class="course-nav-dropdown-item available">Open Source Tools & Frameworks</a>
                        <a href="#" class="course-nav-dropdown-item coming-soon">LLMOps <span>Coming Soon</span></a>
                        <a href="#" class="course-nav-dropdown-item coming-soon">Prompt-Driven Dev <span>Coming Soon</span></a>
                    </div>
                </div>
            </div>
            <a href="https://www.linkedin.com/in/arjun-a-883b2622/" target="_blank" rel="noopener" class="course-nav-linkedin" style="margin-left:20px;display:flex;align-items:center;gap:6px;color:#0a66c2;font-weight:500;text-decoration:none;">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="#0a66c2" style="vertical-align:middle;"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-10h3v10zm-1.5-11.268c-.966 0-1.75-.784-1.75-1.75s.784-1.75 1.75-1.75 1.75.784 1.75 1.75-.784 1.75-1.75 1.75zm15.5 11.268h-3v-5.604c0-1.337-.025-3.063-1.868-3.063-1.868 0-2.154 1.459-2.154 2.968v5.699h-3v-10h2.881v1.367h.041c.401-.761 1.379-1.563 2.838-1.563 3.036 0 3.6 2.001 3.6 4.601v5.595z"/></svg>
                <span>Contact Me</span>
            </a>
        </div>
    </nav>
    `;
    
    // Insert the navigation at the beginning of the body
    document.body.insertAdjacentHTML('afterbegin', navHTML);
    
    // Utility: Set .content-inner padding-top to nav heights
    function setContentInnerPadding() {
        const courseNav = document.querySelector('.course-nav');
        const moduleNav = document.querySelector('.module-nav');
        const contentInner = document.querySelector('.content-inner');
        if (contentInner) {
            let pad = 0;
            if (courseNav) pad += courseNav.offsetHeight;
            if (moduleNav) pad += moduleNav.offsetHeight;
            // Add a small px for safety
            contentInner.style.paddingTop = (pad + 2) + 'px';
        }
    }

    // Utility: Set scroll-margin-top on all section targets to nav heights
    function setSectionScrollMargin() {
        const courseNav = document.querySelector('.course-nav');
        const moduleNav = document.querySelector('.module-nav');
        let margin = 0;
        if (courseNav) margin += courseNav.offsetHeight;
        if (moduleNav) margin += moduleNav.offsetHeight;
        margin += 2; // safety buffer
        // All <section>, .module-section, and elements with an id
        const sectionEls = [
            ...document.querySelectorAll('section'),
            ...document.querySelectorAll('.module-section'),
            ...Array.from(document.querySelectorAll('[id]')).filter(el => el.tagName !== 'SECTION' && !el.classList.contains('module-section'))
        ];
        sectionEls.forEach(el => {
            el.style.scrollMarginTop = margin + 'px';
        });
    }

    // Use requestAnimationFrame to ensure navs/content are rendered
    function setOffsetsAfterRender() {
        requestAnimationFrame(() => {
            setContentInnerPadding();
            setSectionScrollMargin();
        });
    }
    setOffsetsAfterRender();
    window.addEventListener('resize', setOffsetsAfterRender);
    
    // Mobile menu toggle functionality
    const mobileToggle = document.querySelector('.course-nav-mobile-toggle');
    const navMenu = document.querySelector('.course-nav-menu');
    
    if (mobileToggle) {
        mobileToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
    
    // Dropdown hover delay for desktop
    document.querySelectorAll('.course-nav-dropdown').forEach(dropdown => {
        let hoverTimeout;
        const button = dropdown.querySelector('.course-nav-dropdown-btn');

        // Show dropdown after delay on mouseenter (desktop only)
        button.addEventListener('mouseenter', function() {
            if (window.innerWidth > 768) {
                hoverTimeout = setTimeout(() => {
                    dropdown.classList.add('active');
                }, 400); // 400ms delay
            }
        });

        // Cancel show if mouse leaves before delay
        button.addEventListener('mouseleave', function() {
            if (window.innerWidth > 768) {
                clearTimeout(hoverTimeout);
            }
        });

        // Hide dropdown on mouseleave from dropdown area
        dropdown.addEventListener('mouseleave', function() {
            if (window.innerWidth > 768) {
                clearTimeout(hoverTimeout);
                dropdown.classList.remove('active');
            }
        });

        // Mobile: show/hide on click
        button.addEventListener('click', function(e) {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                // Close all other dropdowns
                document.querySelectorAll('.course-nav-dropdown').forEach(function(otherDropdown) {
                    if (otherDropdown !== dropdown) {
                        otherDropdown.classList.remove('active');
                    }
                });
                dropdown.classList.toggle('active');
            }
        });
    });
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
            // If click is outside the nav menu and the menu is open
            if (!e.target.closest('.course-nav-menu') && 
                !e.target.closest('.course-nav-mobile-toggle') && 
                navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
            }
        }
    });

    // On initial load, ensure offsets are set after navs and content are visible
    setOffsetsAfterRender();

    // Patch: After showing a section, re-run offsets after DOM updates
    function rerunOffsetsAfterSectionChange() {
        setTimeout(setOffsetsAfterRender, 0);
    }
    // Nav bar button clicks
    document.querySelectorAll('.module-nav-btn').forEach(btn => {
        btn.addEventListener('click', rerunOffsetsAfterSectionChange);
    });
    // Section nav btns (Back/Next)
    document.querySelectorAll('.section-nav-btns button').forEach(btn => {
        btn.addEventListener('click', rerunOffsetsAfterSectionChange);
    });
    // Hashchange (for anchor navigation)
    window.addEventListener('hashchange', rerunOffsetsAfterSectionChange);
});