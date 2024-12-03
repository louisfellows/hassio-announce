"""Support to interact with a Music Player Daemon."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

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

    async def async_set_volume_level(self, volume: float) -> None:
        """Set volume level, range 0..1."""

    async def async_media_play(self) -> None:
        """Send play command."""

    async def async_media_pause(self) -> None:
        """Send pause command."""

    async def async_media_stop(self) -> None:
        """Send stop command."""

    async def async_media_previous_track(self) -> None:
        """Send previous track command."""

    async def async_media_next_track(self) -> None:
        """Send next track command."""

    async def async_media_seek(self, position: float) -> None:
        """Send seek command."""

    async def async_play_media(
        self, media_type: MediaType | str, media_id: str, **kwargs: Any
    ) -> None:
        """Play a piece of media."""
        data = {ATTR_MEDIA_CONTENT_TYPE: media_type, ATTR_MEDIA_CONTENT_ID: media_id}
        await self._async_call_service(SERVICE_PLAY_MEDIA, data, allow_override=True)

    async def async_volume_up(self) -> None:
        """Turn volume up for media player."""

    async def async_volume_down(self) -> None:
        """Turn volume down for media player."""

    async def async_media_play_pause(self) -> None:
        """Play or pause the media player."""

    async def async_select_sound_mode(self, sound_mode: str) -> None:
        """Select sound mode."""

    async def async_clear_playlist(self) -> None:
        """Clear players playlist."""

    async def async_set_shuffle(self, shuffle: bool) -> None:
        """Enable/disable shuffling."""

    async def async_set_repeat(self, repeat: RepeatMode) -> None:
        """Set repeat mode."""

    async def async_toggle(self) -> None:
        """Toggle the power on the media player."""

    async def _async_call_service(
        self, service_name, service_data=None, allow_override=False
    ):
        """Call either a specified or active child's service."""
