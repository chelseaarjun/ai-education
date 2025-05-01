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
                        <a href="${rootPath}pages/llm-concepts-improved.html" class="course-nav-dropdown-item available">LLM Concepts</a>
                        <a href="${rootPath}pages/prompt-engineering-guide.html" class="course-nav-dropdown-item available">Prompting Strategies</a>
                        <a href="#" class="course-nav-dropdown-item coming-soon">Agents <span>Coming Soon</span></a>
                        <a href="#" class="course-nav-dropdown-item coming-soon">LLMOps <span>Coming Soon</span></a>
                    </div>
                </div>
                
                <div class="course-nav-dropdown">
                    <button class="course-nav-dropdown-btn">Part 2: Building AI Applications</button>
                    <div class="course-nav-dropdown-content">
                        <a href="${rootPath}pages/open-source-tools.html" class="course-nav-dropdown-item available">Open Source Tools</a>
                        <a href="#" class="course-nav-dropdown-item coming-soon">AWS Bedrock <span>Coming Soon</span></a>
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
});