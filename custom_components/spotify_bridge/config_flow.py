import voluptuous as vol
from homeassistant import config_entries
from .const import CONF_CLIENT_ID, CONF_CLIENT_SECRET, DEFAULT_NAME, DOMAIN

class SpotifyBridgeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Spotify Universal Bridge."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Initial step to start the setup."""
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        if user_input is not None:
            return self.async_create_entry(
                title=DEFAULT_NAME,
                data={
                    CONF_CLIENT_ID: user_input[CONF_CLIENT_ID].strip(),
                    CONF_CLIENT_SECRET: user_input[CONF_CLIENT_SECRET].strip(),
                },
            )

        return self.async_show_form(
            step_id="user",
            description_placeholders={
                "link": "https://developer.spotify.com/dashboard",
            },
            data_schema=vol.Schema({
                vol.Required(CONF_CLIENT_ID): str,
                vol.Required(CONF_CLIENT_SECRET): str,
            }),
        )
