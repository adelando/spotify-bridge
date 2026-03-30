from homeassistant.components.media_player import MediaPlayerEntity, MediaPlayerEntityFeature
import spotipy

class SpotifyBridgePlayer(MediaPlayerEntity):
    def __init__(self, name, spotify_client):
        self._name = name
        self._sp = spotify_client
        self._sub_players = [] # List of entity_ids like media_player.living_room_airplay

    @property
    def supported_features(self):
        return (MediaPlayerEntityFeature.PLAY | MediaPlayerEntityFeature.PAUSE | 
                MediaPlayerEntityFeature.VOLUME_SET | MediaPlayerEntityFeature.GROUPING)

    async def async_play_media(self, media_type, media_id, **kwargs):
        # 1. Tell Spotify to start playing
        self._sp.start_playback(context_uri=media_id)
        
        # 2. Command all linked HA players to play the stream (if the device supports URIs)
        # Note: Some devices require a proxy URL which 'Music Assistant' provides.
        for player in self._sub_players:
            await self.hass.services.async_call(
                "media_player", "play_media",
                {"entity_id": player, "media_content_id": media_id, "media_content_type": "music"}
            )
