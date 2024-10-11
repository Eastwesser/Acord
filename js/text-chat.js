const wsText = new WebSocket("ws://localhost:8000/ws/text");

wsText.onopen = () => {
    console.log('Соединение с текстовым чатом установлено');
};

wsText.onmessage = (event) => {
    const chatWindow = document.getElementById('chat-window');
    const messageItem = document.createElement('div');
    messageItem.classList.add('message');
    messageItem.textContent = event.data;
    chatWindow.appendChild(messageItem);
    chatWindow.scrollTop = chatWindow.scrollHeight;
};

function sendMessage() {
    const input = document.getElementById("messageInput");
    if (input.value !== '') {
        wsText.send(input.value);
        input.value = '';
    }
}
