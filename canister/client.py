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

from .objects import CanisterAPIResponse

class Client:
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
            "response_fields": kwargs.pop("resp_fields", [])
        }

        # Specify the given aiohttp session globally
        # Create one session is an aiohttp session isn't given
        self.__session = session or aiohttp.ClientSession()

        # Create a list of supported API endpoints
        self.__endpoints: Dict[str, str] = {
            # More endpoints will be added here later
            "packages": "packages/search"
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

    async def close(self) -> None:
        """ Closes the aiohttp session used to make requests. """
        # Check if there's a running aiohttp session
        # TODO: Return a proper error if this fails at some point
        if self.__session and isinstance(self.__session, aiohttp.ClientSession):
            # Close the running aiohttp session
            await self.__session.close()
