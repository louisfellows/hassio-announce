"""Support to interact with a Music Player Daemon."""
from __future__ import annotations

from datetime import datetime
import logging
import requests
from typing import Any

from homeassistant.components import media_source

from homeassistant.components.media_player import (  # ATTR_APP_ID,; ATTR_APP_NAME,; ATTR_INPUT_SOURCE_LIST,; ATTR_MEDIA_ALBUM_ARTIST,; ATTR_MEDIA_CHANNEL,; ATTR_MEDIA_EPISODE,; ATTR_MEDIA_PLAYLIST,; ATTR_MEDIA_SEASON,; ATTR_MEDIA_SERIES_TITLE,; ATTR_MEDIA_TRACK,; ATTR_SOUND_MODE_LIST,; DEVICE_CLASSES_SCHEMA,; PLATFORM_SCHEMA,; BrowseMedia,; async_process_play_media_url,
    ATTR_INPUT_SOURCE,
    ATTR_MEDIA_ALBUM_NAME,
    ATTR_MEDIA_ARTIST,
    ATTR_MEDIA_CONTENT_ID,
    ATTR_MEDIA_CONTENT_TYPE,
    ATTR_MEDIA_DURATION,
    ATTR_MEDIA_POSITION,
    ATTR_MEDIA_POSITION_UPDATED_AT,
    ATTR_MEDIA_REPEAT,
    ATTR_MEDIA_SEEK_POSITION,
    ATTR_MEDIA_SHUFFLE,
    ATTR_MEDIA_TITLE,
    ATTR_MEDIA_VOLUME_LEVEL,
    ATTR_MEDIA_VOLUME_MUTED,
    ATTR_SOUND_MODE,
    DOMAIN,
    SERVICE_CLEAR_PLAYLIST,
    SERVICE_PLAY_MEDIA,
    SERVICE_SELECT_SOUND_MODE,
    SERVICE_SELECT_SOURCE,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
    MediaType,
    RepeatMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (  # ATTR_SUPPORTED_FEATURES,; CONF_DEVICE_CLASS,; CONF_HOST,; CONF_NAME,; CONF_PASSWORD,; CONF_PORT,; CONF_STATE,; CONF_STATE_TEMPLATE,; CONF_UNIQUE_ID,; EVENT_HOMEASSISTANT_START,; STATE_UNAVAILABLE,; STATE_UNKNOWN,
    ATTR_ENTITY_ID,
    ATTR_ENTITY_PICTURE,
    SERVICE_MEDIA_NEXT_TRACK,
    SERVICE_MEDIA_PAUSE,
    SERVICE_MEDIA_PLAY,
    SERVICE_MEDIA_PLAY_PAUSE,
    SERVICE_MEDIA_PREVIOUS_TRACK,
    SERVICE_MEDIA_SEEK,
    SERVICE_MEDIA_STOP,
    SERVICE_REPEAT_SET,
    SERVICE_SHUFFLE_SET,
    SERVICE_TOGGLE,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    SERVICE_VOLUME_DOWN,
    SERVICE_VOLUME_MUTE,
    SERVICE_VOLUME_SET,
    SERVICE_VOLUME_UP,
    STATE_ON,
)
from homeassistant.core import HomeAssistant, State
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import DiscoveryInfoType

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


async def async_setup_entry(
    hass: HomeAssistant,
    config: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the platform."""
    async_add_entities([AnnouncerMediaDevice(hass)], True)




class AnnouncerMediaDevice(MediaPlayerEntity):
    """Representation of a Number of Mudia Players server."""

    _attr_media_content_type = MediaType.MUSIC

    # pylint: disable=no-member
    def __init__(self, hass):
        """Initialize the device."""
        self.hass = hass
        self._attr_unique_id = "announcer"
        self.state = MediaPlayerState.IDLE
        self.name = "Announcer"
        self.last_announcement_media_id = ""
        self.api_url = "http://192.168.1.204:5000"

    async def async_update(self) -> None:
        """Get the latest data and update the state."""
        return


    def _get_state_from_string(self, value: str) -> MediaPlayerState:
        if value in STRING_TO_STATE:
            return STRING_TO_STATE[value]

        return MediaPlayerState.OFF

    @property
    def _current_state(self) -> State:
        return self.state

    @property
    def name(self) -> str | None:
        """Return the name of the device."""
        return self.name

    @property
    def state(self) -> MediaPlayerState:
        """Return the media state."""
        return self._get_state_from_string(self.state)

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
        return datetime.timezone.utc

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
            media = await media_source.async_resolve_media(
                self.hass, media_id, self.entity_id
            )
            file_name = media.url[media.url.rindex("/") : media.url.rindex(".")]
            
            logging.info(file_name)
            
            url = f"{self.api_url}/"
            body = {'url': file_name}

            self.state = MediaPlayerState.PLAYING
            x = requests.post(url, json = body)
            logging.info(x)
            self.state = MediaPlayerState.IDLE