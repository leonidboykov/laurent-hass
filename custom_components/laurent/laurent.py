"""Client for Laurent."""

import aiohttp
from json import JSONDecoder


class LaurentData:
    firmware: str | None
    serial_number: str | None
    mac: str | None
    model: str | None
    states: list[bool] | None

    def __init__(self, input) -> None:
        # object_hook is called recursively for JSONDecoder.
        if 'fw' in input:
            self.firmware = input.get("fw")
            self.serial_number = input.get("sn")
            self.mac = input.get("mac")
            self.model = self._model_by_fw(input.get("fw"))
            self.states = list(bool(int(x)) for x in input.get("rele"))

    def _model_by_fw(self, fw: str) -> str:
        if fw.startswith("LR"):
            return "Laurent-112"
        elif fw.startswith("LX"):
            return "Laurent-128"
        elif fw.startswith("L"):
            return "Laurent-2"
        elif fw.startswith("L5"):
            return "Laurent-5"
        elif fw.startswith("G5"):
            return "Laurent-5G"
        else:
            return "Unknown Model"


class Laurent:
    def __init__(self, host: str, password: str) -> None:
        self.host = host
        self.password = password

    async def fetch_info(self) -> LaurentData:
        params = {"psw": self.password}
        async with aiohttp.ClientSession(self.host) as session:
            async with session.get("/json_sensor.cgi", params=params) as resp:
                # TODO: Add error handling.
                return await resp.json(
                    content_type="text/html",
                    loads=JSONDecoder(object_hook=LaurentData).decode,
                )

    async def turn_on(self, idx: int) -> bool:
        return await self.exec_command(f"REL,{idx},1")

    async def turn_off(self, idx: int) -> bool:
        return await self.exec_command(f"REL,{idx},0")

    async def exec_command(self, cmd: str) -> bool:
        params = {"psw": self.password, "cmd": cmd}
        async with aiohttp.ClientSession(self.host) as session:
            async with session.get("/cmd.cgi", params=params) as resp:
                ret = await resp.text()
                return ret.startswith("#REL,OK")
