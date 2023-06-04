#
# Copyright (c) 2023 TheRealKeto
# SPDX-License-Identifier: BSD-3-Clause
#

import aiohttp

from importlib import metadata
from typing import (
    Any,
    Dict,
    Optional,
)

from .objects import (
    CanisterAPIResponse,
    CanisterComponents
)


class CanisterClient:
    def __init__(
        self,
        *,
        session: Optional[aiohttp.ClientSession] = None
    ):
        self.__base: str = "https://api.canister.me/v2"
        self.__http_agent = aiohttp.http.SERVER_SOFTWARE

        self.__session = session or aiohttp.ClientSession()

        # List of shorthand, supported endpoints
        self.__endpoints: Dict[str, str] = {
            "package_search": "jailbreak/package/search"
        }

    @property
    def user_agent(self):
        http_agent = self.__http_agent.split()
        try:
            version = metadata.version(__package__)
        except metadata.PackageNotFoundError:
            version = "0.0.0-unknown"

        http_info = CanisterComponents(version, *http_agent)
        return http_info.user_agent

    async def canister_request(
        self,
        endpoint: str,
        params: Dict[str, Any]
    ) -> CanisterAPIResponse:
        request_endpoint = self.__endpoints.get(endpoint)
        request_args: Dict[str, Any] = {
            "url": f"{self.__base}/{request_endpoint}",
            "params": params,
            "headers": {"User-Agent": self.user_agent}
        }

        async with self.__session.get(**request_args) as resp:
            response = await resp.json()

        return CanisterAPIResponse(**response)

    async def close(self) -> None:
        if isinstance(self.__session, aiohttp.ClientSession):
            await self.__session.close()
