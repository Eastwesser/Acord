let localStream;
let peerConnection;

const wsVoice = new WebSocket("ws://localhost:8000/ws/voice");

// Конфигурация STUN-сервера для WebRTC
const configuration = {
    iceServers: [{urls: "stun:stun.l.google.com:19302"}]
};

wsVoice.onmessage = async function (event) {
    const message = JSON.parse(event.data);

    if (message.type === "offer") {
        await createAnswer(message.offer);
    } else if (message.type === "answer") {
        await peerConnection.setRemoteDescription(new RTCSessionDescription(message.answer));
    } else if (message.type === "ice-candidate") {
        await peerConnection.addIceCandidate(new RTCIceCandidate(message.candidate));
    }
};

async function startVoiceChat() {
    localStream = await navigator.mediaDevices.getUserMedia({audio: true});
    peerConnection = new RTCPeerConnection(configuration);

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

async function createAnswer(offer) {
    await peerConnection.setRemoteDescription(new RTCSessionDescription(offer));
    const answer = await peerConnection.createAnswer();
    await peerConnection.setLocalDescription(answer);

    wsVoice.send(JSON.stringify({
        type: "answer",
        answer: answer
    }));
}
