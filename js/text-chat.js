const wsText = new WebSocket("ws://localhost:8000/ws/text");

wsText.onopen = () => {
    console.log('Соединение с текстовым чатом установлено');
};

wsText.onmessage = (event) => {
    const messageData = JSON.parse(event.data); // Парсим JSON
    const chatWindow = document.getElementById('chat-window');
    const messageItem = document.createElement('div');
    messageItem.classList.add('message');
    messageItem.textContent = messageData.text; // Используем текст из парсенного объекта
    chatWindow.appendChild(messageItem);
    chatWindow.scrollTop = chatWindow.scrollHeight;
};

function sendMessage() {
    const input = document.getElementById("messageInput");
    if (input.value !== '') {
        const message = {text: input.value}; // Оборачиваем текст в объект
        wsText.send(JSON.stringify(message)); // Преобразуем в строку JSON
        input.value = '';
    }
}
