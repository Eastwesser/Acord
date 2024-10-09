const ws = new WebSocket("ws://localhost:8000/ws");

// Логирование для отладки
ws.onopen = () => console.log('Соединение установлено');
ws.onclose = () => console.log('Соединение закрыто');
ws.onerror = (error) => console.error('Ошибка WebSocket:', error);

ws.onmessage = function (event) {
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
        ws.send(input.value);
        input.value = '';
        console.log('Сообщение отправлено:', input.value); // Логирование
    }
}
