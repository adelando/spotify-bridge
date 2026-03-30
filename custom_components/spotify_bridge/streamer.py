import logging
import asyncio
from aiohttp import web
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

class SpotifyStreamer:
    def __init__(self, hass: HomeAssistant):
        self.hass = hass
        self.app = web.Application()
        self.app.router.add_get("/spotify_bridge/stream", self.stream_handle)
        self._runner = None
        self._audio_buffer = None # This will be fed by librespot

    async def start(self):
        self._runner = web.AppRunner(self.app)
        await self._runner.setup()
        # Listen on all interfaces so speakers can reach it
        site = web.TCPSite(self._runner, "0.0.0.0", 8081)
        await site.start()
        _LOGGER.info("Spotify Audio Streamer active on port 8081")

    async def stream_handle(self, request):
        response = web.StreamResponse(
            status=200,
            headers={'Content-Type': 'audio/mpeg', 'Cache-Control': 'no-cache'}
        )
        await response.prepare(request)
        
        # This is where the magic happens: 
        # You pipe the output from your librespot session to the response
        try:
            while True:
                # Placeholder for the actual buffer data
                # await response.write(chunk)
                await asyncio.sleep(1)
        except Exception:
            _LOGGER.debug("Speaker disconnected from stream")
        return response

    async def stop(self):
        if self._runner:
            await self._runner.cleanup()
