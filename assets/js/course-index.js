// Course Index JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Create the index HTML based on the page
    function createIndex() {
        // Get the current page
        let currentPage = window.location.pathname.split('/').pop();
        
        // Handle pages in the pages directory
        if (window.location.pathname.includes('/pages/')) {
            currentPage = currentPage;
        }
        
        // Define the index content based on the page
        let indexContent = '';
        let indexTitle = 'Contents';
        
        if (currentPage === 'index.html' || currentPage === '') {
            indexTitle = 'Course Contents';
            indexContent = `
                <li><a href="#introduction" class="nav-link">Introduction</a></li>
                <li><a href="#genai-section" class="nav-link">Understanding Generative AI</a></li>
                <li><a href="#ai-evolution" class="nav-link">Evolution of AI</a></li>
                <li><a href="#course-structure" class="nav-link">Course Structure</a></li>
            `;
        } else if (currentPage === 'llm-concepts-improved.html') {
            indexTitle = 'LLM Concepts';
            indexContent = `
                <li><a href="#introduction" class="nav-link">Introduction</a></li>
                <li><a href="#context-window" class="nav-link">1. Context Window</a></li>
                <li><a href="#tokenization" class="nav-link">2. Tokenization</a></li>
                <li><a href="#embeddings" class="nav-link">3. Embeddings</a></li>
                <li><a href="#temperature" class="nav-link">4. Temperature & Sampling</a></li>
                <li><a href="#response-format" class="nav-link">5. Response Formats</a></li>
                <li><a href="#model-selection" class="nav-link">6. Model Selection</a></li>
                <li><a href="#quiz-section" class="nav-link">Knowledge Check</a></li>
            `;
        } else if (currentPage === 'prompt-engineering-guide.html') {
            indexTitle = 'Contents';
            indexContent = `
                <li><a href="#introduction" class="nav-link">1. Introduction</a></li>
                <li><a href="#prompt-anatomy" class="nav-link">2. Anatomy of a Prompt</a>
                    <ul class="nav-subsection" style="PADDING-LEFT: 12px">
                        <li><a href="#core-principles" class="nav-link">2.1 Core Prompting Principles</a></li>
                    </ul>
                </li>
                <li><a href="#basic-techniques" class="nav-link">3. Basic Techniques</a>
                    <ul class="nav-subsection" style="PADDING-LEFT: 12px">
                        <li><a href="#shot-prompting" class="nav-link">3.1 Zero/One/Few-shot</a></li>
                        <li><a href="#role-based" class="nav-link">3.2 Instruction-based</a></li>
                        <li><a href="#constraint-based" class="nav-link">3.3 Constraint-based</a></li>
                    </ul>
                </li>
                <li><a href="#advanced-techniques" class="nav-link">4. Advanced Techniques</a>
                    <ul class="nav-subsection" style="PADDING-LEFT: 12px">
                        <li><a href="#chain-of-thought" class="nav-link">4.1 Chain-of-thought</a></li>
                        <li><a href="#prompt-chaining" class="nav-link">4.2 Prompt Chaining</a></li>
                        <li><a href="#react" class="nav-link">4.3 ReAct</a></li>
                        <li><a href="#rag" class="nav-link">4.4 RAG</a></li>
                    </ul>
                </li>
                <li><a href="#practical-application" class="nav-link">5. Practical Application</a></li>
                <li><a href="#resources" class="nav-link">6. Resources</a></li>
            `;
        } else if (currentPage === 'open-source-tools.html') {
            indexTitle = 'Open Source Tools';
            indexContent = `
                <li><a href="#introduction" class="nav-link">Introduction</a></li>
                <li><a href="#core-frameworks" class="nav-link">Core LLM Frameworks</a>
                    <ul class="nav-subsection">
                        <li><a href="#langchain" class="nav-link">LangChain</a></li>
                        <li><a href="#llamaindex" class="nav-link">LlamaIndex</a></li>
                        <li><a href="#langfuse" class="nav-link">Langfuse</a></li>
                    </ul>
                </li>
                <li><a href="#general-purpose" class="nav-link">General Purpose Libraries</a>
                    <ul class="nav-subsection">
                        <li><a href="#fastapi" class="nav-link">FastAPI</a></li>
                        <li><a href="#streamlit" class="nav-link">Streamlit</a></li>
                        <li><a href="#pydantic" class="nav-link">Pydantic</a></li>
                        <li><a href="#jinja2" class="nav-link">Jinja2</a></li>
                    </ul>
                </li>
                <li><a href="#additional-libraries" class="nav-link">Additional Libraries</a></li>
            `;
            
            // Back to home link is now added directly in the HTML
        }
        
        // Create the index HTML
        const indexHTML = `
        <div class="nav-index">
            <button class="nav-toggle" onclick="toggleNav()">☰</button>
            <div class="nav-content" id="navContent">
                <h3>${indexTitle}</h3>
                <ul>
                    ${indexContent}
                </ul>
            </div>
        </div>
        `;
        
        // Add the index to the page
        document.body.insertAdjacentHTML('afterbegin', indexHTML);
        
        // Add the toggle function if it doesn't exist
        if (typeof window.toggleNav !== 'function') {
            window.toggleNav = function() {
                const navContent = document.getElementById('navContent');
                navContent.classList.toggle('hidden');
                
                // Update button text
                const navToggle = document.querySelector('.nav-toggle');
                if (navContent.classList.contains('hidden')) {
                    navToggle.textContent = '☰';
                } else {
                    navToggle.textContent = '✕';
                }
            };
        }
        
        // Add IDs to sections if they don't have them
        addSectionIds();
    }
    
    // Add IDs to sections that don't have them
    function addSectionIds() {
        // Get all h2 elements without an id
        const h2Elements = document.querySelectorAll('h2:not([id])');
        
        h2Elements.forEach(function(h2) {
            // Create an ID from the text content
            const id = h2.textContent.toLowerCase().replace(/[^a-z0-9]+/g, '-');
            h2.id = id;
        });
        
        // Add id to the first section if it doesn't have one
        const firstSection = document.querySelector('section:not([id])');
        if (firstSection) {
            firstSection.id = 'introduction';
        }
        
        // Add specific IDs for index.html
        if (window.location.pathname.endsWith('index.html') || window.location.pathname.endsWith('/')) {
            const genaiSection = document.querySelector('.genai-section');
            if (genaiSection && !genaiSection.id) {
                genaiSection.id = 'genai-section';
            }
            
            const aiEvolution = document.querySelector('.ai-evolution');
            if (aiEvolution && !aiEvolution.id) {
                aiEvolution.id = 'ai-evolution';
            }
            
            // Add ID to course structure
            const courseStructure = document.querySelector('h2:contains("Course Structure")');
            if (courseStructure && !courseStructure.parentElement.id) {
                courseStructure.parentElement.id = 'course-structure';
            }
            
            // Add IDs to parts
            const parts = document.querySelectorAll('.part');
            if (parts.length >= 2) {
                parts[0].id = 'part1';
                parts[1].id = 'part2';
            }
        }
        
        // Add specific IDs for open-source-tools.html
        if (window.location.pathname.endsWith('open-source-tools.html')) {
            // Add ID to introduction
            const intro = document.querySelector('.course-description');
            if (intro && !intro.id) {
                intro.id = 'introduction';
            }
            
            // Add ID to core frameworks section
            const coreFrameworks = document.querySelector('.section:nth-of-type(1)');
            if (coreFrameworks && !coreFrameworks.id) {
                coreFrameworks.id = 'core-frameworks';
            }
            
            // Add ID to general purpose section
            const generalPurpose = document.querySelector('.section:nth-of-type(2)');
            if (generalPurpose && !generalPurpose.id) {
                generalPurpose.id = 'general-purpose';
            }
            
            // Add ID to additional libraries section
            const additionalLibraries = document.querySelector('.reference-section');
            if (additionalLibraries && !additionalLibraries.id) {
                additionalLibraries.id = 'additional-libraries';
            }
            
            // Add IDs to individual libraries
            const libraries = document.querySelectorAll('.library h3');
            libraries.forEach(function(lib) {
                const name = lib.textContent.split(' ')[0].toLowerCase();
                const parent = lib.closest('.library');
                if (parent && !parent.id) {
                    parent.id = name;
                }
            });
        }
    }
    
    // Call the function to create the index
    createIndex();
});