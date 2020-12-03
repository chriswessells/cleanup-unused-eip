# Tag an array of IP Addresses to keep
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


def tag_elastic_ip(ec2_client, eip_allocation_ids, tag_key, tag_value, is_dry_run=False):
    try:
        ec2_client.create_tags(
            DryRun=is_dry_run,
            Resources=eip_allocation_ids,
            Tags=[
                {
                    'Key': tag_key,
                    'Value': tag_value
                }
            ]
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'DryRunOperation':
            return True
        else:
            return False
    return True


# Add ip addresses to be whitelisted
keep_public_ips = []
print('Whitelisting the IP Addresses:')
print(keep_public_ips)
eip_to_tag = [x['AllocationId'] for x in eip_unused if x['PublicIp'] in keep_public_ips]

# tagging all IPs at once
# to tag one at a time
keep_key = 'keep'
keep_value = 'True'
a = tag_elastic_ip(client, eip_to_tag, keep_key, keep_value)
if a:
    print('IP Addresses whitelisted')
