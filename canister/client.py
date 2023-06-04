#
# Copyright (c) 2023 TheRealKeto
# SPDX-License-Identifier: BSD-3-Clause
#

import aiohttp

from importlib import metadata
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from .objects import (
    CanisterPackage,
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
            "package": "jailbreak/package/",
            "search": "jailbreak/package/search"
        }

    @property
    def user_agent(self) -> str:
        http_agent = self.__http_agent.split()
        try:
            version = metadata.version(__package__)
        except metadata.PackageNotFoundError:
            version = "0.0.0-unknown"

        http_info = CanisterComponents(version, *http_agent)
        return http_info.user_agent

    async def __search_canister(
        self,
        endpoint: str,
        query: Optional[str] = None,
        *,
        params: Optional[Dict[str, Any]] = None
    ) -> CanisterAPIResponse:
        api_endpoint = self.__endpoints.get(endpoint)
        request_url = f"{self.__base}/{api_endpoint}"

        if query:
            request_url += query

        request_args: Dict[str, Any] = {
            "url": request_url,
            "params": params,
            "headers": {
                "User-Agent": self.user_agent,
                "content-type": "application/json"
            }
        }

        async with self.__session.get(**request_args) as resp:
            response = await resp.json()

        return CanisterAPIResponse(**response)

    async def search_packages(
        self,
        query: str,
        *,
        limit: Optional[int] = 250,
        page: Optional[int] = 1
    ) -> List[CanisterPackage]:
        params = {
            "q": query,
            "limit": limit,
            "page": page
        }
        resp = await self.__search_canister(
            "search", params=params
        )
        return [
            CanisterPackage(**package)
            for package in resp.data
        ]

    async def get_package(self, query: str) -> CanisterPackage:
        resp = await self.__search_canister("package", query)
        return CanisterPackage(**resp.data[0])

    async def close(self) -> None:
        if isinstance(self.__session, aiohttp.ClientSession):
            await self.__session.close()
