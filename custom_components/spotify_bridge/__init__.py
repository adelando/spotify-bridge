import logging
from homeassistant.core import HomeAssistant, ServiceCall
from .streamer import SpotifyStreamer
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry):
    """Setup the Spotify Bridge integration."""
    
    # Initialize the streamer
    streamer = SpotifyStreamer(hass)
    await streamer.start()
    
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = streamer

    async def handle_sync_playback(call: ServiceCall):
        targets = call.data.get("targets", [])
        
        # Get the internal IP to tell speakers where to find the audio
        internal_ip = hass.config.internal_url or "http://your-ha-ip-here"
        stream_url = f"{internal_ip.rstrip('/')}:8081/spotify_bridge/stream"

        for entity_id in targets:
            _LOGGER.info("Casting Spotify stream to %s", entity_id)
            await hass.services.async_call(
                "media_player", "play_media",
                {
                    "entity_id": entity_id,
                    "media_content_id": stream_url,
                    "media_content_type": "music"
                }
            )

    hass.services.async_register(DOMAIN, "sync_playback", handle_sync_playback)
    return True

async def async_unload_entry(hass, entry):
    streamer = hass.data[DOMAIN][entry.entry_id]
    await streamer.stop()
    return True
