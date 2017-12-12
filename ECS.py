import boto3
import ECSImages
import LaunchConf
import EC2VPC
import AutoScaleGroup
import EC2MyInstances

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

asgroups = AutoScaleGroup.AutoScaleGroups()
asgroups.printall()
#asgroup.create('selperf_asg','launch_config_m3')
#asgroup.printall()
#asgroup.delete('selperf_auto_scaling')
#asgroup.printall()

as_my_group = AutoScaleGroup.AutoScaleGroup('selperf_asg', 'us-east-1')

capacity = 0
try:
    as_my_group.setCapacity(capacity)
except ValueError:
    print as_my_group.getLastResponse()

as_my_group.tag()

as_my_group.wait4Capacity(capacity)

perf_machines = EC2MyInstances.ec2MyInstances()

perf_machines.get_region_instances_by_tag('us-east-1', 'SelPerf')

perf_machines.printall()

#response = asgroup.getLastResponse()

# for g in response['AutoScalingGroups']:
#     if len(g['Instances'])!=0:
#         for i in g['Instances']:
#             print i['InstanceId']

#print "========After Capacity update=========="
#asgroup.printall()

#TO DO
#Add Instances to AutoScale group




#    print "AutoScalingGroups are empty"
#else:
#print response