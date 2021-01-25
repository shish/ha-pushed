"""Pushed.co platform for notify component."""
import logging
import requests
import voluptuous as vol

from homeassistant.components.notify import (
    ATTR_DATA,
    ATTR_TARGET,
    ATTR_TITLE,
    ATTR_TITLE_DEFAULT,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_APP_KEY = "app_key"
CONF_APP_SECRET = "app_secret"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Required(CONF_APP_KEY): cv.string, vol.Required(CONF_APP_SECRET): cv.string}
)


def get_service(hass, config, discovery_info=None):
    """Get the Pushover notification service."""
    return PushedNotificationService(
        hass, config[CONF_APP_KEY], config[CONF_APP_SECRET]
    )


class PushedNotificationService(BaseNotificationService):
    """Implement the notification service for Pushover."""

    def __init__(self, hass, app_key, app_secret):
        """Initialize the service."""
        self._hass = hass
        self._app_key = app_key
        self._app_secret = app_secret

    def send_message(self, message="", **kwargs):
        """Send a message to a user."""
        title = kwargs.get("title")
        target = data.get("target")
        url = data.get("url")
        kwargs = {}
        if url:
            kwargs["content_type"] = "url"
            kwargs["content_extra"] = url

        if target:
            if "@" in target:
                self._send_to(target_type="email", email=target, **kwargs)
            else:
                self._send_to(target_type="channel", target_alias=target, **kwargs)
        else:
            self._send_to(target_type="app", **kwargs)

    def _send_to(self, **kwargs):
        try:
            data = {
                "app_key": self._app_key,
                "app_secret": self._app_secret,
                "content": message,
            }
            data.update(kwargs)
            requests.post("https://api.pushed.co/1/push", data=data)
        except ValueError as val_err:
            _LOGGER.error(val_err)

