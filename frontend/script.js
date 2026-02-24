/*
    Created By : Christian Merriman
    Date : 2/2026
*/

let chatHistory = [];

document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    // Attach listeners FIRST (prevents the "click a bunch" issue)
    input.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') sendToSentinel();
    });

    if (sendBtn) {
        sendBtn.addEventListener('click', sendToSentinel);
    }

    // Attempt to connect and pull history
    checkConnectionAndLoad();

    // Check every 5 seconds to see if the server came back online
    setInterval(checkConnectionAndLoad, 5000);
});

document.addEventListener('DOMContentLoaded', () => {
    // ... your existing button/input listeners ...

    // Start the heartbeat check immediately
    checkConnectionAndLoad();
    
    // Check every 5 seconds to see if the server came back online
    setInterval(checkConnectionAndLoad, 5000);
});

async function checkConnectionAndLoad() {
    const statusText = document.getElementById('connection-status');
    
    try {
        const response = await fetch('http://127.0.0.1:8000/get_history');
        
        if (response.ok) {
            const data = await response.json();

            // If we were offline and now we're online, load the history
            if (statusText.classList.contains('offline')) {
                chatHistory = data.history || [];
                renderFullHistory();
            }

            // Update UI to Online
            statusText.innerText = "ONLINE";
            statusText.classList.remove('offline');
            statusText.classList.add('online');
        }
    } catch (error) {
        // Server is still down
        statusText.innerText = "OFFLINE";
        statusText.classList.remove('online');
        statusText.classList.add('offline');
    }
}
async function sendToSentinel() {
    const input = document.getElementById('user-input');
    const display = document.getElementById('chat-display');
    const userText = input.value.trim();

    if (!userText) return; 

    chatHistory.push({ role: "user", content: userText });
    display.innerHTML += `<div class="message user-message">${userText}</div>`;
    input.value = ""; 
    scrollToBottom();

    try {
        const response = await fetch('http://127.0.0.1:8000/ask_sentinel', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ messages: chatHistory })
        });

        const data = await response.json();
        chatHistory = data.history;

        display.innerHTML += `<div class="message ai-message">${data.reply}</div>`;
        scrollToBottom();

    } catch (error) {
        display.innerHTML += `<div class="message ai-message">ERROR: Could not connect to Sentinel Core.</div>`;
        scrollToBottom();
    }
}

// Helper: Keep the chat focused on the latest messages
function scrollToBottom() {
    const display = document.getElementById('chat-display');
    if (display) {
        display.scrollTop = display.scrollHeight;
    }
}

// Helper: Draw all messages (used on page load)
function renderFullHistory() {
    const display = document.getElementById('chat-display');
    if (!display) return;
    
    display.innerHTML = ""; // Clear loader
    chatHistory.forEach(msg => {
        if (msg.role !== 'system') { // Don't show system instructions to the user
            const cssClass = msg.role === 'user' ? 'user-message' : 'ai-message';
            display.innerHTML += `<div class="message ${cssClass}">${msg.content}</div>`;
        }
    });
    scrollToBottom();
}