#python3
import requests
from time import sleep, strftime
import socket
import os
import sqlite3
from contextlib import closing


lcd_info = '/cosmos/base/tendermint/v1beta1/node_info'
lcd_syncing = '/cosmos/base/tendermint/v1beta1/syncing'
app_version = '2.0.3'
rpc_info = '/status?'
bc_chain_registry = 'https://raw.githubusercontent.com/BitCannaGlobal/bcna/main/chain-registry.json'
bc_testnet = 'https://raw.githubusercontent.com/BitCannaGlobal/bcna/main/devnets/bitcanna-dev-1/chain-registry.json'
cosmos_chain_registry = 'https://raw.githubusercontent.com/cosmos/chain-registry/master/bitcanna/chain.json'

PATH = './'
LOG_FILE = 'VIP_checks.csv'
DATABASE = 'VIP.db'

def check_peers_seeds_connection(address, port):
 
    # Create a TCP socket
    timeout = 5 #timeout in seconds
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    print (' 🌍 Attempting to connect to %s on port %s' % (address, port))
    try:
        s.connect((address, int(port)))
        output = 'Connected to %s on port %s' % (address, port)
        print('    🟢  %s' % output)
        result = 1
    except socket.error as error:
        output = 'Connection to %s on port %s failed: %s' % (address, port, error)
        print('    ⛔ %s' % output)
        result = 0
    finally:
        s.close()
    return result

