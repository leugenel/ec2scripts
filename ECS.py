import boto3

cluster_name = 'eugene-ecs-selperf'
ecs_client = boto3.client(
    'ecs',
     region_name='us-east-1'
)

response = ecs_client.describe_clusters(
    clusters=[cluster_name]
)

print "Cluster name: " + cluster_name
for clusters in response['clusters']:
    print "status: "+ clusters['status']
    print "Container Instance Count: "+ str(clusters['registeredContainerInstancesCount'])
    print "Pending Tasks: "+ str(clusters['pendingTasksCount'])
    print "Running Tasks: "+ str(clusters['runningTasksCount'])
    print "Active Services Count: "+ str(clusters['activeServicesCount'])




ec2 = boto3.client('ec2', region_name='us-east-1')

response=ec2.describe_images(
     Filters = [ {
        'Name': 'name',
        'Values': [
            'amzn-ami-2017.09.a-amazon-ecs-optimized'
        ],
     }],
)

#response = ecs_client.list_clusters()
print response