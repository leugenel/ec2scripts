"""
    This module allows stop/start and describe EC2 instances
    Usage from the command line:
    <python EC2Instance.py> prints all instances in all regions
    <python EC2Instance.py --h> shows the arguments
    <python EC2Instance.py -name instance_name> - describe instance_name
    <python EC2Instance.py -name instance_name -action> allows start or stop the instance_name.
"""
import argparse
import EC2MyInstances

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-name", help="Instance name")
    parser.add_argument("-action", help="start stop for instance")
    args = parser.parse_args()

    if args.action and args.action not in ("start", "stop"):
        print "Please provide action start or stop"
        return

    machines = EC2MyInstances.ec2MyInstances()

    #If no argument will print info about all instances
    if not args.action and not args.name:
        machines.printall()
        return

    #If no action print info about instance
    if not args.action and args.name:
        machines.printone(args.name)

    if args.action == "start" and args.name:
        machines.start(args.name)

    if args.action == "stop" and args.name:
        machines.stop(args.name)


#invoke main
if __name__ == "__main__":
    main()