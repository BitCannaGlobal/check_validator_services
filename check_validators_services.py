#python3
import requests
# import datetime
import time
import socket


lcd_info = '/cosmos/base/tendermint/v1beta1/node_info'
lcd_syncing = '/cosmos/base/tendermint/v1beta1/syncing'
app_version = '2.0.3'
rpc_info = '/status?'
chain_registry = 'https://raw.githubusercontent.com/BitCannaGlobal/bcna/main/chain-registry.json'


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
            try:
                # print(URL)
                response_check = requests.get(address, headers={'Accept': '*/*', 'Content-Type': '*/*'},  timeout=5)
                print ('    🍌 RESPONSE: %s ' % (response_check))
            except:
                output = 'ERROR. Connection to server:  %s failed' % (address)
                print('    ⛔ ', end =' ')
            else:
                output = 'Connection to GRPC is successfully done.'
                print('    🟢 ', end =' ')
    return output

def check_seeds():
    seeds = json_response.get('peers').get('seeds')
    print('\n🌈 We are going to check the following SEEDS:\n')
    for seed in seeds:
        # print('\n' + str(seed))
        host = seed.get('address')
        hostname = host.split(":")
        message = check_peers_seeds_connection(hostname[0], hostname[1])
        print(message)
        node_id = seed.get('id')
        print('    🍏 Node_ID provided: %s' % (node_id) + '\n')        

def check_persistent_peers(): #check connection
    ppers = json_response.get('peers').get('persistent_peers')
    print('\n🌈 We are going to check the following PERSISTENT PEERS:\n')
    for peers in ppers:
        # print('\n' + str(peers))
        host = peers.get('address')
        hostname = host.split(":")
        message = check_peers_seeds_connection(hostname[0], hostname[1])
        print(message)
        node_id = peers.get('id')
        print('    🍏 Node_ID provided: %s' % (node_id) + '\n')            

def check_rpc(): #rpc: connection, tx_index active, prune strategy, voting power
    rpcs = json_response.get('apis').get('rpc')
    print('\n🌈 We are going to check the following RPC servers:\nGathered data: node_id, moniker, tx_index, synced, voting_power (is validator?)\n')
    # print('\n' + str(rpcs))
    for rpc in rpcs:
        message = check_http_connection(rpc.get('address'), 'rpc')
        print(message, end='\n\n')
        time.sleep(1) # let's breath the client

def check_grpc():
    grpcs = json_response.get('apis').get('grpc')
    print('\n🌈 We are going to check the following GRPC servers:\n')
    # print('\n' + str(grpcs))
    for grpc in grpcs:
        message = check_http_connection(grpc.get('address'), 'grpc')
        print(message, end='\n\n')
        time.sleep(1) # let's breath the client

def check_archive_nodes(): #archive_nodes: connection, prune strategy, sinced, voting power
    archives = json_response.get('archive_nodes')
    print('\n🌈 We are going to check the following RPC Archive Nodes:\nGathered data: node_id, moniker, synced, voting_power (is validator?)\n')
    # print('\n' + str(archives))
    for archive in archives:
        message = check_http_connection(archive.get('address'), 'archive_nodes')
        print(message, end='\n\n')
        time.sleep(1) # let's breath the client

def check_explorer(): # check if an explorer is alive or not
    explorers = json_response.get('explorers')
    print('\n🌈 We are going to check connectivity of the following EXPLORERS:\n')
    # print('\n' + str(explorers))
    for explorer in explorers:
        message = check_http_connection(explorer.get('url'), 'grpc')
        print(message, end='\n\n')
        time.sleep(1) # let's breath the client

def check_lcd():
    lcds = json_response.get('apis').get('rest')
    print('\n🌈 We are going to check the following LCD servers:\nGathered data: node_id, moniker, tx_index, synced, voting_power (is validator?)\n')
    # print('\n' + str(lcds))
    for lcd in lcds:
        message = check_http_connection(lcd.get('address'), 'lcd')
        print(message, end='\n\n')
        time.sleep(1) # let's breath the client


def main():
    # Let's get the JSON file from Github
    try:
        response_check = requests.get(chain_registry, headers={"Accept": "application/json"},)
    except:
        conn_error = 'An error occurred getting the info at: ' + chain_registry
        print("\n"+conn_error)
    else:
       global json_response 
       json_response = response_check.json()
    check_seeds()
    check_persistent_peers()
    check_rpc()
    check_grpc()
    check_archive_nodes()
    check_explorer()
    check_lcd()

if __name__ == "__main__":
    main()
