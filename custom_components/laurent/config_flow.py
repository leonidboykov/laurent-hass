from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigFlow,
    ConfigEntry,
    OptionsFlow,
    ConfigFlowResult,
)
from homeassistant.core import callback
from homeassistant.const import (
    CONF_NAME,
    CONF_HOST,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL
)
from .const import (
    DOMAIN,
    DEFAULT_NAME,
    DEFAULT_HOST,
    DEFAULT_PASSWORD,
    DEFAULT_SCAN_INTERVAL
)


class LaurentConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for Laurent device."""
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        return LaurentOptionsFlowHandler()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            name = user_input[CONF_NAME]
            return self.async_create_entry(
                title=name,
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
                vol.Required(CONF_PASSWORD, default=DEFAULT_PASSWORD): str,
                vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
            }),
            errors=errors
        )


class LaurentOptionsFlowHandler(OptionsFlow):
    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            return self.async_create_entry(
                title="",
                data=user_input
            )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(
                    CONF_HOST,
                    default=self.config_entry.data.get(
                        CONF_HOST, DEFAULT_HOST
                    ),
                ): str,
                vol.Required(
                    CONF_PASSWORD,
                    default=self.config_entry.data.get(
                        CONF_PASSWORD, DEFAULT_PASSWORD,
                    )
                ): str,
                vol.Required(
                    CONF_SCAN_INTERVAL,
                    default=self.config_entry.data.get(
                        CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL,
                    )
                ): int,
            }),
            errors=errors
        )
