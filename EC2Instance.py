import boto3


class ec2Instance ():
    ID = ""
    Name = ""
    Region = ""
    State = ""

    def printme(self):
        print self.Region + " : "
        print self.Name + " <<instance ID>> " + self.ID+ " <<with the state>> " + self.State

    def findByName(self, name):
        if name == self.Name:
            return True
        return False

#########################

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
    instances = []
    ec2 = boto3.client('ec2')
    regions = ec2.describe_regions()
    for r in regions['Regions']:
        inst=get_instance(r["RegionName"])
        if len(inst.Name)>0:
            instances.append(inst)
            inst.printme()
    return instances

instances = get_all_instances()

for i in instances:
    if i.findByName("DenverXLarge"):
        print i.ID