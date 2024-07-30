document.getElementById('login-button').addEventListener('click', () => {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    fetch('http://localhost:8080/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    })
    .then(response => {
        if (response.ok) {
            sessionStorage.setItem('username', username);
            window.location.href = 'index.html';
        } else {
            alert('Login failed');
        }
    });
});

document.getElementById('register-button').addEventListener('click', () => {
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    fetch('http://localhost:8080/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    })
    .then(response => {
        if (response.ok) {
            alert('Registration successful');
        } else {
            alert('Registration failed');
        }
    });
});
