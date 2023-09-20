#python3
import requests
# import datetime
import time
import socket
import os


lcd_info = '/cosmos/base/tendermint/v1beta1/node_info'
lcd_syncing = '/cosmos/base/tendermint/v1beta1/syncing'
app_version = '2.0.3'
rpc_info = '/status?'
bc_chain_registry = 'https://raw.githubusercontent.com/BitCannaGlobal/bcna/main/chain-registry.json'
cosmos_chain_registry = 'https://raw.githubusercontent.com/cosmos/chain-registry/master/bitcanna/chain.json'


def check_peers_seeds_connection(address, port):
 
    # Create a TCP socket
    timeout = 5 #timeout in seconds
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    print (' 🌍 Attempting to connect to %s on port %s' % (address, port))
    try:
        s.connect((address, int(port)))
        output = 'Connected to %s on port %s' % (address, port)
        print('    🟢 ', end =' ')
    except socket.error as error:
        output = 'Connection to %s on port %s failed: %s' % (address, port, error)
        print('    ⛔ ', end =' ')
    finally:
        s.close()
    return output

def check_http_connection(address, json_check):
    match json_check:
        case "rpc":
            URL = address + rpc_info
            print (' 🌍 Attempting to connect to %s'  % (URL))
            try:
                # print(URL)
                response_check = requests.get(URL, headers={"Accept": "application/json"}, timeout=5)
                print ('    🍌 RESPONSE: %s ' % (response_check))
                if response_check.status_code != 200:
                    output = 'ERROR. Status code at server:  %s is: %s   failed' % (URL, str(response_check.status_code))
                    print('    ⛔ ' + output)
                    pass               
            except:
                output = 'ERROR. Connection to server:  %s failed' % (URL)
                print('    ⛔ ', end =' ')
            else:
                try:
                    json_response = response_check.json()
                except:
                    json_error = 'An error occurred getting the JSON data'
                    print('    ⛔ ', end =' ')
                    output = json_error
                else:        
                    json_response = response_check.json()
                    id = json_response["result"]["node_info"]["id"]
                    moniker = json_response["result"]["node_info"]["moniker"]
                    tx_index = json_response["result"]["node_info"]["other"]["tx_index"]
                    synced = json_response["result"]["sync_info"]["catching_up"]
                    voting_power = json_response["result"]["validator_info"]["voting_power"]
                    output = id, moniker, tx_index, synced, voting_power
                    if int(voting_power) > 0:
                        print('    ❗ This public RPC is running in a MainNET Validator ❗')
                    if synced != False:
                        print('    ❗ This public RPC is NOT SYNCED at MainNET ❗')
                    if tx_index != 'on':
                        print('    ❗ This public RPC has not activated the TX Index ❗')
                    print('    🟢', end =' ')
        case "archive_nodes":
            URL = address + rpc_info
            print (' 🌍 Attempting to connect to %s'  % (URL))
            try:
                # print(URL)
                response_check = requests.get(URL, headers={"Accept": "application/json"}, timeout=5)
                print ('    🍌 RESPONSE: %s ' % (response_check))
            except:
                output = 'ERROR. Connection to server:  %s failed' % (URL)
                print('    ⛔ ', end =' ')
            else:
                try:
                    json_response = response_check.json()
                except:
                    json_error = 'An error occurred getting the JSON data'
                    print('    ⛔ ', end =' ')
                    output = json_error
                else:        
                    json_response = response_check.json()
                    id = json_response["result"]["node_info"]["id"]
                    moniker = json_response["result"]["node_info"]["moniker"]
                    synced = json_response["result"]["sync_info"]["catching_up"]
                    earliest_block = json_response["result"]["sync_info"]["earliest_block_height"]
                    voting_power = json_response["result"]["validator_info"]["voting_power"]
                    output = id, moniker, synced, earliest_block, voting_power
                    if int(voting_power) > 0:
                        print('    ❗ This public RPC is running in a MainNET Validator ❗')
                    if synced != False:
                        print('    ❗ This public RPC is NOT SYNCED at MainNET ❗')
                    if int(earliest_block) != 1:
                        print('    ❗❗ This Archive Node does not sync the whole chain ❗❗')
                    else:
                        print('    🟢 This Archive Node syncs the whole chain')
        case "explorer":
            URL = address
            print (' 🌍 Attempting to connect to %s'  % (URL))
            try:
                response_check = requests.get(URL, headers={"Accept": "application/json"}, timeout=5)
                print ('    🍌 RESPONSE: %s ' % (response_check))
            except:
                output = 'ERROR. Connection to server:  %s failed' % (URL)
                print('    ⛔ ', end =' ')
            else:
                print('    🟢 ', end =' ')
                output = 'Connected'
        case "lcd":
            URL = address + lcd_info
            print (' 🌍 Attempting to connect to %s'  % (URL))
            try:
                # print(URL)
                response_check = requests.get(URL, headers={"Accept": "application/json"}, timeout=5)
                print ('    🍌 RESPONSE: %s ' % (response_check))
            except:
                output = 'ERROR. Connection to server:  %s failed' % (URL)
                print('    ⛔ ', end =' ')
            else:
                try:
                    json_response = response_check.json()
                except:
                    json_error = 'An error occurred getting the JSON Node data'
                    print('    ⛔ ', end =' ')
                    output = json_error
                else:        
                    json_response = response_check.json()
                    id = json_response["default_node_info"]["default_node_id"]
                    moniker = json_response["default_node_info"]["moniker"]
                    tx_index = json_response["default_node_info"]["other"]["tx_index"]
                    version = json_response["application_version"]["version"]
                    output = id, moniker, tx_index, version
                    if version != app_version:
                        print('    ❗ This public LCD is not running the last version of the BCNA software ❗')
                    if tx_index != 'on':
                        print('    ❗ This public LCD has not activated the TX Index ❗')
                    print('    🟢', end =' ')
            # check the syncing
            URL = address + lcd_syncing
            print ('Checking SYNCING at %s'  % (URL))
            try:
                # print(URL)
                response_check = requests.get(URL, headers={"Accept": "application/json"}, timeout=5)
                print ('    🍌 RESPONSE: %s ' % (response_check))
            except:
                output = 'ERROR. Connection to server:  %s failed' % (URL)
                print('    ⛔ ', end =' ')
            else:
                try:
                    json_response = response_check.json()
                except:
                    json_error = 'An error occurred getting the JSON Syncing data'
                    print('    ⛔ ', end =' ')
                    output = json_error
                else:        
                    json_response = response_check.json()
                    syncing  = json_response["syncing"]
                    output = output + (syncing, )
                    if syncing != False:
                        print('    ❗ This public LCD is NOT SYNCED at MainNET ❗')
                    print('    🟢', end =' ')
        case "grpc":
            print (' 🌍 Attempting to connect to %s'  % (address))
            # determine if is a TLS connection or not
            hostname = address.split(":")
            port = hostname[1]
            if port == '443':
                plaintext = ''
            else:
                plaintext = '-plaintext '
            cmd = 'grpcurl -vv ' + plaintext + address + ' list'
            #print(cmd)
            returned_value = os.system(cmd)  # returns the exit code in unix
            # print('returned value:', returned_value)
            if returned_value == 0:
                output = 'Connection to GRPC is successfully done.'
                print('    🟢 ', end =' ')
            else:
                output = 'ERROR. Connection to server:  %s failed' % (address)
                print('    ⛔ ', end =' ')               
    return output

