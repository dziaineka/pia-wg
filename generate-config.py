from time import sleep
from piawg import piawg
from pick import pick
from credentials import get_credentials

username, password = get_credentials()

pia = piawg()

# Generate public and private key pair
pia.generate_keys()

# Select region
title = 'Please choose a region: '
available_options = sorted(list(pia.server_list.keys()))

selected_options: list[tuple[str, int]] = \
    pick(available_options, title, multiselect=True)

for option_with_index in selected_options:
    option = option_with_index[0]

    pia.set_region(option)
    pia.get_token(username, password)
    print("Selected '{}'".format(option))

    # Add key
    status, response = pia.addkey()
    if status:
        print("Added key to server!")
    else:
        print("Error adding key to server")
        print(response)

    # Build config
    location = pia.region.replace(' ', '-')
    config_file = 'PIA-{}.conf'.format(location)
    print("Saving configuration file {}".format(config_file))

    with open(config_file, 'w') as file:
        file.write('[Interface]\n')
        file.write('Address = {}\n'.format(pia.connection['peer_ip']))
        file.write('PrivateKey = {}\n'.format(pia.privatekey))
        file.write('DNS = {},{}\n\n'.format(pia.connection['dns_servers'][0], pia.connection['dns_servers'][1]))
        file.write('[Peer]\n')
        file.write('PublicKey = {}\n'.format(pia.connection['server_key']))
        file.write('Endpoint = {}:1337\n'.format(pia.connection['server_ip']))
        file.write('AllowedIPs = 0.0.0.0/0\n')
        file.write('PersistentKeepalive = 25\n')

    sleep(3)
