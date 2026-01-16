const startBtn = document.getElementById('start-btn');
const loadingDiv = document.getElementById('loading');
const resultsView = document.getElementById('results-view');
const globalSummaryText = document.getElementById('global-summary-text');
const resultsContainer = document.getElementById('results-container');
const errorMessage = document.getElementById('error-message');
const errorDetails = document.getElementById('error-details');

startBtn.addEventListener('click', async () => {
    // UI State: Loading
    startBtn.style.display = 'none';
    loadingDiv.classList.remove('hidden');
    resultsView.classList.add('hidden');
    errorMessage.classList.add('hidden');

    try {
        const response = await fetch('/api/scrape_and_summarize');

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        renderData(data);

        // UI State: Success
        loadingDiv.classList.add('hidden');
        resultsView.classList.remove('hidden');

        startBtn.style.display = 'block';
        startBtn.textContent = 'Refresh Digest';

    } catch (error) {
        console.error('Fetch error:', error);
        loadingDiv.classList.add('hidden');
        errorMessage.classList.remove('hidden');
        errorDetails.textContent = error.message;
        startBtn.style.display = 'block';
    }
});

function renderData(data) {
    // 1. Render Global Summary
    // Replace newlines with <br> or <p> for the essay look
    const rawSummary = data.summary || "No summary could be generated.";
    const formattedSummary = rawSummary.split('\n\n').map(p => `<p>${p}</p>`).join('');

    globalSummaryText.innerHTML = formattedSummary;

    // 2. Render Articles List
    const articles = data.articles;
    resultsContainer.innerHTML = '';

    if (articles.length === 0) {
        resultsContainer.innerHTML = '<p style="text-align:center; padding: 1rem;">No relevant articles found.</p>';
        return;
    }

    articles.forEach(article => {
        const item = document.createElement('div');
        item.className = 'card article-item';
        // Simpler card for list view

        item.innerHTML = `
            <div class="card-header" style="margin-bottom:0.5rem;">
                <span class="badge">${article.score} pts</span>
                <span class="date">${article.age_text}</span>
            </div>
            <h3 style="margin: 0; font-size: 1.1rem;">
                <a href="${article.url}" target="_blank" style="text-decoration:none; color:#333;">${article.title}</a>
            </h3>
            <div class="card-footer" style="margin-top:0.5rem; padding-top:0.5rem;">
                <a href="https://news.ycombinator.com/item?id=${article.id}" target="_blank" style="font-size:0.8rem;">View on HN &rarr;</a>
            </div>
        `;

        resultsContainer.appendChild(item);
    });
}
