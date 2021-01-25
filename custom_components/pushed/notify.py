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

ATTR_ATTACHMENT = "attachment"
ATTR_URL = "url"
ATTR_URL_TITLE = "url_title"
ATTR_PRIORITY = "priority"
ATTR_RETRY = "retry"
ATTR_SOUND = "sound"
ATTR_HTML = "html"
ATTR_CALLBACK_URL = "callback_url"
ATTR_EXPIRE = "expire"
ATTR_TIMESTAMP = "timestamp"

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

        # Extract params from data dict
        title = kwargs.get(ATTR_TITLE, ATTR_TITLE_DEFAULT)
        data = dict(kwargs.get(ATTR_DATA) or {})
        url = data.get(ATTR_URL)
        url_title = data.get(ATTR_URL_TITLE)
        priority = data.get(ATTR_PRIORITY)
        retry = data.get(ATTR_RETRY)
        expire = data.get(ATTR_EXPIRE)
        callback_url = data.get(ATTR_CALLBACK_URL)
        timestamp = data.get(ATTR_TIMESTAMP)
        sound = data.get(ATTR_SOUND)
        html = 1 if data.get(ATTR_HTML, False) else 0

        image = data.get(ATTR_ATTACHMENT)
        # Check for attachment
        if image is not None:
            # Only allow attachments from whitelisted paths, check valid path
            if self._hass.config.is_allowed_path(data[ATTR_ATTACHMENT]):
                # try to open it as a normal file.
                try:
                    file_handle = open(data[ATTR_ATTACHMENT], "rb")
                    # Replace the attachment identifier with file object.
                    image = file_handle
                except OSError as ex_val:
                    _LOGGER.error(ex_val)
                    # Remove attachment key to send without attachment.
                    image = None
            else:
                _LOGGER.error("Path is not whitelisted")
                # Remove attachment key to send without attachment.
                image = None

        targets = kwargs.get(ATTR_TARGET)

        if not isinstance(targets, list):
            targets = [targets]

        for target in targets:
            try:
                requests.post("https://api.pushed.co/1/push", data={
                    "app_key": self._app_key,
                    "app_secret": self._app_secret,
                    "target_type": "app",
                    "content": message,
                })
            except ValueError as val_err:
                _LOGGER.error(val_err)
