# canister.py (client.py)
# Class wrapper for Canister

# Imports
import aiohttp

from typing import (
    Any,
    Dict,
    List,
    Union,
    Optional
)

from .objects import (
    CanisterPackage,
    CanisterAPIResponse,
    CanisterRepository,
    CanisterRepoStatus,
)

class CanisterClient:
    """ Class representation of the Canister API client.

    This class will interact with the Canister API, and allow
    users to make requests to it. """
    def __init__(
        self,
        *,
        user_agent: str,
        session: Optional[aiohttp.ClientSession] = None,
        **kwargs: Any
    ):
        # Set the base endpoint of the Canister API
        self.__base: str = "https://api.canister.me/v1/community"

        # Setup specific request parameters
        # These are used when interacting with the API
        self.__params: Dict[str, Union[str, List[str]]] = {
            # Add user specified search fields
            "searchFields": kwargs.pop("search_fields", []),
            # Add user specified response fields
            "responseFields": kwargs.pop("resp_fields", "*")
        }

        # Specify a (required) user agent for requets
        # This is requirement by the Canister API, so...
        self.__user_agent: str = user_agent

        # Specify the given aiohttp session globally
        # Create one session is an aiohttp session isn't given
        self.__session = session or aiohttp.ClientSession()

        # Create a list of supported API endpoints
        self.__endpoints: Dict[str, str] = {
            # More endpoints will be added here later
            "packages": "packages/search",
            "check/repo": "repositories/check",
            "repositories": "repositories/search"
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
        (request_params := self.__params).update({"query": query})

        # Add parameters and headers into a dict, for the request
        request_args: Dict[str, Any] = {
            # Also, add API URL being used for the request
            "url": request_url,
            "params": request_params,
            "headers": {"User-Agent": self.__user_agent}
        }

        # Actually make a request to the Canister API
        async with self.__session.get(**request_args) as resp:
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

        # Search Canister for packages that match the given query
        resp = await self.__search_canister("packages", query)

        # Convert each response result into a CanisterPackage object
        # then, append the Package object and return a list of packages
        return [CanisterPackage(package) for package in resp.data]

    async def get_repositories(self, query: str) -> List[CanisterRepository]:
        """ Obtains a list of repositories based on given query.

        This function uses the 'search/repos' endpoint in order
        to return a list of repos available in Canister that
        matched the given query. """

        # Search Canister for repositories that match the given query
        resp = await self.__search_canister("repositories", query)

        # Convert each response result into a CanisterRepo object
        # then, append the Repo object and return a list of repos
        return [CanisterRepository(repo) for repo in resp.data]

    async def check_repository(self, query: str) -> CanisterRepoStatus:
        """ Checks if the given query is an unsafe repo.

        This is based on a list that Canister internally uses,
        which contains repositories that host malware or are
        otherwise considered as piracy. """
        # Check if the given query is an unsafe repo
        resp = await self.__search_canister("check/repo", query)

        # Get the returned data of the request
        # Wrap the response in a CanisterRepository object
        return CanisterRepoStatus(resp.data)

    async def close(self) -> None:
        """ Closes the aiohttp session used to make requests. """
        # Check if there's a running aiohttp session
        # TODO: Return a proper error if this fails at some point
        if isinstance(self.__session, aiohttp.ClientSession):
            # Close the running aiohttp session
            await self.__session.close()
