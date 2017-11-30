import boto3

class VPC():
    vpc = []
    indx = 0

    def __init__(self, vpcId):
        ec2_res = boto3.resource('ec2')
        for subnet in ec2_res.Vpc(vpcId).subnets.all():
            self.vpc.append(subnet.id)
        if len(self.vpc)==0:
            raise ValueError("The subnets are not exist")


    def getFirst(self):
         return  self.vpc[0]

    def isLast(self):
         return (self.indx == len(self.vpc)-1)

    def isFirst(self):
        return (self.indx == 0)

    def getNext(self):
         self.indx = self.indx+1
         return self.vpc[self.indx]

    def getPrev(self):
        self.indx = self.indx-1
        if self.isFirst():
            self.indx = 0
            return self.getFirst()
        return self.vpc[self.indx]

    def reset(self):
        self.indx = 0