# canister.py

An `async` wrapper for the Canister API, written in Python. **There
are no front-facing docs for this, and it's not on PyPI.**

## History

Seeing as there's no API wrapper for Canister (since it's still a work
in progress) written in Python, I decided to make this for that
occasion.

Its main use (for me, at least) was to be used alongside a Discord bot
to interact with Canister. The wrapper itself supports a limited amount
of API endpoints, and is just as unfinished as Canister itself.

### Usage

`canister.py` can be imported like any Python module once installed. The
example below should provide a general idea on how to get started.

```py
# Import canister.py and asyncio
import asyncio
import canister

from typing import List

async def main(package_name: str) -> List[canister.CanisterPackage]:
    """ Search Canister for the given package """
    # Create an instance of the Canister client
    client = canister.Client()

    # Next, search Canister using the created client
    # The search term can be any string, passed in the function

    # This will return a list of packages that match the query
    packages = await client.get_packages(package_name)

    # This is optional in most cases, but you should
    # close the running instance of the Canister client
    await client.close()

    # Print general information about the retrieved package
    # The returned object has several attributes, as well
    [print(package) for package in packages]

# Setup async related stuff and run the function
# The function recieves "siguza-utils" as a query term
loop = asyncio.get_event_loop()
loop.run_until_complete(main("siguza-utils"))
```

## License

This project is licensed under the [BSD 3-Clause License](LICENSE)
