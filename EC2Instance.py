import boto3


class ec2Instance ():
    ID = ""
    Name = ""
    Region = ""
    State = ""


def get_all_running_instances():
    ec2 = boto3.client('ec2')
    regions = ec2.describe_regions()
    for r in regions['Regions']:
        inst=get_running_instances(r["RegionName"])
        if len(inst)>0:
            print r["RegionName"]+" : "
            for a in inst:
                print(a)


def get_running_instances(region):
    instances=[]
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_instances(
        Filters=[
                    {
                        'Name': 'instance-state-name',
                        'Values': [
                            'running',
                        ]
                    },

                ]
    )
    for r in response['Reservations']:
        for i in r['Instances']:
            for t in i["Tags"]:
                instances.append(t["Value"])

    return instances

def get_instance_old(region):
    instances=[]
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_instances()
    for r in response['Reservations']:
        for i in r['Instances']:
            resLine=""
            for t in i["Tags"]:
                resLine = t["Value"]+ " <<instance ID>> " + i["InstanceId"]+ " <<with the state>> " + i["State"]["Name"]
            instances.append(resLine)

    return instances

def get_instance(region):
    inst = ec2Instance()
    inst.Region=region
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_instances()
    for r in response['Reservations']:
        for i in r['Instances']:
            for t in i["Tags"]:
                inst.ID = i["InstanceId"]
                inst.Name = t["Value"]
                inst.State = i["State"]["Name"]

    return inst



def get_all_instances():
    ec2 = boto3.client('ec2')
    regions = ec2.describe_regions()
    for r in regions['Regions']:
        inst=get_instance(r["RegionName"])
        if len(inst.Name)>0:
            #print r["RegionName"]+" : "
            print inst.Region + " : "
            #for a in inst:
            #    print(a)
            print inst.Name + " <<instance ID>> " + inst.ID+ " <<with the state>> " + inst.State

#inst = get_running_instances("eu-west-1")
#get_all_running_instances()
get_all_instances()
