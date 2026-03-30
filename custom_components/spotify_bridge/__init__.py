import logging
from urllib.parse import urlsplit
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.network import NoURLAvailableError, get_url
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

        # Determine a reachable base URL for media players on the local network.
        try:
            base_url = get_url(hass, allow_internal=True, allow_external=False)
        except NoURLAvailableError:
            _LOGGER.error(
                "Could not determine Home Assistant internal URL. "
                "Configure Internal URL in Settings > System > Network."
            )
            return

        parsed_base_url = urlsplit(base_url)
        if parsed_base_url.hostname is None:
            _LOGGER.error("Internal URL is invalid: %s", base_url)
            return
        stream_url = (
            f"{parsed_base_url.scheme}://{parsed_base_url.hostname}:8081"
            "/spotify_bridge/stream"
        )

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
    hass.data[DOMAIN].pop(entry.entry_id)
    if not hass.data[DOMAIN]:
        hass.services.async_remove(DOMAIN, "sync_playback")
    return True
