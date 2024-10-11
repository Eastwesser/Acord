let localStream;
let peerConnection;
const wsVoice = new WebSocket("ws://localhost:8000/ws/voice");

wsVoice.onopen = function () {
    console.log("Подключение к голосовому чату установлено.");
    document.getElementById("voiceChatButton").textContent = "Подключено";
};

wsVoice.onmessage = async function (event) {
    const message = JSON.parse(event.data);

    if (message.type === 'offer') {
        await handleOffer(message.offer);
    } else if (message.type === 'ice-candidate') {
        await handleIceCandidate(message.candidate);
    }
};

async function startVoiceChat() {
    localStream = await navigator.mediaDevices.getUserMedia({audio: true});
    peerConnection = new RTCPeerConnection({
        iceServers: [{urls: "stun:stun.l.google.com:19302"}]
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
}

async function handleOffer(offer) {
    await peerConnection.setRemoteDescription(new RTCSessionDescription(offer));
    const answer = await peerConnection.createAnswer();
    await peerConnection.setLocalDescription(answer);

    wsVoice.send(JSON.stringify({
        type: "answer",
        answer: answer
    }));
}

async function handleIceCandidate(candidate) {
    try {
        await peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
    } catch (error) {
        console.error('Ошибка добавления ICE кандидата:', error);
    }
}
