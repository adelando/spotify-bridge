import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import config_entry_oauth2_flow
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class SpotifyBridgeConfigFlow(config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN):
    """Handle a config flow for Spotify Universal Bridge."""
    
    DOMAIN = DOMAIN
    VERSION = 1

    @property
    def logger(self) -> logging.Logger:
        return _LOGGER

    async def async_step_user(self, user_input=None):
        """Initial step to start the setup."""
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        if user_input is not None:
            return await self.async_step_pick_implementation()
        
        # This text appears in the UI to guide the user
        return self.async_show_form(
            step_id="user",
            description_placeholders={
                "link": "https://developer.spotify.com/dashboard"
            },
            data_schema=vol.Schema({
                vol.Required("client_id"): str,
                vol.Required("client_secret"): str,
            })
        )

    async def async_oauth_create_entry(self, data):
        return self.async_create_entry(title="Spotify Bridge", data=data)
