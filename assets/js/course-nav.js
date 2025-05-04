// Course Navigation JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Create the navigation HTML based on current path
    // Determine if we're in the root or pages directory
    const isInPagesDir = window.location.pathname.includes('/pages/');
    const rootPath = isInPagesDir ? '../' : '';
    
    const navHTML = `
    <nav class="course-nav">
        <div class="course-nav-container">
            <a href="${rootPath}index.html" class="course-nav-logo">AI Foundations Course</a>
            
            <button class="course-nav-mobile-toggle" aria-label="Toggle navigation menu">☰</button>
            
            <div class="course-nav-menu">
                <a href="${rootPath}index.html" class="course-nav-home">Home</a>
                
                <div class="course-nav-dropdown">
                    <button class="course-nav-dropdown-btn">Part 1: Foundational Concepts</button>
                    <div class="course-nav-dropdown-content">
                        <a href="${rootPath}pages/llm.html" class="course-nav-dropdown-item available">LLM Concepts</a>
                        <a href="${rootPath}pages/prompts.html" class="course-nav-dropdown-item available">Prompt Engineering</a>
                        <a href="${rootPath}pages/agents.html" class="course-nav-dropdown-item available">Agents</a>
                        <a href="#" class="course-nav-dropdown-item coming-soon">LLMOps <span>Coming Soon</span></a>
                    </div>
                </div>
                
                <div class="course-nav-dropdown">
                    <button class="course-nav-dropdown-btn">Part 2: Building AI Applications</button>
                    <div class="course-nav-dropdown-content">
                        <a href="#" class="course-nav-dropdown-item coming-soon">Model Context Protocol <span>Coming Soon</span></a>
                        <a href="#" class="course-nav-dropdown-item coming-soon">AWS Bedrock <span>Coming Soon</span></a>
                        <a href="${rootPath}pages/open-source.html" class="course-nav-dropdown-item available">Open Source Tools & Frameworks</a>
                        <a href="#" class="course-nav-dropdown-item coming-soon">Prompt-Driven Dev <span>Coming Soon</span></a>
                    </div>
                </div>
            </div>
        </div>
    </nav>
    `;
    
    // Insert the navigation at the beginning of the body
    document.body.insertAdjacentHTML('afterbegin', navHTML);
    
    // Mobile menu toggle functionality
    const mobileToggle = document.querySelector('.course-nav-mobile-toggle');
    const navMenu = document.querySelector('.course-nav-menu');
    
    if (mobileToggle) {
        mobileToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
    
    // Make dropdowns clickable on mobile
    const dropdowns = document.querySelectorAll('.course-nav-dropdown');
    
    dropdowns.forEach(function(dropdown) {
        const button = dropdown.querySelector('.course-nav-dropdown-btn');
        
        button.addEventListener('click', function(e) {
            // Only handle click on mobile view
            if (window.innerWidth <= 768) {
                e.preventDefault();
                
                // Close all other dropdowns
                dropdowns.forEach(function(otherDropdown) {
                    if (otherDropdown !== dropdown) {
                        otherDropdown.classList.remove('active');
                    }
                });
                
                // Toggle this dropdown
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
});