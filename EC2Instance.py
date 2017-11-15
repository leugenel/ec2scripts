
import boto3

class ec2Instance ():
    """EC2 Instance, allows start, stop the instance"""
    ID = ""
    Name = ""
    Region = ""
    State = ""
    PublicDns = ""

    def printme(self):
        """Prints instance most important info"""
        print self.Region + " : "+ " <<Name>> " +self.Name + " <<instance ID>> " + \
              self.ID+ " <<with the state>> " + self.State + " <<DNS>> " + self.PublicDns

    def start(self, name):
        """Start the instance by provided instance name"""
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
        """Stop the instance by provided instance name"""
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
        """Get the instance URL by provided instance name"""
        res=""
        if name == self.Name:
            res=self.PublicDns
        return res

    def refresh(self):
        """Refresh info about instance"""
        ec2 = boto3.client('ec2', self.Region)
        response = ec2.describe_instances()
        for r in response['Reservations']:
            for i in r['Instances']:
                for t in i["Tags"]:
                    if self.Name == t["Value"]:
                        self.ID = i["InstanceId"]
                        self.State = i["State"]["Name"]
                        self.PublicDns = i['PublicDnsName']
