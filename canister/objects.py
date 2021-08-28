# canister.py (objects.py)
# Object classes for Canister

# Imports
from typing import (
    Dict,
    List,
    Union,
    Optional,
    NamedTuple
)

class CanisterAPIResponse(NamedTuple):
    """ Namedtuple representation of a request response.

    This class is the raw representation of a returned response
    from the Canister API. """
    # Status of the request
    status: str

    # Date of when the request was made
    date: str

    # Data response of the API request
    # Raw data, handled by specific class objects
    data: List[Dict[str, str]]

class CanisterPackage(object):
    """ Independent class representation of a package object.

    This class takes data from a CanisterAPIResponse object,
    making it easier to refer to specific fields of packages. """
    def __init__(self, data: Dict[str, str]):
        # Get the name of the package
        self.__name: Union[str, None] = data.get("name")

        # Get the package identifier
        # This also serves as the package name
        self.package: str = data.get("identifier")

        # Get the description of the package
        self.description: str = data.get("description")

        # Get the section of the package
        self.section: str = data.get("section")

        # Get the author and maintainer of the package
        self.__author: Optional[str] = data.get("author")
        self.maintainer: str = data.get("maintainer")

        # Get the URLs of package depictions
        self.__normal_depiction: str = data.get("depiction")
        self.__native_depiction: str = data.get("nativeDepiction")

        # Get the URL to the package icon image
        # In many cases, packages may not have this
        self.icon_url: str = data.get("packageIcon")

        # Get the version of the package
        # Only returns the latest version available
        self.version: str = data.get("latestVersion")

        # Get information about the package repo
        # Will be used to get the URL of the repo
        self.__repo: Dict[str, str] = data.get("repository")

    def __repr__(self) -> str:
        """ Visual represenation of the object. """
        return f"CanisterPackage('{self.name}', '{self.description}')"

    def depiction(self, depiction_type: Optional[str] = None) -> str:
        """ Returns the specified depiction type.

        The depiction type can either be the native depiction,
        which is used by Sileo, or the normal depiction, used
        by other packages managers. """
        # Use a case-switch thingy to 'chose'
        # It'll default to the normal depiction
        depictions: Dict[str, str] = {
            "normal": self.__normal_depiction,
            "native": self.__native_depiction
        }

        # Chose the specified depiction type
        return depictions.get(depiction_type, depictions.get("normal"))

    @property
    def author(self) -> str:
        """ Returns the author of the package.

        As a fallback, this property will return the
        package's maintainer if there's no package available. """
        # Check if there's an author value
        if self.__author is not None:
            # Return the accurate package author
            return self.__author

        # All other instances, return the package maintanier
        return self.maintainer

    @property
    def name(self) -> str:
        """ Returns the name of the package.

        As a fallback, this property will return the
        package's identifier if there's no name available. """
        # Check if there's an available package name
        if self.__name is not None:
            # Return the accurate package name
            return self.__name

        # All other instances, return the package identifier
        return self.package

    @property
    def url(self) -> str:
        """ Returns the package's repository URL. """
        # Return the URI from the repository response
        return self.__repo.get("uri")

class CanisterRepository(object):
    """ Class representation of a repository check.

    This specific class handles the contents of a repo check
    request from Canister, using the 'check/repo' endpoint. """
    def __init__(self, data: Dict[str, str]):
        # Get the URL of the repository
        self.url: str = data.get("repositoryURI")

        # Get the status of the repository
        # Tells users whether a repo is safe or not
        self.__status: str = data.get("status")

    def __repr__(self) -> str:
        """ Visual representation of the object. """
        return f"CanisterRepository('{self.url}', status='{self.status}')"

    @property
    def status(self) -> str:
        """ Return the status of the repository.

        This property tells users whether the repository
        is marked as safe or unsafe. """
        # Get the status from the response
        # then, capitalize the returned status
        return self.__status.capitalize()
