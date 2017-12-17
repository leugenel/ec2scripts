import boto3
import time
from  botocore.exceptions import ClientError
import EC2VPC
import EC2MyInstances

class AutoScaleGroup():
    GroupName = ""
    LaunchConfName = ""
    DesiredCapacity = 0
    MaxSize = 1
    MinSize = 0
    region = ""
    perf_tag = 'SelPerf'
    __autoscale = None
    __response = ""

    def __init__(self, name, region='us-east-1'):
        self.__autoscale = boto3.client('autoscaling', region)
        self.region = region
        self.GroupName = name

    def find (self, name):
        if self.GroupName == name:
            return True
        return False

    def create(self, name, configuration):
        self.GroupName = name
        self.LaunchConfName = configuration
        try:
            self.__response=self.__autoscale.create_auto_scaling_group(
                AutoScalingGroupName=self.GroupName,
                LaunchConfigurationName=self.LaunchConfName,
                MaxSize=self.MaxSize,
                MinSize=self.MinSize,
                VPCZoneIdentifier=EC2VPC.VPC('vpc-ff34d39a').getFirst()
            )
        except ClientError as ce:
            if ce.response['Error']['Code'] == 'AlreadyExists':
                raise ValueError("Auto Scale Group already exists with the name "+ name)

        self.tag()

    def delete(self):
        self.__autoscale.delete_auto_scaling_group(
            AutoScalingGroupName = self.GroupName,
        )

    def setCapacity(self, capacity):
        try:
            self.__autoscale.set_desired_capacity(
                AutoScalingGroupName=self.GroupName,
                DesiredCapacity=capacity
            )
        except ClientError as ce:
            if ce.response['Error']['Code'] == 'ValidationError':
                raise ValueError("The Auto Scale Group with "+ self.GroupName+ " doesn't exist!" )

    def wait4Capacity(self, capacity):
        new_machines = EC2MyInstances.ec2MyInstances()
        for i in range(1,15):
            new_machines.get_region_instances_by_tag(self.region, self.perf_tag)
            if len(new_machines.instances) >= capacity:
                break
            time.sleep(4)

    def tag(self):
        self.__autoscale.create_or_update_tags(
            Tags=[
                {
                    'ResourceId': self.GroupName,
                    'ResourceType': 'auto-scaling-group',
                    'Key': 'Product',
                    'Value': self.perf_tag,
                    'PropagateAtLaunch': True
                }
            ]
        )

    def getLastResponse(self):
        return self.__response

    def printme(self):
        print "**************Auto Scale Group Info****************"
        print "Auto Scale Group Name: "+ self.GroupName
        print "Launch Configuration: "+ self.LaunchConfName
        print "MaxSize: "+ str(self.MaxSize)
        print "MinSize: "+ str(self.MinSize)
        print "DesiredCapacity: "+ str(self.DesiredCapacity)
        print "**************End Auto Scale Group Info****************"


######################### class AutoScaleGroups #########################################

class AutoScaleGroups():

    asGroups = []
    __autoscale = None
    __region = ""
    __response = ""

    def __init__(self, region='us-east-1'):
        self.__autoscale = boto3.client('autoscaling', region)
        self.__region = region
        self.get_all()


    def get_all (self):
        self.__response = self.__autoscale.describe_auto_scaling_groups()
        if len(self.__response['AutoScalingGroups'])!=0:
            for g in self.__response['AutoScalingGroups']:
                asg = AutoScaleGroup(g['AutoScalingGroupName'], self.__region)
                #asg.GroupName  = g['AutoScalingGroupName']
                asg.LaunchConfName = g["LaunchConfigurationName"]
                asg.MaxSize = g['MaxSize']
                asg.MinSize = g['MinSize']
                asg.DesiredCapacity = g['DesiredCapacity']
                self.asGroups.append(asg)

    def printall(self):
        if self.isEmpty():
            print "No Auto Scale Groups"
            return

        print "*************************************"
        print "We have "+str(len(self.asGroups))+" Auto Scale Groups in "+self.__region
        print "*************************************"
        for m in self.asGroups:
            self.printone(m.GroupName)

    def isEmpty(self):
        if len(self.asGroups):
            return False
        return True

    def printone(self, name):
        indx = self.getIndex(name)
        if indx<0:
            raise ValueError("No instances with name "+name)
        self.asGroups[indx].printme()

    def getIndex(self, name):
        for indx,val in enumerate(self.asGroups):
            if val.GroupName == name:
                return indx
        return -1


    def refresh(self):
        """Refresh the instances info"""
        self.asGroups=[]
        self.get_all()

    def getLastResponse(self):
        return self.__response
