import boto3
import time
import EC2Instance


class ec2MyInstances ():
    """Stub for the instance actions. Deal with the array of instances"""

    instances = []

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


    def start(self, instanceName):
        """Start the instance by provided instance name. Finding it in the array before"""
        indx = self.getIndex(instanceName)
        if indx<0:
            raise ValueError("No instances with name "+instanceName)
        self.instances[indx].start(self.instances[indx].Name)
        self.verifyStateChange("running", instanceName)
        self.instances[indx].printme()

    def stop(self, instanceName):
        """Stop the instance by provided instance name. Finding it in the array before"""
        indx = self.getIndex(instanceName)
        if indx<0:
            raise ValueError("No instances with name "+instanceName)
        self.instances[indx].stop(self.instances[indx].Name)
        self.verifyStateChange("stopped", instanceName)
        self.instances[indx].printme()

    def getIndex(self, name):
        for indx,val in enumerate(self.instances):
            if val.Name == name:
                return indx
        return -1

    def printall(self):
        for m in self.instances:
            self.printone(m.Name)

    def printone(self, instance):
        indx = self.getIndex(instance)
        if indx<0:
            raise ValueError("No instances with name "+instance)
        self.instances[indx].printme()

    def verifyStateChange(self,  afterState, instance):
        indx = self.getIndex(instance)
        if indx <= 0:
            raise ValueError("No instances with name "+instance)
        for i in range(1,15):
            self.instances[indx].refresh()
            if self.instances[indx].State == afterState:
                break
            time.sleep(4)

