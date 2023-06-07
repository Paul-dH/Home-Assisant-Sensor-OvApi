import logging

import voluptuous as vol
from homeassistant.const import SERVICE_RELOAD, Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.reload import async_reload_integration_platforms
from homeassistant.helpers.typing import ConfigType
from typing import Final

_LOGGER = logging.getLogger(__name__)

DOMAIN: Final = "ovapi"
    
PLATFORMS = [
    Platform.SENSOR,
]

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the platforms."""
    # Print startup message
    _LOGGER.info("ovapi component is starting...")

    # await async_setup_reload_service(hass, DOMAIN, PLATFORMS)

    component = EntityComponent(_LOGGER, DOMAIN, hass)

    async def reload_service_handler(service: ServiceCall) -> None:
        """Reload all sensors from config."""
        print("+++++++++++++++++++++++++")
        print(component)
        # print(hass.data[DATA_INSTANCES]["sensors"].entities[0])

        await async_reload_integration_platforms(hass, DOMAIN, PLATFORMS)

    hass.services.async_register(
        DOMAIN, SERVICE_RELOAD, reload_service_handler, schema=vol.Schema({})
    )

    return True
