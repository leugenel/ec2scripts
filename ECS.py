import boto3
import ECSImages
import LaunchConf

cluster_name = 'eugene-ecs-selperf'
ecs_client = boto3.client(
    'ecs',
     region_name='us-east-1'
)

print "**************Clusters****************"

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


ec2 = boto3.client('ec2')  #, region_name='us-east-1')
ecs_im = ECSImages.ecsImages('us-east-1')
print "**************ECS Images in us-east-1****************"
print "Image name: "+ecs_im.getName()
print "ImageID: " + ecs_im.getId()


autoscale = boto3.client('autoscaling',  region_name='us-east-1')
response = autoscale.describe_auto_scaling_groups()
print "***************AutoScalingGroups***************"
if len(response['AutoScalingGroups'])==0:
    print "AutoScalingGroups are empty"
else:
    print response

launchConf = LaunchConf.LaunchConfig('us-east-1')
launchConf.printall()
launchConf.create('eugene_launch_config_create')
launchConf.printall()
launchConf.delete('eugene_launch_config_create')
launchConf.printall()



#    print "AutoScalingGroups are empty"
#else:
#print response