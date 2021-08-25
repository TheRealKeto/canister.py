# canister.py (objects.py)
# Object classes for Canister

# Imports
from typing import (
    Dict,
    List,
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
