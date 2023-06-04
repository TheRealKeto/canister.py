#
# Copyright (c) 2023 TheRealKeto
# SPDX-License-Identifier: BSD-3-Clause
#

from typing import (
    Any,
    Dict,
    List,
    Optional
)

from dataclasses import dataclass


@dataclass(frozen=True)
class CanisterComponents:
    canister_version: str
    python_version: str
    aiohttp_version: str

    @property
    def user_agent(self) -> str:
        return ", ".join((
            f"canister/{self.canister_version}",
            self.python_version,
            self.aiohttp_version
        ))


@dataclass(frozen=True)
class CanisterAPIResponse:
    status: str
    date: str
    refs: Dict[str, str]
    count: int
    data: List[Optional[Dict[str, Any]]]
