"""
    This module allows stop/start and describe EC2 instances
    Usage from the command line:
    <python EC2Instance.py> prints all instances in all regions
    <python EC2Instance.py --h> shows the arguments
    <python EC2Instance.py -name instance_name> - describe instance_name
    <python EC2Instance.py -name instance_name -action> allows start or stop the instance_name.
"""
import time
import argparse
import EC2MyInstances


def waitStateChange(machines, indx):
    if indx <= 0:
        return
    oldState = machines.instances[indx].State
    for i in range(1,15):
        machines.instances[indx].refresh()
        if oldState != machines.instances[indx].State:
            if "ing" not in machines.instances[indx].State or machines.instances[indx].State=="running":
                break
        time.sleep(4)


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
        for m in machines.instances:
            m.printme()
        return

    #If no action print info about instance
    if not args.action and args.name:
        indx = machines.getIndex(args.name)
        if indx<0:
            print "No instances with name "+args.name
            return
        machines.instances[indx].printme()


    if args.action == "start" and args.name:
        indx = machines.getIndex(args.name)
        if indx<0:
            print "No instances with name "+args.name
            return
        res=machines.start(args.name)
        print(res)
        waitStateChange(machines, indx)
        #print all info about instance
        print (machines.instances[indx].printme())

    if args.action == "stop" and args.name:
        #Stop
        indx = machines.getIndex(args.name)
        if indx<0:
            print "No instances with name "+args.name
            return
        res=machines.stop(args.name)
        print(res)
        waitStateChange(machines, indx)
        print (machines.instances[indx].printme())


#invoke main
if __name__ == "__main__":
    main()
