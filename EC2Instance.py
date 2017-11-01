import boto3
import time

######################### ec2Instance class #########################

class ec2Instance ():
    ID = ""
    Name = ""
    Region = ""
    State = ""
    PublicDns = ""

    def printme(self):
        print self.Region + " : "+ " <<Name>> " +self.Name + " <<instance ID>> " + \
              self.ID+ " <<with the state>> " + self.State + " <<DNS>> " + self.PublicDns

    def start(self, name):
        res=[]
        if name == self.Name:
            ec2 = boto3.client('ec2', self.Region)
            res=ec2.start_instances(
                InstanceIds=[
                    self.ID
                ]
            )
        return res

    def stop(self, name):
        res=[]
        if name == self.Name:
            ec2 = boto3.client('ec2', self.Region)
            res=ec2.stop_instances(
                InstanceIds=[
                    self.ID
                ]
            )
        return res

    def getDns(self, name):
        res=""
        if name == self.Name:
            res=self.PublicDns
        return res

    def refresh(self):
        ec2 = boto3.client('ec2', self.Region)
        response = ec2.describe_instances()
        for r in response['Reservations']:
            for i in r['Instances']:
                for t in i["Tags"]:
                    if self.Name == t["Value"]:
                        self.ID = i["InstanceId"]
                        self.State = i["State"]["Name"]
                        self.PublicDns = i['PublicDnsName']

######################### ec2Actions class #########################

class ec2Actions ():

    instances = []

    def __init__(self):
        self.get_all_instances()

    def refresh(self):
        self.instances=[]
        self.get_all_instances()


    def get_region_instances(self, region):
        ec2 = boto3.client('ec2', region_name=region)
        response = ec2.describe_instances()
        for r in response['Reservations']:
            for i in r['Instances']:
                inst = ec2Instance()
                inst.Region=region
                inst.ID = i["InstanceId"]
                inst.State = i["State"]["Name"]
                inst.PublicDns = i['PublicDnsName']
                for t in i["Tags"]:
                    inst.Name = t["Value"]
                self.instances.append(inst)


    def get_all_instances(self):
        ec2 = boto3.client('ec2')
        regions = ec2.describe_regions()
        for r in regions['Regions']:
            self.get_region_instances(r["RegionName"])


    def start(self, name):
        res = []
        for insti in self.instances:
            res = insti.start(name)
            if len(res):
                break
        return res

    def stop(self, name):
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

######################### usage #########################

machines = ec2Actions()
indx = machines.getIndex("DockerTestEu")
oldState = machines.instances[indx].State

#Start
res=machines.start("DockerTestEu")
print(res)

for i in range(1,15):
    machines.instances[indx].refresh()
    if oldState != machines.instances[indx].State:
        if "ing" not in machines.instances[indx].State or machines.instances[indx].State=="running":
            break
    time.sleep(4)

if indx>0:
    #print the Dns of starting instance
    print (machines.instances[indx].PublicDns)
    #print all info about instance
    print (machines.instances[indx].printme())

#Stop
oldState = machines.instances[indx].State
res=machines.stop("DockerTestEu")
print(res)
#wait 40 sec before it will stop
for i in range(1,15):
    machines.instances[indx].refresh()
    if oldState != machines.instances[indx].State:
        if "ing" not in machines.instances[indx].State or machines.instances[indx].State=="running":
            break
    time.sleep(4)

if indx>0:
    #print the Dns of starting instance
    print (machines.instances[indx].PublicDns)
    #print all info about instance
    print (machines.instances[indx].printme())

#def waitStateChange():
