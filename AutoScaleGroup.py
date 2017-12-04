import boto3
from  botocore.exceptions import ClientError
import EC2VPC

class AutoScaleGroup():
    GroupName = ""
    LaunchConfName = ""
    DesiredCapacity = 0
    MaxSize = 1
    MinSize = 0
    __response = ""

    def find (self, name):
        if self.GroupName == name:
            return True
        return False

    def printme(self):
        print "**************Auto Scale Group Info****************"
        print "Auto Scale Group Name: "+ self.GroupName
        print "Launch Configuration: "+ self.LaunchConfName
        print "MaxSize: "+ str(self.MaxSize)
        print "MinSize: "+ str(self.MinSize)
        print "DesiredCapacity: "+ str(self.DesiredCapacity)
        print "**************End Auto Scale Group Info****************"

class AutoScaleGroups():

    asGroups = []
    __autoscale = None
    __region = ""

    def __init__(self, region='us-east-1'):
        self.__response=self.__autoscale = boto3.client('autoscaling', region)
        self.__region = region
        self.get_all()


    def get_all (self):
        response = self.__autoscale.describe_auto_scaling_groups()
        if len(response['AutoScalingGroups'])!=0:
            for g in response['AutoScalingGroups']:
                asg = AutoScaleGroup()
                asg.GroupName  = g['AutoScalingGroupName']
                asg.LaunchConfName = g["LaunchConfigurationName"]
                asg.MaxSize = g['MaxSize']
                asg.MinSize = g['MinSize']
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

    def create(self, name, configuration):
        try:
            self.__response=self.__autoscale.create_auto_scaling_group(
                AutoScalingGroupName=name,
                LaunchConfigurationName=configuration,
                MaxSize=1,
                MinSize=0,
                VPCZoneIdentifier=EC2VPC.VPC('vpc-ff34d39a').getFirst()
            )
        except ClientError as ce:
            if ce.response['Error']['Code'] == 'AlreadyExists':
                raise ValueError("Auto Scale Group already exists with the name "+ name)

        self.refresh()


    def refresh(self):
        """Refresh the instances info"""
        self.asGroups=[]
        self.get_all()

    def delete(self, name):
        self.__autoscale.delete_auto_scaling_group(
            AutoScalingGroupName = name,
        )
        self.refresh()

    def setCapacity(self, name, capacity):
        self.__response=self.__autoscale.set_desired_capacity(
            AutoScalingGroupName=name,
            DesiredCapacity=capacity
        )
        #update our data
        self.asGroups[self.getIndex(name)].DesiredCapacity=capacity

    def getLastResponse(self):
        return self.__response