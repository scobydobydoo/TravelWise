const BASE_URL = "http://127.0.0.1:5000";


function signup() {
    let username = document.getElementById("username").value.trim();
    let password = document.getElementById("password").value.trim();
    let msg = document.getElementById("msg");

    if (!username || !password) {
        msg.innerText = " Fill all fields";
        return;
    }

    fetch(`${BASE_URL}/signup`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
        msg.innerText = data.message;

        if (data.status === "success") {
            setTimeout(() => {
                window.location.href = "index.html";
            }, 1000);
        }
    })
    .catch(() => {
        msg.innerText = " Server error";
    });
}


function login() {
    let username = document.getElementById("username").value.trim();
    let password = document.getElementById("password").value.trim();
    let msg = document.getElementById("msg");

    if (!username || !password) {
        msg.innerText = " Enter all fields";
        return;
    }

    fetch(`${BASE_URL}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            msg.innerText = " Login successful";

            localStorage.setItem("user", username);

            setTimeout(() => {
                window.location.href = "main.html"; 
            }, 800);
        } else {
            msg.innerText = " Invalid credentials";
        }
    })
    .catch(() => {
        msg.innerText = " Server not responding";
    });
}