function getQuote(philosopher) {
    fetch(`/philosophers/${philosopher}`)
        .then(response => response.text())
        .then(html => document.getElementById('quote').innerHTML = html)
}