#
# Copyright (c) 2023 TheRealKeto
# SPDX-License-Identifier: BSD-3-Clause
#

import aiohttp

from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from .objects import (
    Package,
    Repository,
    APIResponse,
    CanisterComponents
)


class CanisterClient:
    def __init__(
        self,
        *,
        session: Optional[aiohttp.ClientSession] = None
    ):
        self.__base = "https://api.canister.me/v2"
        self.__http_agent = aiohttp.http.SERVER_SOFTWARE
        self.__session = session or aiohttp.ClientSession()

        # List of shorthand, supported endpoints
        self.__endpoints = {
            "package": "jailbreak/package/",
            "repo": "jailbreak/repository/",
            "search": "jailbreak/package/search",
        }
        self.__info = CanisterComponents(self.__http_agent)

    async def __search_canister(
        self,
        endpoint: str,
        query: Optional[str] = None,
        *,
        params: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        api_endpoint = self.__endpoints.get(endpoint)
        request_url = f"{self.__base}/{api_endpoint}"

        if query:
            request_url += query

        request_args: Dict[str, Any] = {
            "url": request_url,
            "params": params,
            "headers": {
                "User-Agent": self.__info.user_agent,
                "content-type": "application/json"
            }
        }

        async with self.__session.get(**request_args) as resp:
            response = await resp.json()

        return APIResponse(**response)

    async def search_packages(
        self,
        query: str,
        *,
        limit: Optional[int] = 250,
        page: Optional[int] = 1
    ) -> List[Package]:
        params = {
            "q": query,
            "limit": limit,
            "page": page
        }
        resp = await self.__search_canister(
            "search", params=params
        )
        return [Package(**package) for package in resp.data]

    async def get_package(self, query: str) -> Package:
        resp = await self.__search_canister("package", query)
        return Package(**resp.data[0])

    async def get_repository(self, repo_slug: str) -> Repository:
        resp = await self.__search_canister("repo", repo_slug)
        return Repository(**resp.data)

    async def close(self) -> None:
        if isinstance(self.__session, aiohttp.ClientSession):
            await self.__session.close()
