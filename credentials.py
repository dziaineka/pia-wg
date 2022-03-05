from typing import Tuple
from piawg import piawg
from getpass import getpass


def get_credentials() -> Tuple[str, str]:
    pia = piawg()

    # Generate public and private key pair
    pia.generate_keys()

    # Select region
    options = sorted(list(pia.server_list.keys()))
    pia.set_region(options.pop())

    # Check credentials
    while True:
        username = input("\nEnter PIA username: ")
        password = getpass()
        if pia.get_token(username, password):
            print("Login successful!")
            return username, password
        else:
            print("Error logging in, please try again...")
