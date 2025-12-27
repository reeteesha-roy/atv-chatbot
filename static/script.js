function addMessage(text, className) {
    const chatBox = document.getElementById("chatBox");
    const msg = document.createElement("div");
    msg.className = className;
    msg.innerText = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function quickAsk(text) {
  document.getElementById("user-input").value = text;
  sendMessage();
}

function sendMessage() {
    const input = document.getElementById("userInput");
    const userText = input.value.trim();

    if (!userText) return;

    addMessage(userText, "user-message");
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userText })
    })
    .then(res => res.json())
    .then(data => {
        addMessage(data.reply, "bot-message");
    })
    .catch(() => {
        addMessage(" Something went wrong. Please try again.", "bot-message");
    });
}
