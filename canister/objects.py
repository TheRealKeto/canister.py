# canister.py (objects.py)
# Object classes for Canister

# Imports
from typing import (
    Dict,
    List,
    Optional
)

from dataclasses import field, dataclass

@dataclass(frozen=True)
class CanisterAPIResponse(object):
    """ Namedtuple representation of a request response.

    This class is the raw representation of a returned response
    from the Canister API. """
    # Status of the request
    status: str

    # Date of when the request was made
    date: str

    # Message returned by the request
    # You'll only get one if the request fails
    message: Optional[str] = field(default_factory=str)

    # Data response of the API request
    # Raw data, handled by specific class objects
    data: List[Optional[Dict[str, str]]] = field(default_factory=list)

class CanisterPackage(object):
    """ Independent class representation of a package object.

    This class takes data from a CanisterAPIResponse object,
    making it easier to refer to specific fields of packages. """
    def __init__(self, data: Dict[str, str]):
        # Get the name of the package
        self.__name: Optional[str] = data.get("name")

        # Get the package identifier
        # This also serves as the package name
        self.identifier: str = data.get("identifier")

        # Get the description of the package
        self.description: str = data.get("description")

        # Get the section of the package
        self.section: Optional[str] = data.get("section")

        # Get the author and maintainer of the package
        self.__author: Optional[str] = data.get("author")
        self.maintainer: str = data.get("maintainer")

        # Get the URLs of package depictions
        self.__depiction: Optional[str] = data.get("depiction")
        self.__sileodepiction: Optional[str] = data.get("nativeDepiction")

        # Get the URL to the package icon image
        # In many cases, packages may not have this
        self.icon_url: Optional[str] = data.get("packageIcon")

        # Get the version of the package
        # Only returns the latest version available
        self.version: str = data.get("latestVersion")

        # Get information about the package repo
        # Will be used to get the URL of the repo
        self.__repo: Dict[str, str] = data.get("repository")

        # Get the tint color of the package icon
        self.color: Optional[str] = data.get("tintColor")

    def __repr__(self) -> str:
        """ Visual representation of the object. """
        return f"CanisterPackage('{self.name}', '{self.description}')"

    @property
    def depiction(self) -> Optional[str]:
        """ Returns the package's depiction.

        This property defaults to returning the native depiction
        of the package, which is used by Sileo, but it will
        try to avoid None by attempting to return the raw depiction.

        Unfortunately, some packages simply don't have any depictions,
        hence this can still return None. """
        # Check for the package's native depiction
        if self.__sileodepiction is not None:
            # Return the native depiction
            return self.__sileodepiction

        # All other instances, return the raw depiction
        # Doesn't avoid having None; it can still happen
        return self.__depiction

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
        return self.identifier

    @property
    def repo_url(self) -> str:
        """ Returns the package's repository URL. """
        # Return the URI from the repository response
        return self.__repo.get("uri")

class CanisterRepoStatus(object):
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
        return f"CanisterRepoStatus('{self.url}', status='{self.status}')"

    @property
    def status(self) -> str:
        """ Return the status of the repository.

        This property tells users whether the repository
        is marked as safe or unsafe. """
        # Get the status from the response
        # then, capitalize the returned status
        return self.__status.capitalize()

class CanisterRepository(object):
    """ Independent class representation of a package object.

    This class takes data from a CanisterAPIResponse object,
    making it easier to refer to specific fields of repositories. """
    def __init__(self, data: Dict[str, str]):
        # Get the of the repository
        self.name: str = data.get("name")

        # Get the name of the URI
        # This property has an alias
        self.uri: str = data.get("uri")

        # Get the version of the repository
        self.version: str = data.get("version")

        # Get the slug of the repository
        self.slug: str = data.get("slug")

        # Get the list of aliases
        # These are other names the repo is known by
        self.__aliases: Optional[List[str]] = data.get("aliases")

    def __repr__(self) -> str:
        """ Visual representation of the object. """
        return f"CanisterRepository('{self.name}', '{self.url}')"

    @property
    def url(self) -> str:
        """ Returns the URL of the repository.

        This property also functions as an alias to get the URI
        of the repository. You can use either property. """
        return self.uri

    @property
    def aliases(self) -> Optional[str]:
        """ Returns all the aliases that the repository is known by.

        In most instances, this property will return None, as most
        repositories do not have aliases. If aliases are found, they
        are returned in joined string. """
        return ", ".join(self.__aliases) or None
