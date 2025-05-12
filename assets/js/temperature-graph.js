// assets/js/temperature-graph.js

// Generic logits for demonstration
const logits = [2.0, 1.0, 0.5, 0.0, -1.0];
const tokenLabels = ["Token A", "Token B", "Token C", "Token D", "Token E"];

// Softmax function with temperature
function softmax(logits, temperature) {
    const scaled = logits.map(x => x / temperature);
    const maxLogit = Math.max(...scaled); // for numerical stability
    const exps = scaled.map(x => Math.exp(x - maxLogit));
    const sumExps = exps.reduce((a, b) => a + b, 0);
    return exps.map(x => x / sumExps);
}

// Initial temperature
let temperature = 1.0;

// Chart.js setup
const ctx = document.getElementById('temperature-prob-chart').getContext('2d');
let chart = null;

function renderChart(probabilities) {
    if (chart) {
        chart.data.datasets[0].data = probabilities;
        chart.options.scales.y.max = 1;
        chart.update();
    } else {
        chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: tokenLabels,
                datasets: [{
                    label: 'Probability',
                    data: probabilities,
                    backgroundColor: '#3498db',
                }]
            },
            options: {
                responsive: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1,
                        ticks: {
                            callback: function(value) { return (value * 100).toFixed(0) + '%'; }
                        },
                        title: { display: true, text: 'Probability' }
                    },
                    x: {
                        title: { display: true, text: 'Token' }
                    }
                }
            }
        });
    }
}

// Initial render
const initialProbs = softmax(logits, temperature);
renderChart(initialProbs);

document.getElementById('temperature-slider').addEventListener('input', function(e) {
    temperature = parseFloat(e.target.value);
    document.getElementById('temperature-value').textContent = temperature.toFixed(2);
    const probs = softmax(logits, temperature);
    renderChart(probs);
}); 