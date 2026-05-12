const SERVER = "http://localhost:5000";

document.addEventListener("DOMContentLoaded", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        const url      = new URL(tabs[0].url);
        const hostname = url.hostname.replace("www.", "");
        document.getElementById("site-name").textContent = "Site: " + hostname;
        document.getElementById("site-name").dataset.site = hostname;
    });
});


document.getElementById("login-btn").addEventListener("click", async () => {
    const password = document.getElementById("master-pw").value;

    const res = await fetch(`${SERVER}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ master_password: password })
    });

    if (res.ok) {
        document.getElementById("login-screen").style.display = "none";
        document.getElementById("main-screen").style.display  = "block";
    } else {
        document.getElementById("login-error").textContent = "Wrong password!";
    }
});

document.getElementById("get-btn").addEventListener("click", async () => {
    const site     = document.getElementById("site-name").dataset.site;
    const username = document.getElementById("username").value;

    const res = await fetch(`${SERVER}/get`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ site, username })
    });

    const data = await res.json();

    if (res.ok) {
        
        navigator.clipboard.writeText(data.password);
        document.getElementById("message").textContent = "Password copied to clipboard!";
        document.getElementById("error").textContent   = "";
    } else {
        document.getElementById("error").textContent   = "No entry found.";
        document.getElementById("message").textContent = "";
    }
});

document.getElementById("add-btn").addEventListener("click", async () => {
    const site     = document.getElementById("site-name").dataset.site;
    const username = document.getElementById("username").value;

    const res = await fetch(`${SERVER}/add`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ site, username })
    });

    const data = await res.json();

    if (res.ok) {
        navigator.clipboard.writeText(data.password);
        document.getElementById("message").textContent = "Generated & copied to clipboard!";
        document.getElementById("error").textContent   = "";
    } else {
        document.getElementById("error").textContent   = "Failed to generate.";
    }
});


document.getElementById("logout-btn").addEventListener("click", async () => {
    await fetch(`${SERVER}/logout`, { method: "POST" });
    document.getElementById("login-screen").style.display = "block";
    document.getElementById("main-screen").style.display  = "none";
    document.getElementById("master-pw").value            = "";
});