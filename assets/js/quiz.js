// assets/js/quiz.js

function selectQuizOption(optionEl) {
    console.log('Quiz option clicked:', optionEl.textContent);
    const options = optionEl.parentElement.querySelectorAll('.quiz-option');
    options.forEach(opt => {
        opt.classList.remove('selected', 'correct', 'incorrect');
    });
    optionEl.classList.add('selected');
    if (optionEl.dataset.correct === 'true') {
        optionEl.classList.add('correct');
    } else {
        optionEl.classList.add('incorrect');
    }
    // Show feedback
    const feedback = optionEl.closest('.quiz-container').querySelector('.quiz-feedback');
    if (feedback) {
        feedback.style.display = 'block';
    }
}

function attachQuizListeners() {
    document.querySelectorAll('.quiz-option').forEach(option => {
        option.onclick = function() { selectQuizOption(this); };
    });
}

document.addEventListener('DOMContentLoaded', attachQuizListeners);
// In case of dynamic content, also re-attach on DOM changes
const observer = new MutationObserver(attachQuizListeners);
observer.observe(document.body, { childList: true, subtree: true }); 

// --- Quiz Section Next Button Navigation Logic ---
(function() {
    // Define the module order for each part
    const moduleOrder = [
        ["llm.html", "prompts.html", "agents.html", "mcp.html"], // Part 1
        ["aws-bedrock.html", "open-source.html", "llmops.html", "prompt-driven-dev.html"] // Part 2
    ];

    // Get current filename
    const currentFile = window.location.pathname.split('/').pop();

    // Find current part and module index
    let found = false;
    let partIndex = -1;
    let moduleIndex = -1;
    for (let i = 0; i < moduleOrder.length; i++) {
        const idx = moduleOrder[i].indexOf(currentFile);
        if (idx !== -1) {
            partIndex = i;
            moduleIndex = idx;
            found = true;
            break;
        }
    }

    const nextQuizBtn = document.getElementById('next-quiz-section');
    if (nextQuizBtn && found) {
        // If not the last module in the part, enable and set redirect
        if (moduleIndex < moduleOrder[partIndex].length - 1) {
            nextQuizBtn.disabled = false;
            nextQuizBtn.addEventListener('click', () => {
                window.location.href = moduleOrder[partIndex][moduleIndex + 1];
            });
        } else {
            // Last module in the part: keep disabled or hide
            nextQuizBtn.disabled = true;
            // Or: nextQuizBtn.style.display = 'none';
        }
    }
})(); 