import boto3


class Cluster():
    Name = ""
    Status = ""
    PendingTasksCount = 0
    RunningTasksCount = 0
    ActiveServicesCount = 0
    __ecs = None
    __response = ""

    def __init__(self, name, region='us-east-1'):
        self.region = region
        self.Name = name

    def describe(self):
        self.__ecs = boto3.client('ecs', self.region)
        self.__response = self.__ecs.describe_clusters(
            clusters=[self.Name]
        )
        cluster = self.__response['clusters'][0]
        self.Status = cluster['status']
        self.PendingTasksCount = cluster['pendingTasksCount']
        self.RunningTasksCount = cluster['runningTasksCount']
        self.ActiveServicesCount =  cluster['activeServicesCount']

    def printme(self):
        print "**************Cluster****************"
        print "Cluster name: " + self.Name
        print "status: "+ self.Status
        print "Pending Tasks: "+ str(self.PendingTasksCount)
        print "Running Tasks: "+ str(self.RunningTasksCount)
        print "Active Services Count: "+ str(self.ActiveServicesCount)
        print "**************End Cluster Info****************"

    def getLastResponse(self):
        return self.__response

######################### class Clusters #########################################

class Clusters():
    ActiveClusters = []
    __ecs = None
    __region = ""
    __response = ""

    def __init__(self, region='us-east-1'):
        self.__ecs = boto3.client('ecs', region)
        self.__region = region
        self.get_all()

    def get_all (self):
        all_response = self.__ecs.list_clusters()
        if len(all_response['clusterArns'])==0:
            print "No clusters found"
            return
        for one in all_response['clusterArns']:
            self.__response = self.__ecs.describe_clusters(
                clusters=[one]
            )
            cluster = self.__response['clusters'][0]
            one_cluster = Cluster(cluster['clusterName'], self.__region)
            one_cluster.Status = cluster['status']
            one_cluster.PendingTasksCount = cluster['pendingTasksCount']
            one_cluster.RunningTasksCount = cluster['runningTasksCount']
            one_cluster.ActiveServicesCount =  cluster['activeServicesCount']
            self.ActiveClusters.append(one_cluster)

    def printall(self):
        if len(self.ActiveClusters) == 0:
            print "No Clusters in "+ self.__region
            return

        print "*************************************"
        print "We have "+str(len(self.ActiveClusters))+" Clusters "+self.__region
        print "*************************************"
        for ac in self.ActiveClusters:
            ac.printme()

    def getLastResponse(self):
        return self.__response