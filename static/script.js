function addMessage(text, className) {
    const chatBox = document.getElementById("chatBox");
    const msg = document.createElement("div");
    msg.className = className;
    msg.innerText = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}
function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (!message) return;

  const chatBox = document.getElementById("chat-box");

  // User message
  const userDiv = document.createElement("div");
  userDiv.className = "user-message";
  userDiv.innerText = message;
  chatBox.appendChild(userDiv);

  input.value = "";
  chatBox.scrollTop = chatBox.scrollHeight;

  // Typing indicator
  const typingDiv = document.createElement("div");
  typingDiv.className = "bot-message typing";
  typingDiv.innerText = "typing...";
  chatBox.appendChild(typingDiv);
  chatBox.scrollTop = chatBox.scrollHeight;

  fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message })
  })
    .then(res => res.json())
    .then(data => {
      chatBox.removeChild(typingDiv);

      const botDiv = document.createElement("div");
      botDiv.className = "bot-message";

      if (data.learn_more) {
        botDiv.innerHTML = `
          ${data.reply}<br>
          <a href="${data.learn_more}" target="_blank">🔗 Learn more</a>
        `;
      } else {
        botDiv.innerText = data.reply;
      }

      chatBox.appendChild(botDiv);
      chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(() => {
      chatBox.removeChild(typingDiv);
      const errorDiv = document.createElement("div");
      errorDiv.className = "bot-message";
      errorDiv.innerText = "Something went wrong. Please try again.";
      chatBox.appendChild(errorDiv);
    });
}

