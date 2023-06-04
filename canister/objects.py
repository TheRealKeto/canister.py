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

from dataclasses import field, dataclass


@dataclass(frozen=True)
class CanisterComponents:
    canister_version: str
    python_version: str
    aiohttp_version: str

    @property
    def user_agent(self) -> str:
        return ", ".join((
            f"canister.py/{self.canister_version}",
            self.python_version,
            self.aiohttp_version
        ))


@dataclass(frozen=True)
class CanisterAPIResponse:
    status: str
    date: str
    refs: Optional[Dict[str, str]] = field(default=None)
    count: Optional[int] = field(default=None)
    data: List[Dict[str, Any]] = field(
        default_factory=list
    )
    error: Optional[str] = field(default=None)


@dataclass(frozen=True)
class CanisterAPIErrResponse:
    status: str
    date: str
    error: str


@dataclass()
class CanisterPackage:
    architecture: str
    author: str
    depiction: Optional[str]
    description: str
    filename: str
    header: Optional[str]
    icon: Optional[str]
    installedSize: int = field(repr=False)
    installed_size: int = field(init=False)
    isCurrent: bool = field(repr=False)
    is_current: bool = field(init=False)
    isPruned: bool = field(repr=False)
    is_pruned: bool = field(init=False)
    maintainer: str
    name: Optional[str]
    nativeDepiction: Optional[str] = field(repr=False)
    native_depiction: Optional[str] = field(init=False)
    package: str
    price: str
    refs: Dict[str, str]
    repository: Dict[str, Any]
    repositorySlug: str = field(repr=False)
    repository_slug: str = field(init=False)
    repositoryTier: int = field(repr=False)
    repository_tier: int = field(init=False)
    section: str
    sha256: int
    sileoDepiction: Optional[str] = field(repr=False)
    sileo_depiction: Optional[str] = field(init=False)
    size: int
    tags: Optional[List[str]]
    tintColor: Optional[str] = field(repr=False)
    tint_color: Optional[str] = field(init=False)
    uuid: str
    version: str

    # Let's deal with camelCase bullshit
    def __post_init__(self) -> None:
        self.installed_size = self.installedSize
        self.is_current = self.isCurrent
        self.is_pruned = self.isPruned
        self.native_depiction = self.nativeDepiction
        self.sileo_depiction = self.sileoDepiction
        self.repository_slug = self.repositorySlug
        self.repository_tier = self.repositoryTier
        self.tint_color = self.tintColor
