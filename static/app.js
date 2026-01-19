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
    const rawSummary = data.summary || "No summary could be generated.";

    // Split by double newlines but also filter out any empty strings or literal \n sequences
    const points = rawSummary.split(/\n\n|\\n\\n/).filter(p => p.trim().length > 0);

    globalSummaryText.innerHTML = points.map(point => {
        let content = point.trim();

        // Use regex to inject a class into the footer for better styling
        // The footer starts with (Posted...
        content = content.replace(/(\(Posted.*)/, '<div class="pill-footer">$1</div>');

        // Wrap the whole point in a capsule div
        return `<div class="summary-capsule">${content}</div>`;
    }).join('');

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
        console.log(article);
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