def do_checks(services):
    print(services)
    for service in services:
        match service:
            case 'lcds':
                elements = json_response.get('apis').get('rest')
                field = 'address'
                type = 'lcd'               
            case 'grpcs':
                elements = json_response.get('apis').get('grpc')
                field = 'address'
                type = 'grpc'
            case 'rpcs':
                elements = json_response.get('apis').get('rpc')
                field = 'address'
                type = 'rpc' 
            case 'explorers':
                elements = json_response.get('explorers')
                field = 'url'
                type = 'explorer'
            case 'archive_nodes':
                elements = json_response.get('archive_nodes')
                field = 'address'
                type = 'archive_nodes'  
            case 'state_sync':
                elements = json_response.get('state_sync')
                field = 'address'
                type = 'rpc'
            case 'explorers':
                elements = json_response.get('explorers')
                field = 'url'
                type = 'explorer'
        print('\n🌈 We are going to check the following **%s** services' % service)
        for element in elements:
            message = check_http_connection(element.get(field), type)
            print(message, end='\n\n')
            time.sleep(1) # let's breath the client

def do_check_connections(connections):
    print(connections)
    for connection in connections:
        match connection:
            case 'seeds':
                elements = json_response.get('peers').get('seeds')             
            case 'peers':
                elements = json_response.get('peers').get('persistent_peers')
        print('\n🌈 We are going to check the following **%s** connections' % connection)
        for element in elements:
            print('\n' + str(element))
            host = element.get('address')
            hostname = host.split(":")
            node_id = element.get('id')
            provider = element.get('provider')
            message = check_peers_seeds_connection(hostname[0], hostname[1])
            print(message)
            print('    🍌 Node_ID: %s' % (node_id))
            print('    🍌 Provider: %s' % (provider) + '\n')


            time.sleep(1) # let's breath the client
def main():
    # Let's get the JSON file from Github
    chain_registry = bc_chain_registry # BitCanna github
    #chain_registry = cosmos_chain_registry # Cosmos Chain-Registry github
    try:
        response_check = requests.get(chain_registry, headers={"Accept": "application/json"},)
    except:
        conn_error = 'An error occurred getting the info at: ' + chain_registry
        print("\n"+conn_error)
    else:
       global json_response 
       json_response = response_check.json()

    # CHECKS: ['rpcs', 'grpcs', 'lcds', 'explorers', 'archive_nodes', 'state_sync']
    do_checks(['rpcs', 'grpcs', 'lcds', 'explorers', 'archive_nodes', 'state_sync'])
    do_check_connections(['seeds', 'peers'])

if __name__ == "__main__":
    main()
