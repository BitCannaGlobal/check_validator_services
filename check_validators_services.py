#python3
import requests
import datetime
import time
import os
import json
import socket


lcd_bitcanna='https://lcd.bitcanna.io/cosmos/bank/v1beta1/balances/'
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
    URL = address + '/status?'
    print (' 🌍 Attempting to connect to %s'  % (URL))
    try:
        # print(URL)
        response_check = requests.get(URL, headers={"Accept": "application/json"},)
        print ('    🍌 RESPONSE: %s ' % (response_check))
    except:
        output = 'ERROR. Connection to server:  %s failed' % (URL)
        print('    ⛔ ', end =' ')
    else:
        match json_check:
            case "rpc":
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
            case "lcd":
                print('lcd')

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


if __name__ == "__main__":
    main()
