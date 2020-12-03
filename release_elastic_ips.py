# release unused IP addresses that are not flagged
import boto3
import botocore

client = boto3.client('ec2')


eip_in_use = []
eip_unused = []
for address in client.describe_addresses()['Addresses']:
    if 'AssociationId' in address.keys():
        eip_in_use.append(address)
    else:
        eip_unused.append(address)


def release_elastic_ip(ec2_client, address_obj, is_dry_run=False):
    try:
        ec2_client.release_address(
            AllocationId=address_obj['AllocationId'],
            DryRun=is_dry_run
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'DryRunOperation':
            return True
        else:
            return False
    return True


def flagged(tag_list, key):
    flagged_tags = [x for x in tag_list if x['Key'] == key]
    if flagged_tags:
        return True
    return False


def ips_not_flagged(address_list, flag_key):
    ips = []
    for address in address_list:
        if 'Tags' in address.keys() and not flagged(address['Tags'], flag_key):
            ips.append(address)
        if 'Tags' not in address.keys():
            ips.append(address)
    return ips


keep_key = 'keep'
ips_to_release = ips_not_flagged(eip_unused, keep_key)

print('releasing addresses:')
print([x['PublicIp'] for x in ips_to_release])
for address in ips_to_release:
    released = release_elastic_ip(client, address)
    if released:
        print(f'Address released: {address["PublicIp"]}')
