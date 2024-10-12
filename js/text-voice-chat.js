const wsText = new WebSocket("ws://localhost:8000/ws/text");

wsText.onopen = () => {
    console.log('Соединение с текстовым чатом установлено');
};

wsText.onmessage = (event) => {
    const messageData = JSON.parse(event.data);
    const chatWindow = document.getElementById("chat-window");
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.textContent = `${messageData.nickname}: ${messageData.text}`;
    chatWindow.appendChild(messageElement);
    chatWindow.scrollTop = chatWindow.scrollHeight;
};

function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const nickname = "Anonymous"; // Упростим для примера
    const message = messageInput.value.trim();

    if (message) {
        const messageData = {nickname: nickname, text: message};
        wsText.send(JSON.stringify(messageData));
        messageInput.value = '';
    }
}
