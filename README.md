# Example for releasing many unattached Elastic IP Addresses

The scripts are an example to solve a specific problem; when you have some unattached elastic IP addresses you want to
maintain and then release all the remaining unattached elastic IP addresses.

## Requirements

Python and boto3
## whitelist_elastic_ips.py

Edit the script adding a string array of IP Addresses to tag with a Key Value pair. Run the script and it will
tag all unattached elastcip IPs that match.

You can perform a permissions check by passing the parameter True as the last argument to the function
`tag_elastic_ip()`

## release_elastic_ips.py

Edit the script adding the key name used in the whitelist_elastic_ips.py. Run the script and it will release the
unattached elastic IPs that do not have the key tag defined in the script.

You can perform a permissions check by passing the parameter True as the last argument to the function
`release_elastic_ip()`

## DISCLAIMER

Read through the scripts and execute at your own risk. The scripts will release elastic ips from your AWS account.
Read through the scripts so you know what they are doing prior to executing the scripts.