def check_http_connection(address, json_check, owner, extra):
    match json_check:
        case "rpc":
            if extra == '':
                extra_info = 'No extra info: '
                url_doc = ''
            else:
                url_doc = ' - URL DOC: ' + extra
            URL = address + rpc_info
            print (' 🌍 Attempting to connect to %s'  % (URL))
            try:
                # print(URL)
                response_check = requests.get(URL, headers={"Accept": "application/json"}, timeout=5)
                print ('    🍌 RESPONSE: %s ' % (response_check))
                if response_check.status_code != 200:
                    extra_info = 'ERROR. Status code at server:  %s is: %s   failed' % (URL, str(response_check.status_code))
                    print('    ⛔ ' + extra_info)
                    result = 0
                    pass               
            except:
                extra_info = 'ERROR. Connection to server:  %s failed' % (URL)
                print('    ⛔ ', end =' ')
                result = 0
            else:
                try:
                    json_response = response_check.json()
                except:
                    json_error = 'An error occurred getting the JSON data'
                    print('    ⛔ ', end =' ')
                    extra_info = extra_info + ' - ' + json_error + url_doc
                    result = 0
                else:        
                    json_response = response_check.json()
                    result = 1
                    id = json_response["result"]["node_info"]["id"]
                    moniker_raw = json_response["result"]["node_info"]["moniker"]
                    moniker = moniker_raw.replace("'", " ")
                    tx_index = json_response["result"]["node_info"]["other"]["tx_index"]
                    syncing = json_response["result"]["sync_info"]["catching_up"]
                    voting_power = json_response["result"]["validator_info"]["voting_power"]
                    if int(voting_power) > 0:
                        print('    ❗ This public RPC is running in a MainNET Validator ❗')
                    if syncing != False:
                        print('    ❗ This public RPC is NOT SYNCED at MainNET ❗')
                    if tx_index != 'on':
                        print('    ❗ This public RPC has not activated the TX Index ❗')
                    print('    🟢', end =' ')
                    extra_info = 'Moniker: ' + moniker + ' - Syncing: ' + str(syncing) + ' - TX_Index: ' + str(tx_index) + ' - Voting Power: ' + str(voting_power)
            output = json_check + ',' + str(result) + ',' + owner + ',' + URL + ',' + extra_info + url_doc
        case "archive_nodes":
            extra_info = 'No extra info: '
            URL = address + rpc_info
            print (' 🌍 Attempting to connect to %s'  % (URL))
            try:
                # print(URL)
                response_check = requests.get(URL, headers={"Accept": "application/json"}, timeout=5)
                print ('    🍌 RESPONSE: %s ' % (response_check))
            except:
                extra_info = 'ERROR. Connection to server:  %s failed' % (URL)
                print('    ⛔ ', end =' ')
                result = 0
            else:
                try:
                    json_response = response_check.json()
                except:
                    json_error = 'An error occurred getting the JSON data'
                    print('    ⛔ ', end =' ')
                    extra_info = extra_info + ' - ' + json_error
                    result = 0
                else:        
                    json_response = response_check.json()
                    result = 1
                    id = json_response["result"]["node_info"]["id"]
                    moniker_raw = json_response["result"]["node_info"]["moniker"]
                    moniker = moniker_raw.replace("'", " ")
                    syncing = json_response["result"]["sync_info"]["catching_up"]
                    earliest_block = json_response["result"]["sync_info"]["earliest_block_height"]
                    voting_power = json_response["result"]["validator_info"]["voting_power"]
                    #output = id, moniker, synced, earliest_block, voting_power
                    if int(voting_power) > 0:
                        print('    ❗ This public RPC is running in a MainNET Validator ❗')
                    if syncing != False:
                        print('    ❗ This public RPC is NOT SYNCED at MainNET ❗')
                    if int(earliest_block) != 1:
                        print('    ❗❗ This Archive Node does not sync the whole chain ❗❗')
                        result = 0
                    else:
                        print('    🟢 This Archive Node syncs the whole chain')
                    extra_info = 'Moniker: ' + moniker + ' - Syncing: ' + str(syncing) + ' - Earliest Block: ' + str(earliest_block) + ' - Voting Power: ' + str(earliest_block) 
            output = json_check + ',' + str(result) + ',' + owner + ',' + URL + ',' + extra_info
        case "explorer":
            URL = address
            print (' 🌍 Attempting to connect to %s'  % (URL))
            try:
                response_check = requests.get(URL, headers={"Accept": "application/json"}, timeout=5)
                print ('    🍌 RESPONSE: %s ' % (response_check))
            except:
                output = 'ERROR. Connection to server:  %s failed' % (URL)
                result = 0
                print('    ⛔ ', end =' ')
            else:
                print('    🟢 ', end =' ')
                output = 'Connected'
                result = 1
            url_to_check = extra.replace('${txHash}', '638BE404C6496C86262D6AA7734F170EBFDA04F076CCC592EFF7ED71C31DFA89' )
            output = json_check + ',' + str(result) + ',' + owner + ',' + url_to_check + ',' + output
        case "lcd":
            result = 0
            extra_info = 'No extra info: '
            URL = address + lcd_info
            print (' 🌍 Attempting to connect to %s'  % (URL))
            try:
                # print(URL)
                response_check = requests.get(URL, headers={"Accept": "application/json"}, timeout=5)
                print ('    🍌 RESPONSE: %s ' % (response_check))
            except:
                extra_info = 'ERROR. Connection to server:  %s failed' % (URL)
                print('    ⛔ ', end =' ')
                result = 0
            else:
                try:
                    json_response = response_check.json()
                except:
                    json_error = 'An error occurred getting the JSON Node data'
                    print('    ⛔ ', end =' ')
                    extra_info = extra_info + ' - ' + json_error
                    result = 0
                else:        
                    json_response = response_check.json()
                    result = 1
                    try:
                        id = json_response["default_node_info"]["default_node_id"]
                    except:
                        result = 0
                        message = json_response["message"]
                        extra_info = "ERROR: " + message
                    else:
                        moniker_raw = json_response["default_node_info"]["moniker"]
                        moniker = moniker_raw.replace("'", " ")
                        tx_index = json_response["default_node_info"]["other"]["tx_index"]
                        version = json_response["application_version"]["version"]
                        if version != app_version:
                            print('    ❗ This public LCD is not running the last version of the BCNA software ❗')
                        if tx_index != 'on':
                            print('    ❗ This public LCD has not activated the TX Index ❗')
                        print('    🟢', end =' ')
                        extra_info = 'Moniker: ' + moniker + ' - TX_Index: ' + tx_index + ' - Version: ' + version
            output_connection = json_check + ',' + str(result) + ',' + owner + ',' + URL + ',' + extra_info
            # check the syncing
            URL = address + lcd_syncing
            print ('Checking SYNCING at %s'  % (URL))
            sleep(1)
            try:
                # print(URL)
                response_check = requests.get(URL, headers={"Accept": "application/json"}, timeout=5)
                print ('    🍌 RESPONSE: %s ' % (response_check))
            except:
                error = 'ERROR. Connection to server:  %s failed' % (URL)
                print('    ⛔ ', end =' ')
                output = output_connection + ' - Syncing: ' + error
            else:
                try:
                    json_response = response_check.json()
                except:
                    syncing_json_error = 'An error occurred getting the JSON Syncing data'
                    print('    ⛔ ', end =' ')
                    output = output_connection + ' - Syncing: ' + syncing_json_error
                else:
                    if result == 1:
                        json_response = response_check.json()
                        syncing  = json_response["syncing"]
                        output = output_connection + ' - Syncing: ' + str(syncing)
                        if syncing != False:
                            print('    ❗ This public LCD is NOT SYNCED at MainNET ❗')
                        print('    🟢', end =' ')
                    else:
                        output = output_connection + "- Syncing: ERROR, it can't be checked"
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
                result = 1
                print('    🟢 ', end =' ')
            else:
                output = 'ERROR. Connection to server:  %s failed' % (address)
                result = 0
                print('    ⛔ ', end =' ')
            output = json_check + ',' + str(result) + ',' + owner + ',' + cmd + ',' + output      
    return output

