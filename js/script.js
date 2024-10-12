const themeToggle = document.getElementById('themeToggle');
const body = document.body;

// Устанавливаем начальную тему
if (localStorage.getItem('theme') === 'dark') {
    body.classList.add('dark-theme');
    themeToggle.checked = true;
}

// Слушаем изменения переключателя
themeToggle.addEventListener('change', () => {
    body.classList.toggle('dark-theme');

    // Сохраняем выбранную тему в localStorage
    if (body.classList.contains('dark-theme')) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }
});

// WebSocket для текстового чата
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
    const nickname = document.getElementById('nickname').value || "Anonymous"; // Используем ник из поля ввода
    const message = messageInput.value.trim();

    if (message) {
        const messageData = {nickname: nickname, text: message};
        wsText.send(JSON.stringify(messageData));
        messageInput.value = '';
    }
}

// WebSocket для голосового чата
let localStream;
let peerConnection;

const wsVoice = new WebSocket("ws://localhost:8000/ws/voice");

wsVoice.onopen = function () {
    console.log("Подключение к голосовому чату установлено.");
};

wsVoice.onmessage = async function (event) {
    const data = JSON.parse(event.data);

    if (data.type === 'offer') {
        await peerConnection.setRemoteDescription(new RTCSessionDescription(data.offer));
        const answer = await peerConnection.createAnswer();
        await peerConnection.setLocalDescription(answer);
        wsVoice.send(JSON.stringify({type: 'answer', answer: answer}));
    } else if (data.type === 'answer') {
        await peerConnection.setRemoteDescription(new RTCSessionDescription(data.answer));
    } else if (data.type === 'ice-candidate') {
        await peerConnection.addIceCandidate(new RTCIceCandidate(data.candidate));
    }
};

async function toggleVoiceChat() {
    if (!localStream) {
        localStream = await navigator.mediaDevices.getUserMedia({audio: true});

        peerConnection = new RTCPeerConnection({
            iceServers: [{urls: 'stun:stun.l.google.com:19302'}]
        });

        localStream.getTracks().forEach(track => {
            peerConnection.addTrack(track, localStream);
        });

        peerConnection.onicecandidate = event => {
            if (event.candidate) {
                wsVoice.send(JSON.stringify({
                    type: "ice-candidate",
                    candidate: event.candidate
                }));
            }
        };

        const offer = await peerConnection.createOffer();
        await peerConnection.setLocalDescription(offer);

        wsVoice.send(JSON.stringify({
            type: "offer",
            offer: offer
        }));

        document.getElementById("voiceChatButton").textContent = "Отключиться";

    } else {
        // Отключение от голосового чата
        localStream.getTracks().forEach(track => track.stop());
        localStream = null;

        wsVoice.close();

        document.getElementById("voiceChatButton").textContent = "Подключиться к голосовому чату";
    }
}