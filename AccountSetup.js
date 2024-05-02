function handleFormSubmit(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    fetch(form.action, {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not OK');
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            window.location.href = 'https://terranovaai.net/login.html';
        } else {
            alert('Failed to create account. Please try again. Message: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Fetch error:', error);
        alert('Fetch Error: ' + error.message);
    });
}
