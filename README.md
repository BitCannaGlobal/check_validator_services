# check_validator_services
A simple tool to check validators' services

## The services that are going to be checked in a randomized date (maybe two or three times by week) are:

* Seed nodes (connectivity*)
* Persistent Nodes (connectivity)
* RPC public servers (connectivity* + node_id + tx_index active* +  synced* + voting_power(is validator or not)* )
* GRPC (connectivity*)
* REST(LCD)  (connectivity* + prune strategy + synced* + bcnad version* + node_id)
* Explorer (connectivity* +  prune strategy*)
* Archive_nodes (connectivity* + prune strategy*)


NOTE: *marked is valuable for delegations

## A photo paints a thousand words
<img width="900" alt="image" src="https://github.com/BitCannaGlobal/check_validator_services/assets/3751926/d314dc10-5bdc-4014-9105-ca561dd3d800">


