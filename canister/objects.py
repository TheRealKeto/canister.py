#
# Copyright (c) 2023 TheRealKeto
# SPDX-License-Identifier: BSD-3-Clause
#

from typing import (
    Any,
    Dict,
    List,
    Union,
    Optional
)

from importlib import metadata
from dataclasses import field, dataclass


@dataclass(frozen=True)
class CanisterComponents:
    aiohttp_info: str

    @property
    def user_agent(self) -> str:
        try:
            version = metadata.version(__package__)
        except metadata.PackageNotFoundError:
            version = "0.0.0-unknown"

        return ", ".join((
            f"canister.py/{version}",
            *self.aiohttp_info.split()
        ))


@dataclass(frozen=True)
class APIResponse:
    status: str
    date: str
    data: Any
    refs: Optional[Dict[str, str]] = field(default=None)
    count: Optional[int] = field(default=None)
    error: Optional[str] = field(default=None)


@dataclass()
class Package:
    architecture: str
    author: Optional[str]
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
        if not self.author:
            self.author = self.maintainer

        self.installed_size = self.installedSize
        self.is_current = self.isCurrent
        self.is_pruned = self.isPruned
        self.native_depiction = self.nativeDepiction
        self.sileo_depiction = self.sileoDepiction

        if not self.sileo_depiction:
            self.sileo_depiction = self.native_depiction

        self.repository_slug = self.repositorySlug
        self.repository_tier = self.repositoryTier
        self.tint_color = self.tintColor


@dataclass()
class Repository:
    slug: str
    aliases: List[Optional[str]]
    isBootstrap: bool = field(repr=False)
    is_bootstrap: bool = field(init=False)
    tier: int
    packageCount: int = field(repr=False)
    package_count: int = field(init=False)
    sections: List[str]
    uri: str
    suite: Optional[str]
    component: Optional[str]
    name: str
    version: str
    description: str
    date: str
    paymentGateway: str = field(repr=False)
    payment_gateway: str = field(init=False)
    sileoEndpoint: str = field(repr=False)
    sileo_endpoint: str = field(init=False)
    isPruned: bool = field(repr=False)
    is_pruned: bool = field(init=False)
    origin: Dict[str, Union[str, bool]]
    originId: str = field(repr=False)
    origin_id: str = field(init=False)
    packages: str
    refs: Dict[str, str]

    def __post_init__(self) -> None:
        self.is_bootstrap = self.isBootstrap
        self.package_count = self.packageCount
        self.payment_gateway = self.paymentGateway
        self.sileo_endpoint = self.sileoEndpoint
        self.is_pruned = self.isPruned
        self.origin_id = self.originId
