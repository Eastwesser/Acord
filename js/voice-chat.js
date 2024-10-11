const wsVoice = new WebSocket("ws://localhost:8000/ws/voice");

wsVoice.onopen = function () {
    console.log("Подключение к голосовому чату установлено.");
    document.getElementById("connect-button").textContent = "Подключено";
};

wsVoice.onmessage = async function (event) {
    const message = JSON.parse(event.data);
    console.log("Получено сообщение:", message);
    // Обработка ICE-кандидатов и офферов
};

async function startVoiceChat() { // Declare the function as async
    try {
        localStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        peerConnection = new RTCPeerConnection({
            iceServers: [{ urls: "stun:stun.l.google.com:19302" }]
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

        peerConnection.ontrack = event => {
            const remoteAudio = new Audio();
            remoteAudio.srcObject = event.streams[0];
            remoteAudio.play();
        };

        const offer = await peerConnection.createOffer();
        await peerConnection.setLocalDescription(offer);

        wsVoice.send(JSON.stringify({
            type: "offer",
            offer: offer
        }));
    } catch (error) {
        console.error("Ошибка в голосовом чате:", error);
    }
}
