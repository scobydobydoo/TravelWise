function signup() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    fetch("http://127.0.0.1:5000/signup", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("msg").innerText = data.message;
    });
}




function login() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            window.location.href = "index.html";
        } else {
            document.getElementById("msg").innerText = "Invalid credentials";
        }
    });
}