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