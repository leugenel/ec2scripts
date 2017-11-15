import boto3

class ecsImages ():
    #Not a full list , add from the following link if required
    #http://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html
    Optimized = {
        "us-east-2":"ami-b0527dd5",
        "us-east-1":"ami-20ff515a",
        "us-west-2":"ami-3702ca4f",
        "us-west-1":"ami-b388b4d3",
        "eu-west-2":"ami-ee7d618a",
        "eu-west-1":"ami-d65dfbaf",
        "eu-central-1":"ami-ebfb7e84"
    }
    __image = ""
    __region = ""

    def __init__(self, region='us-east-1'):
        try:
            self.__image=self.Optimized[region]
        except KeyError:
            raise ValueError("The region you provided is not exists")
        self.__region=region



    def __describe(self):
        if self.__region == "":
            return
        ec2 = boto3.client('ec2', self.__region)
        return ec2.describe_images(
            Filters = [ {
                'Name': 'image-id',
                'Values': [self.__image],
            }],
        )

    def getImage(self):
        return self.__image

    def getRegion(self):
        return self.__region

    def getName(self):
        if self.__region == "":
            return
        resp = self.__describe()
        name=""
        for images in resp['Images']:
            name = images['Name']
        return name

    def getId(self):
        return self.__image