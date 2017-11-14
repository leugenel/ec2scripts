import boto3
import EC2Instance

class ec2MyInstances ():
    """Stub for the instance actions. Deal with the array of instances"""

    instances = []

    def __init__(self):
        """Initialize an instance array"""
        self.get_all_instances()


    def refresh(self):
        """Refresh the instances info"""
        self.instances=[]
        self.get_all_instances()


    def get_region_instances(self, region):
        """Get info about instances in the specific region"""
        ec2 = boto3.client('ec2', region_name=region)
        response = ec2.describe_instances()
        for r in response['Reservations']:
            for i in r['Instances']:
                inst = EC2Instance.ec2Instance()
                inst.Region=region
                inst.ID = i["InstanceId"]
                inst.State = i["State"]["Name"]
                inst.PublicDns = i['PublicDnsName']
                for t in i["Tags"]:
                    inst.Name = t["Value"]
                self.instances.append(inst)


    def get_all_instances(self):
        """Get info about instances in all regions"""
        ec2 = boto3.client('ec2')
        regions = ec2.describe_regions()
        for r in regions['Regions']:
            self.get_region_instances(r["RegionName"])


    def start(self, name):
        """Start the instance by provided instance name. Finding it in the array before"""
        res = []
        for insti in self.instances:
            res = insti.start(name)
            if len(res):
                break
        return res

    def stop(self, name):
        """Stop the instance by provided instance name. Finding it in the array before"""
        res = []
        for insti in self.instances:
            res = insti.stop(name)
            if len(res):
                break
        return res

    def getIndex(self, name):
        for indx,val in enumerate(self.instances):
            if val.Name == name:
                return indx
        return -1
