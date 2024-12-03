"""Support to interact with a Music Player Daemon."""
from __future__ import annotations

from datetime import datetime
import logging
import requests
from typing import Any
import voluptuous as vol

from homeassistant.components import media_source
import homeassistant.helpers.config_validation as cv

from homeassistant.components.media_player import (  # ATTR_APP_ID,; ATTR_APP_NAME,; ATTR_INPUT_SOURCE_LIST,; ATTR_MEDIA_ALBUM_ARTIST,; ATTR_MEDIA_CHANNEL,; ATTR_MEDIA_EPISODE,; ATTR_MEDIA_PLAYLIST,; ATTR_MEDIA_SEASON,; ATTR_MEDIA_SERIES_TITLE,; ATTR_MEDIA_TRACK,; ATTR_SOUND_MODE_LIST,; DEVICE_CLASSES_SCHEMA,; PLATFORM_SCHEMA,; BrowseMedia,; async_process_play_media_url,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
    MediaType,
    RepeatMode,
    async_process_play_media_url
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, State
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import DiscoveryInfoType
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.components.media_player import PLATFORM_SCHEMA

_LOGGER = logging.getLogger(__name__)

SUPPORT = ( MediaPlayerEntityFeature.PLAY_MEDIA )

STATES_ORDER = [
    MediaPlayerState.OFF,
    MediaPlayerState.IDLE,
    MediaPlayerState.PLAYING
]
STATES_ORDER_LOOKUP = {state: idx for idx, state in enumerate(STATES_ORDER)}
STATES_ORDER_IDLE = STATES_ORDER_LOOKUP[MediaPlayerState.IDLE]

STRING_TO_STATE = {
    "off": MediaPlayerState.OFF,
    "idle": MediaPlayerState.IDLE,
    "playing": MediaPlayerState.PLAYING
}

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_NAME): cv.string
})

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the platform."""
    
    host = config[CONF_HOST]
    name = config[CONF_NAME]
    
    add_entities([AnnouncerMediaDevice(hass, host, name)], True)


class AnnouncerMediaDevice(MediaPlayerEntity):
    """Representation of a Number of Mudia Players server."""

    _attr_media_content_type = MediaType.MUSIC

    # pylint: disable=no-member
    def __init__(self, hass, host, name):
        """Initialize the device."""
        self.hass = hass
        self._attr_unique_id = name
        self._state = MediaPlayerState.IDLE
        self._name = name
        self.last_announcement_media_id = ""
        self.api_url = host

    async def async_update(self) -> None:
        """Get the latest data and update the state."""
        return


    def _get_state_from_string(self, value: str) -> MediaPlayerState:
        if value in STRING_TO_STATE:
            return STRING_TO_STATE[value]

        return MediaPlayerState.OFF

    @property
    def _current_state(self) -> State:
        return self._state

    @property
    def name(self) -> str | None:
        """Return the name of the device."""
        return self._name

    @property
    def state(self) -> MediaPlayerState:
        """Return the media state."""
        return self._get_state_from_string(self._state)

    @property
    def is_volume_muted(self) -> bool | None:
        """Boolean if volume is currently muted."""
        return False

    @property
    def media_content_id(self) -> str | None:
        """Return the content ID of current playing media."""
        return self.last_announcement_media_id

    @property
    def media_duration(self) -> int | None:
        """Return the duration of current playing media in seconds."""
        return 1

    @property
    def media_position(self) -> int | None:
        """Position of current playing media in seconds."""
        return 1

    @property
    def media_position_updated_at(self) -> datetime | None:
        """Last valid time of media position."""
        return datetime.now()

    @property
    def media_title(self) -> str | None:
        """Return the title of current playing media."""
        return "Announcement"

    @property
    def media_artist(self) -> str | None:
        """Return the artist of current playing media (Music track only)."""
        return "Hassio"

    @property
    def media_album_name(self) -> str | None:
        """Return the album of current playing media (Music track only)."""
        return "Hassio"

    @property
    def media_image_hash(self) -> str | None:
        """Hash value for media image."""
        return None

    @property
    def volume_level(self) -> float | None:
        """Return the volume level."""
        return 100

    @property
    def supported_features(self) -> MediaPlayerEntityFeature:
        """Flag media player features that are supported."""
        supported = SUPPORT
        return supported

    @property
    def source(self) -> str | None:
        """Name of the current input source."""
        return "Announcer"

    @property
    def source_list(self) -> list[str] | None:
        """Return the list of available input sources."""
        return ["Announcer"]

    @property
    def repeat(self) -> RepeatMode:
        """Return current repeat mode."""
        return None

    @property
    def shuffle(self) -> bool | None:
        """Boolean if shuffle is enabled."""
        return False

    @property
    def media_image_url(self) -> str | None:
        """Image url of current playing media."""
        return "/www/hassio.png"

    async def async_play_media(
        self, media_type: MediaType | str, media_id: str, **kwargs: Any
    ) -> None:
        """Play a piece of media."""
        
        logging.info(media_id)
        
        if media_source.is_media_source_id(media_id):
            play_item = await media_source.async_resolve_media(
                self.hass, media_id, self.entity_id
            )

            file_name = async_process_play_media_url(self.hass, play_item.url)
            url = f"{self.api_url}/"

            self._state = MediaPlayerState.PLAYING
            self.hass.async_add_executor_job(self.send_play_request, url, file_name)
            self._state = MediaPlayerState.IDLE

    def send_play_request(self, url, file_name):
        body = {'uri': file_name}
        logging.info(body)
        x = requests.post(url, json = body)
        logging.info(x)