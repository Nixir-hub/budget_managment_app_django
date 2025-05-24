
const ctx = document.getElementById('summaryChart').getContext('2d');
const summaryChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Przychody', 'Wydatki'],
        datasets: [{
            label: 'Zestawienie',
            data: summaryData,
            backgroundColor: ['#28a745', '#dc3545'],
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});