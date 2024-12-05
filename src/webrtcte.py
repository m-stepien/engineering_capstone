import asyncio
import json
import cv2
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiohttp import web
from aiortc.contrib.signaling import TcpSocketSignaling


class CameraStreamTrack(VideoStreamTrack):

    def __init__(self, track_id):
        super().__init__()  # Initialize the parent class
        self._track_id = track_id
        self._cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        self._frame_rate = 30  # Frame rate in FPS

    async def recv(self):

        ret, frame = self._cap.read()
        if not ret:
            raise Exception("Failed to capture frame")

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame


async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params['sdp'], type=params['type'])

    pc = RTCPeerConnection()

    video_track = CameraStreamTrack("video")
    pc.addTrack(video_track)

    @pc.on('iceconnectionstatechange')
    def on_ice_connection_state_change():
        if pc.iceConnectionState == 'failed':
            asyncio.create_task(pc.close())

    await pc.setRemoteDescription(offer)

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type='application/json',
        text=json.dumps({
            'sdp': pc.localDescription.sdp,
            'type': pc.localDescription.type
        })
    )


async def create_app():
    app = web.Application()
    app.add_routes([web.post('/offer', offer)])
    return app


if __name__ == '__main__':
    web.run_app(create_app(), host='0.0.0.0', port=8080)