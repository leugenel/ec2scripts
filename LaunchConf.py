import boto3
import ECSImages

class Configuration():
    Name = ""
    InstanceType = ""
    ImageId = ""
    KeyName = ""

    def find (self, name):
        if self.Name == name:
            return True
        return False

    def printme(self):
        print "**************LaunchConfiguration Info****************"
        print "Launch Configuration Name: "+ self.Name
        print "Instance type: "+ self.InstanceType
        print "ImageId: "+ self.ImageId
        print "Key Name: "+ self.KeyName
        print "**************End LaunchConfiguration Info****************"

class LaunchConfig():
    Configurations = []
    __region = ""
    __autoscale = None

    def __init__(self, region='us-east-1'):
        self.__autoscale = boto3.client('autoscaling',  region_name=region)
        self.__region=region
        self.get_all()

    def get_all (self):
        response = self.__autoscale.describe_launch_configurations()
        if len(response['LaunchConfigurations'])!=0:
            for lc in response['LaunchConfigurations']:
                conf = Configuration()
                conf.Name = lc['LaunchConfigurationName']
                conf.InstanceType = lc["InstanceType"]
                conf.ImageId = lc['ImageId']
                conf.KeyName = lc['KeyName']
                self.Configurations.append(conf)

    def getIndex(self, name):
        for indx,val in enumerate(self.Configurations):
            if val.Name == name:
                return indx
        return -1

    def printall(self):
        if self.isEmpty():
            print

        print "*************************************"
        print "we have "+str(len(self.Configurations))+" Configurations"
        print "*************************************"
        for m in self.Configurations:
            self.printone(m.Name)

    def printone(self, name):
        indx = self.getIndex(name)
        if indx<0:
            raise ValueError("No instances with name "+name)
        self.Configurations[indx].printme()

    def isEmpty(self):
        if len(self.Configurations):
            return True
        return False

    def getImage(self):
        return ECSImages.ecsImages(self.__region).getImage()

    def create(self, name):
        self.__autoscale.create_launch_configuration(
            IamInstanceProfile='eugene-ecs-selperf-role',
            ImageId=self.getImage(),
            KeyName = 'ApachePerf',
            InstanceType='t2.medium',
            InstanceMonitoring = {'Enabled' : False},
            LaunchConfigurationName=name,
            SecurityGroups=[
                'sg-f7655184',
            ],
        )
        self.refresh()

    def delete(self, name):
        self.__autoscale.delete_launch_configuration(
            LaunchConfigurationName=name,
        )
        self.refresh()

    def refresh(self):
        """Refresh the instances info"""
        self.Configurations=[]
        self.get_all()