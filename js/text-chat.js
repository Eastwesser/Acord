const wsText = new WebSocket("ws://localhost:8000/ws/text");
const wsVoice = new WebSocket("ws://localhost:8000/ws/voice");

wsText.onopen = () => console.log('Соединение с текстовым чатом установлено');
wsText.onclose = () => console.log('Соединение с текстовым чатом закрыто');
wsText.onerror = (error) => console.error('Ошибка WebSocket текста:', error);

wsText.onmessage = function (event) {
    const chatWindow = document.getElementById('chat-window');
    const messageItem = document.createElement('div');
    messageItem.classList.add('message');
    messageItem.textContent = event.data;
    chatWindow.appendChild(messageItem);
    chatWindow.scrollTop = chatWindow.scrollHeight;  // Прокрутка вниз
};

function sendMessage() {
    const input = document.getElementById("messageInput");
    if (input.value !== '') {
        wsText.send(input.value);
        input.value = '';
        console.log('Сообщение отправлено:', input.value);
    }
}
