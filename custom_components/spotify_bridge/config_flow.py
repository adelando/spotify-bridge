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
        """Return logger."""
        return _LOGGER

    async def async_step_user(self, user_input=None):
        """Initial step to start the setup."""
        # This check ensures we don't start the flow if it's already configured
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        if user_input is not None:
            # You can add logic here to store the client_id/secret globally 
            # if they aren't already in your configuration.yaml
            return await self.async_step_pick_implementation()
        
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("client_id"): str,
                vol.Required("client_secret"): str,
            })
        )

    async def async_oauth_create_entry(self, data):
        """Create the config entry after successful OAuth."""
        return self.async_create_entry(title="Spotify Bridge", data=data)
