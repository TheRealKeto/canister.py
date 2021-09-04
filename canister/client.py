# canister.py (client.py)
# Class wrapper for Canister

# Imports
import aiohttp
import requests

from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union
)

from .objects import (
    CanisterPackage,
    CanisterAPIResponse,
    CanisterRepository
)

class Client:
    """ Class representation of the Canister API client.

    This class will interact with the Canister API, and allow
    users to make requests to it. """
    def __init__(
        self,
        *,
        session: Optional[Union[aiohttp.ClientSession, requests.Session]] = None,
        **kwargs: Any
    ):
        # Set the base endpoint of the Canister API
        self.__base = "https://api.canister.me/v1/community"

        # Setup specific request parameters
        # These are used when interacting with the API
        self.__params: Dict[str, List[str]] = {
            # Add user specified search fields
            "searchFields": kwargs.pop("search_fields", []),
            # Add user specified response fields
            "responseFields": kwargs.pop("resp_fields", [])
        }

        # Specify whether to do it async or not
        # This makes it easier to check what session to use
        self.__async = session is None or isinstance(
            session, aiohttp.ClientSession
        )

        # Specify the given aiohttp session globally
        # Create one session is an aiohttp session isn't given
        self.__session = session

        # Create a list of supported API endpoints
        self.__endpoints: Dict[str, str] = {
            # More endpoints will be added here later
            "packages": "packages/search",
            "check/repo": "repositories/check"
        }

    def __prepare_request(self, endpoint: str, query: str):
        """ Prepares any request to the Canister API.

        This function works regardless as to whether the
        request is being done async or not. """
        # Get the specified endpoint for the request
        # then, attach it to the API base, creating a URL
        request_url = f"{self.__base}/{self.__endpoints.get(endpoint)}"

        # Update the API params with the given query
        (params := self.__params).update({"query": query})

        # Return the created URL and parameters
        # These are important for each request made
        return request_url, params

    def __create_packages(self, metadata: Dict[str, str]) -> List[CanisterPackage]:
        """ Creates a list of packages.

        The list of packages contain given metadata from
        a Canister API request, made either with requests
        or aiohttp. """
        # Create an empty list for converted packages
        # Packages contain metadata recieved from a request
        package_list: List[CanisterPackage] = []

        # Convert each request result into a CanisterPackage object
        for package in metadata:
            # Convert package metadata
            # Makes it easier to refer to data
            new_package = CanisterPackage(package)

            # Append the converted package to the list
            package_list.append(new_package)

        # Return the list of converted packages
        return package_list

    async def __generate_aiohttp_session(self) -> aiohttp.ClientSession:
        """ Generates a live aiohttp session if one isn't given. """
        # Start a live aiohttp session
        # then, pass the live session to the client
        self.__session = aiohttp.ClientSession()
        return self.__session

    async def __async_search_canister(
        self, endpoint: str, query: str
    ) -> CanisterAPIResponse:
        """ Async request to the Canister API with aiohttp. """
        # Check if the request is meant to be async or not
        # then, generate a live aiohttp session if one isn't given
        if not self.__session and self.__async:
            self.__session = await self.__generate_aiohttp_session()

        # Get the request URL and params for the request
        request_url, params = self.__prepare_request(endpoint, query)

        # Actually make a request with the given/generated aiohttp session
        async with self.__session.get(request_url, params=params) as resp:
            # Get the response of the request
            # TODO: Do some error handling here
            response = await resp.json()

        # Return the response as a CanisterAPIResponse object
        # This makes it easier to acess requested information
        return CanisterAPIResponse(**response)

    async def __async_get_packages(self, query: str) -> List[CanisterPackage]:
        """ Async version of get_packages, with aiohttp. """
        # Search Canister for packages that match the given query
        resp = await self.__async_search_canister("packages", query)

        # Convert each response result into a CanisterPackage object
        return self.__create_packages(resp.data)

    async def __async_check_repository(self, repo_url: str) -> CanisterRepository:
        """ Async version of check_repository, with aiohttp. """
        # Check if the given repo URL is an unsafe repo
        resp = await self.__async_search_canister("check/repo", repo_url)

        # Get the returned metadata of the request
        # Wrap the response in a CanisterRepository object
        return CanisterRepository(resp.data)

    def __sync_search_canister(
        self, endpoint: str, query: str
    ) -> CanisterAPIResponse:
        """ Sync request to the Canister API. """
        # Get the request URL and params for the request
        request_url, params = self.__prepare_request(endpoint, query)

        # Load up the response using requests
        # This module is so slow but whatever...
        response = self.__session.get(request_url, params=params)

        # Wrap the response in a CanisterAPIResponse object
        return CanisterAPIResponse(**response.json())

    def __sync_get_packages(self, query: str) -> List[CanisterPackage]:
        """ Sync version of get_packages. """
        # Search Canister for packages that match the given query
        resp = self.__sync_search_canister("packages", query)

        # Convert each response result into a CanisterPackage object
        return self.__create_packages(resp.data)

    def __sync_check_repository(self, repo_url: str) -> CanisterRepository:
        """ Sync version of check repository. """
        # Check if the given URL is an unsafe repo
        resp = self.__sync_search_canister("check/repo", repo_url)

        # Get the response of the request
        # Wrap the returned metadata in a CanisterRepository object
        return CanisterRepository(resp.data)

    def get_packages(self, query: str) -> List[CanisterPackage]:
        """ Obtains a list of packages based on given query.

        This function uses the 'packages' endpoint in order
        to return a list of packages available in Canister
        based on the given query. """
        # Use requests to interact with Canister first
        # This checks if the function should be awaited
        if not self.__async:
            # Get the list of packages with the given query
            return self.__sync_get_packages(query)
        # By default, use aiohttp to get the package list
        return self.__async_get_packages(query)

    def check_repository(self, repo_url: str) -> CanisterRepository:
        """ Checks if the given query is an unsafe repo.

        This is based on a list that Canister internally uses,
        which contains repositories that host malware or are
        otherwise considered as piracy. """
        # Use requests to interact with Canister first
        if not self.__async:
            # Check the given repo URL if it's safe
            return self.__sync_check_repository(repo_url)
        # By default, use aiohttp and check the given repo URL
        return self.__async_check_repository(repo_url)

    async def close(self) -> None:
        """ Closes the aiohttp session used to make requests. """
        # Check if there's a running aiohttp session
        # TODO: Return a proper error if this fails at some point
        if self.__session and isinstance(self.__session, aiohttp.ClientSession):
            # Close the running aiohttp session
            await self.__session.close()
