// Update penalty unit when type changes
document.getElementById('penalty_type').addEventListener('change', function() {
    var unit = this.value === 'percentage' ? '%' : 'points';
    document.getElementById('penalty_unit').textContent = unit;
});

// Show status message
function showMessage(message, isError = false) {
    const results = document.getElementById('results');
    results.innerHTML = `<div class="alert alert-${isError ? 'danger' : 'success'}">${message}</div>`;
    setTimeout(() => {
        results.innerHTML = '';
    }, 3000);
}

// Handle form submission
document.getElementById('penalty-settings-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    let data = {
        enabled: document.getElementById('penalty_enabled').checked,
        penalty_type: document.getElementById('penalty_type').value,
        penalty_value: parseInt(document.getElementById('penalty_value').value) || 5
    };

    // Clear previous results
    document.getElementById('results').innerHTML = '';

    CTFd.fetch('/api/v1/penalties/settings', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(response => {
        if (response.success) {
            showMessage('Settings saved successfully!');
        } else {
            showMessage('Failed to save settings', true);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Error saving settings', true);
    });
});