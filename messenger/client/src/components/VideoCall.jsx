import React, { useEffect, useRef, useState } from 'react';
import { useParams } from 'react-router-dom';
import io from 'socket.io-client';
import Chat from './Chat';
import { Button, Container, Box } from '@mui/material';

let socket;
let peerConnection;
let localStream;

const configuration = {
  iceServers: [
    { urls: 'stun:stun.l.google.com:19302' },
    {
      urls: `turn:${process.env.REACT_APP_TURN_SERVER}:3478`,
      username: process.env.REACT_APP_TURN_USERNAME,
      credential: process.env.REACT_APP_TURN_PASSWORD
    }
  ]
};

export default function VideoCall() {
  const { roomId } = useParams();
  const [isVideoEnabled, setIsVideoEnabled] = useState(true);
  const [isAudioEnabled, setIsAudioEnabled] = useState(true);
  const localVideoRef = useRef();
  const remoteVideoRef = useRef();

  useEffect(() => {
    const token = localStorage.getItem('token');
    socket = io('http://localhost:3001', { transports: ['websocket'] });

    socket.on('disconnect', () => {
      console.log('Disconnected, attempting to reconnect...');
      setTimeout(() => {
        socket.connect();
      }, 3000);
    });

    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
      .then(stream => {
        localStream = stream;
        localVideoRef.current.srcObject = stream;

        socket.emit('join_room', { roomId, token });

        socket.on('user_joined', async () => {
          createPeerConnection();
          const offer = await peerConnection.createOffer();
          await peerConnection.setLocalDescription(offer);
          socket.emit('signal', { to: null, signal: offer });
        });

        socket.on('signal', async (data) => {
          if (!peerConnection) createPeerConnection();

          if (data.signal.type === 'offer') {
            await peerConnection.setRemoteDescription(data.signal);
            const answer = await peerConnection.createAnswer();
            await peerConnection.setLocalDescription(answer);
            socket.emit('signal', { to: data.from, signal: answer });
          } else if (data.signal.type === 'answer') {
            await peerConnection.setRemoteDescription(data.signal);
          } else if (data.signal.candidate) {
            await peerConnection.addIceCandidate(data.signal);
          }
        });
      });

    const createPeerConnection = () => {
      peerConnection = new RTCPeerConnection(configuration);

      localStream.getTracks().forEach(track => {
        peerConnection.addTrack(track, localStream);
      });

      peerConnection.onicecandidate = (event) => {
        if (event.candidate) {
          socket.emit('signal', { to: null, signal: event.candidate });
        }
      };

      peerConnection.ontrack = (event) => {
        remoteVideoRef.current.srcObject = event.streams[0];
      };
    };

    return () => socket.close();
  }, [roomId]);

  const toggleCamera = () => {
    const videoTrack = localStream.getVideoTracks()[0];
    if (videoTrack) {
      videoTrack.enabled = !videoTrack.enabled;
      setIsVideoEnabled(videoTrack.enabled);
    }
  };

  const toggleMicrophone = () => {
    const audioTrack = localStream.getAudioTracks()[0];
    if (audioTrack) {
      audioTrack.enabled = !audioTrack.enabled;
      setIsAudioEnabled(audioTrack.enabled);
    }
  };

  return (
    <Container maxWidth={false} style={{ background: '#2e2e2e', height: '100vh', padding: '20px' }}>
      <Box display="flex" justifyContent="space-between" mb={2}>
        <video ref={localVideoRef} autoPlay muted style={{ width: '45%', height: '40%', border: '2px solid gold' }} />
        <video ref={remoteVideoRef} autoPlay style={{ width: '45%', height: '40%', border: '2px solid gold' }} />
      </Box>

      <Box display="flex" justifyContent="center" mb={2}>
        <Button
          variant="contained"
          onClick={toggleMicrophone}
          style={{
            backgroundColor: isAudioEnabled ? '#4CAF50' : '#f44336',
            color: 'white',
            padding: '10px 20px',
            borderRadius: '30px',
            fontWeight: 'bold',
            textTransform: 'none',
            marginRight: '10px'
          }}
        >
          {isAudioEnabled ? 'Disable Mic' : 'Enable Mic'}
        </Button>
        <Button
          variant="contained"
          onClick={toggleCamera}
          style={{
            backgroundColor: isVideoEnabled ? '#4CAF50' : '#f44336',
            color: 'white',
            padding: '10px 20px',
            borderRadius: '30px',
            fontWeight: 'bold',
            textTransform: 'none'
          }}
        >
          {isVideoEnabled ? 'Disable Camera' : 'Enable Camera'}
        </Button>
      </Box>

      <Chat socket={socket} roomId={roomId} />
    </Container>
  );
}