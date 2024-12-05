import json
import logging
import asyncio
from aiohttp import web
from aiortc import RTCConfiguration, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.signaling import TcpSocketSignaling

logging.basicConfig(level=logging.INFO)

pcs = set()

async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params['sdp'], type=params['type'])
    pc = RTCPeerConnection()

    @pc.on('iceconnectionstatechange')
    def on_ice_connection_state_change():
        if pc.iceConnectionState == 'failed':
            asyncio.create_task(pc.close())

    @pc.on('datachannel')
    def on_data_channel(channel):
        @channel.on('message')
        def on_message(message):
            print("Received:", message)

    @pc.on('track')
    def on_track(track):
        if track.kind == 'video':
            track.on('frame', lambda frame: print(frame))

    await pc.setRemoteDescription(offer)

    # Create an answer to the offer
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
    web.run_app(create_app(), host='0.0.0.0', port=8081)
