# canister.py (client.py)
# Class wrapper for Canister

# Imports
import aiohttp

from typing import (
    Any,
    Dict,
    List,
    Optional
)

from .objects import (
    CanisterPackage,
    CanisterAPIResponse,
    CanisterRepository
)

class CanisterClient:
    """ Class representation of the Canister API client.

    This class will interact with the Canister API, and allow
    users to make requests to it. """
    def __init__(
        self,
        *,
        session: Optional[aiohttp.ClientSession] = None,
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

        # Specify the given aiohttp session globally
        # Create one session is an aiohttp session isn't given
        self.__session = session or aiohttp.ClientSession()

        # Create a list of supported API endpoints
        self.__endpoints: Dict[str, str] = {
            # More endpoints will be added here later
            "packages": "packages/search",
            "check/repo": "repositories/check"
        }

    async def __search_canister(
        self, endpoint: str, query: str
    ) -> CanisterAPIResponse:
        """ Make a request to the Canister API.

        The request is made to a specificied endpoint,
        and results will match with the given query. """
        # Get the specified endpoint for the request
        # then, attach it to the API base, creating a URL
        request_url = f"{self.__base}/{self.__endpoints.get(endpoint)}"

        # Update the API params with the given query
        (params := self.__params).update({"query": query})

        # Actually make a request to the Canister API
        async with self.__session.get(request_url, params=params) as resp:
            # Get the response of the request
            # TODO: Add error handling to this function
            response = await resp.json()

        # Return the response as a CanisterResponse object
        # This makes it easier to access requested information
        return CanisterAPIResponse(**response)

    async def get_packages(self, query: str) -> List[CanisterPackage]:
        """ Obtains a list of packages based on given query.

        This function uses the 'packages' endpoint in order
        to return a list of packages available in Canister
        based on the given query. """
        # Create an empty list
        # Used for converted package data
        package_list: List[CanisterPackage] = []

        # Search Canister for packages that match the given query
        resp = await self.__search_canister("packages", query)

        # Convert each response result into a CanisterPackage object
        for package in resp.data:
            # Convert package data
            # This makes it easier to refer to it
            new_package = CanisterPackage(package)

            # Append the converted data to the list
            package_list.append(new_package)

        # Return the list of converted packages
        return package_list

    async def check_repository(self, query: str) -> CanisterRepository:
        """ Checks if the given query is an unsafe repo.

        This is based on a list that Canister internally uses,
        which contains repositories that host malware or are
        otherwise considered as piracy. """
        # Check if the given query is an unsafe repo
        resp = await self.__search_canister("check/repo", query)

        # Get the returned data of the request
        # Wrap the response in a CanisterRepository object
        return CanisterRepository(resp.data)

    async def close(self) -> None:
        """ Closes the aiohttp session used to make requests. """
        # Check if there's a running aiohttp session
        # TODO: Return a proper error if this fails at some point
        if isinstance(self.__session, aiohttp.ClientSession):
            # Close the running aiohttp session
            await self.__session.close()