def do_checks(services):
    print(services)
    for service in services:
        match service:
            case 'lcds':
                elements = json_response.get('apis').get('rest')
                field = 'address'
                type = 'lcd'
                validator = 'provider'
                extra = ''          
            case 'grpcs':
                elements = json_response.get('apis').get('grpc')
                field = 'address'
                type = 'grpc'
                validator = 'provider'
                extra = ''
            case 'rpcs':
                elements = json_response.get('apis').get('rpc')
                field = 'address'
                type = 'rpc'
                validator = 'provider'
                extra = ''
            case 'archive_nodes':
                elements = json_response.get('archive_nodes')
                field = 'address'
                type = 'archive_nodes'
                validator = 'provider'
                extra = ''
            case 'state_sync':
                elements = json_response.get('state_sync')
                field = 'address'
                type = 'rpc'
                validator = 'provider'
                extra = 'url_doc'
            case 'explorers':
                elements = json_response.get('explorers')
                field = 'url'
                type = 'explorer'
                validator = 'kind'
                extra = 'tx_page'
        print('\n🌈 We are going to check the following **%s** services' % service)
        for element in elements:
            if extra != '':
                message = check_http_connection(element.get(field), type, element.get(validator), element.get(extra))
            else:
                message = check_http_connection(element.get(field), type, element.get(validator), extra)
            print('', end='\n\n')
            ### Loging
            log_this(message)
            database_save(message)
            sleep(1) # let's breath the client

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
            result = check_peers_seeds_connection(hostname[0], hostname[1])
            print('    🍌 Node_ID: %s' % (node_id))
            print('    🍌 Provider: %s' % (provider) + '\n')
            extra_info = 'Node_ID: ' + node_id
            ### Loging
            cmd = 'telnet ' + hostname[0] + ' ' +  hostname[1]
            message = connection + ',' + str(result) + ',' + provider + ',' + cmd + ',' + extra_info 
            log_this(message)
            database_save(message)
            sleep(1) # let's breath the client

def log_this(log_info):
    string_to_log = strftime('%d-%m-%Y-%H:%M') + ',' + log_info + '\n'
    file_log = open(PATH + LOG_FILE, "a")
    file_log.write (string_to_log)

def database_save(data):
    fields = data.split(',')
    current_date = strftime('%d-%m-%Y-%H:%M') 
    sql_sentence = "INSERT INTO services VALUES ('"+fields[0]+"','"+fields[1]+"','"+fields[2]+"','"+fields[3]+"','"+fields[4]+"', '" + current_date + "')"
    #print(sql_sentence)
    with closing(sqlite3.connect(DATABASE)) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute(sql_sentence)
            connection.commit()


def main():
    # Let's get the JSON file from Github
    chain_registry = bc_chain_registry # BitCanna github
    # chain_registry = bc_testnet # BitCanna-dev-1 
    # chain_registry = cosmos_chain_registry # Cosmos Chain-Registry github
    try:
        response_check = requests.get(chain_registry, headers={"Accept": "application/json"},)
    except:
        conn_error = 'An error occurred getting the info at: ' + chain_registry
        print("\n"+conn_error)
    else:
       global json_response 
       json_response = response_check.json()

    do_checks(['rpcs', 'grpcs', 'lcds', 'explorers', 'archive_nodes', 'state_sync']) #---> BitCanna Github
    # do_checks(['rpcs', 'grpcs', 'lcds', 'explorers']) #--> Cosmos Github
    # do_checks(['state_sync'])

    do_check_connections(['seeds', 'peers'])

if __name__ == "__main__":
    main()  
    # TO-DO: check if the CSV file exist, if not, create it with this headers 
    # column_names = ['Timestamp', 'NodeType', 'Status', 'NodeName', 'ConnectionAddress', 'NodeID']
    #
    # Make the same with DB. Create the file and structure if doesn't exist 
