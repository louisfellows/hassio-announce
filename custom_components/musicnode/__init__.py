"""The MusicNode integration."""
from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

LOGGER = logging.getLogger(__name__)

# For your initial PR, limit it to 1 platform.
PLATFORMS: list[Platform] = [Platform.MEDIA_PLAYER]

def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up a skeleton component."""
    
    hass.states.set('hassio_announce.Idle', 'Idle')

    # Return boolean to indicate that initialization was successfully.
    return True
