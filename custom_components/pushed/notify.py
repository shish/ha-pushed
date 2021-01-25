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
        target = kwargs.get("target")
        data = dict(kwargs.get("data") or {})
        url = data.get("url")
        
        # Full list of possible args at https://about.pushed.co/docs/api
        msg_args = {
            "app_key": self._app_key,
            "app_secret": self._app_secret,
            "content": message,
            "target_type": "app",
        }
        if url:
            msg_args["content_type"] = "url"
            msg_args["content_extra"] = url
        if target:
            if "@" in target:
                msg_args["target_type"] = "email"
                msg_args["email"] = target
            else:
                msg_args["target_type"] = "channel"
                msg_args["target_alias"] = target

        try:
            requests.post("https://api.pushed.co/1/push", data=msg_args)
        except ValueError as val_err:
            _LOGGER.error(val_err)
