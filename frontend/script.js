document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const resultCard = document.getElementById('result-card');
    const introCard = document.getElementById('intro-card');
    const loading = document.getElementById('loading');
    const riskBox = document.getElementById('risk-box');
    const riskText = document.getElementById('risk-text');
    const probPercentage = document.getElementById('prob-percentage');
    const probFill = document.getElementById('prob-fill');
    const detailText = document.getElementById('prediction-detail');
    const performanceGrid = document.getElementById('performance-grid');

    // Fetch model performance results from backend
    fetch('http://127.0.0.1:5000/results')
        .then(response => response.json())
        .then(data => {
            Object.keys(data).forEach(model => {
                const accuracy = (data[model].Accuracy * 100).toFixed(1);
                const card = document.createElement('div');
                card.className = 'perf-card';
                card.innerHTML = `
                    <h3>${model}</h3>
                    <div class="perf-value">${accuracy}%</div>
                    <p style="font-size: 0.8rem; color: #64748b; margin-top: 0.5rem;">Accuracy Score</p>
                `;
                performanceGrid.appendChild(card);
            });
        })
        .catch(err => {
            console.error('Error fetching results:', err);
            performanceGrid.innerHTML = '<p>Performance data unavailable. Start the backend server.</p>';
        });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Show loading
        introCard.style.display = 'none';
        resultCard.style.display = 'none';
        loading.style.display = 'block';

        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        try {
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            // Simulate slight delay for effect
            setTimeout(() => {
                loading.style.display = 'none';
                resultCard.style.display = 'block';

                // Update UI based on result
                riskText.innerText = result.risk_level;
                const prob = (result.probability * 100).toFixed(1);
                probPercentage.innerText = `${prob}%`;
                probFill.style.width = `${prob}%`;

                // Update styling
                riskBox.className = 'risk-display';
                if (result.risk_level === 'High') {
                    riskBox.classList.add('risk-high');
                    detailText.innerText = 'High probability of heart disease detected. Urgent medical consultation recommended.';
                } else if (result.risk_level === 'Medium') {
                    riskBox.classList.add('risk-medium');
                    detailText.innerText = 'Moderate risk detected. Periodic screening and lifestyle adjustments advised.';
                } else {
                    riskBox.classList.add('risk-low');
                    detailText.innerText = 'Low risk of heart disease. Maintain a healthy lifestyle and regular check-ups.';
                }
            }, 800);

        } catch (error) {
            console.error('Error:', error);
            loading.style.display = 'none';
            alert('Error connecting to backend server. Please make sure app.py is running.');
        }
    });
});
