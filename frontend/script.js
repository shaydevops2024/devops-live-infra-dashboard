function updateStatus() {
    fetch("http://localhost:8000/status")
        .then(res => res.json())
        .then(data => {
            updateBox("db", data.db);
            updateBox("redis", data.redis);
            updateBox("rabbit", data.rabbit);
        })
        .catch(() => console.log("Failed to fetch status"));
}

function updateBox(id, isOnline) {
    const box = document.getElementById(id);
    const status = box.querySelector(".status");

    if (isOnline) {
        status.textContent = "Online";
        status.className = "status online";
    } else {
        status.textContent = "Offline";
        status.className = "status offline";
    }
}

function stopService(name) {
    fetch(`http://localhost:8000/stop/${name}`, { method: "POST" })
        .then(res => res.json())
        .then(() => setTimeout(updateStatus, 1500));
}

function startService(name) {
    fetch(`http://localhost:8000/start/${name}`, { method: "POST" })
        .then(res => res.json())
        .then(() => setTimeout(updateStatus, 2000));
}

function pingService(name) {
    fetch(`http://localhost:8000/ping/${name}`, { method: "POST" })
        .then(res => res.json())
        .then(data => addEvent(name, data.message));
}

function addEvent(serviceId, message) {
    const box = document.getElementById(serviceId);
    const events = box.querySelector(".events");
    const entry = document.createElement("div");
    entry.textContent = message;
    events.appendChild(entry);
    events.scrollTop = events.scrollHeight; // auto scroll
}

// Load logs from Postgres on page load
function loadLogsFromDB() {
    ["db", "redis", "rabbit"].forEach(serviceId => {
        fetch(`http://localhost:8000/logs/${serviceId}`)
            .then(res => res.json())
            .then(data => {
                const box = document.getElementById(serviceId);
                const events = box.querySelector(".events");
                events.innerHTML = ""; // clear before loading
                data.forEach(log => {
                    const entry = document.createElement("div");
                    entry.textContent = log.message;
                    events.appendChild(entry);
                });
                events.scrollTop = events.scrollHeight; // auto scroll
            })
            .catch(err => console.log("Failed to fetch logs:", err));
    });
}

window.onload = () => {
    loadLogsFromDB();
    updateStatus();
    setInterval(updateStatus, 2000);
};
