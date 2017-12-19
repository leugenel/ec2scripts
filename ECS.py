import boto3
import ECSImages
import LaunchConf
import EC2VPC
import AutoScaleGroup
import EC2MyInstances
import ECSClusters


#Scenario and Action Items
#We assume that nothing not ready and verify if exists something
#0. Region - currently we are in N.Virginia - us-east-1
#1. ECS Cluster.
# We have to clusters default and eugene-ecs-selperf
# AI: the test currently works with default we need configure EC2 launch configuration User Data in the way (already in the code)
# that will work with the eugene-ecs-selperf cluster.
# We need verify that the cluster eugene-ecs-selperf exists
#2. Launch configuration
# AI: Need create the new one that will work with the predefined cluster
# Then verify that this launch configuration exists
#3. Auto Scaling Group
# AI: Need create one with LC from #2
# Then verify that the ASG is exists
# Need set the desired capacity to 1 at least for one machine
#4. Task definition.
# AI: Create class that will aloows to create the required task definition.
#Currently we have selperf:3 that was verifyied manually
#The most important thing this is memory = 500 MiB
#5. Cluster Task. This will launch the required docker
# AI: Create Class
#6. AI: Need divide the main file to two files
# One configuration that goes to all configuration and check that the configuration is ok
# Nedd think about the property file that includes all required names
#Second launch file that changes the capacity and launch the task
#7. AI: Need find the mechanism for the passing parameters to the docker







# cluster_name = 'eugene-ecs-selperf'
# ecs_client = boto3.client(
#     'ecs',
#      region_name='us-east-1'
# )
#
# print "**************Clusters****************"
#
# response = ecs_client.describe_clusters(
#     clusters=[cluster_name]
# )
#
# print "Cluster name: " + cluster_name
# for clusters in response['clusters']:
#     print "status: "+ clusters['status']
#     print "Container Instance Count: "+ str(clusters['registeredContainerInstancesCount'])
#     print "Pending Tasks: "+ str(clusters['pendingTasksCount'])
#     print "Running Tasks: "+ str(clusters['runningTasksCount'])
#     print "Active Services Count: "+ str(clusters['activeServicesCount'])

clusters = ECSClusters.Clusters()
clusters.printall()

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