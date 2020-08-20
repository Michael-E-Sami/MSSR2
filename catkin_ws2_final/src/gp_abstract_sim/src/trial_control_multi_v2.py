#!/usr/bin/env python

import math
import os.path
from math import atan2, cos, pi, pow, sin, sqrt

import rospy
from geometry_msgs.msg import Point
from gp_abstract_sim.msg import path_points
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32, String
from tf.transformations import euler_from_quaternion

###########################################################################

whichDitto = [0, 0]

currentX = [0, 0]
currentY = [0, 0]
currentYawDeg = [0, 0]
currentYawRad = [0, 0]

pub = {}

###########################################################################


def pathAcquisition(data):
    global currentPath
    global size
    currentPath = path_points()

    currentPath.x = data.x
    currentPath.y = data.y
    currentPath.yaw = data.yaw
    currentPath.dOne = data.dOne
    currentPath.dTwo = data.dTwo
    size = len(currentPath.x)


def movingDittoCB(data):
    global currentX
    global currentY
    global currentYawRad, currentYawDeg

    currentX[0] = data.pose.pose.position.x
    currentY[0] = data.pose.pose.position.y
    rot = data.pose.pose.orientation
    (roll, pitch, currentYawRad[0]) = euler_from_quaternion(
        [rot.x, rot.y, rot.z, rot.w])

    currentYawDeg[0] = currentYawRad[0]*(180/pi)

    if currentYawDeg[0] < 0:
        currentYawDeg[0] += 360


def stableDittoCB(data):
    global currentX
    global currentY
    global currentYawRad, currentYawDeg

    currentX[1] = data.pose.pose.position.x
    currentY[1] = data.pose.pose.position.y
    rot = data.pose.pose.orientation
    (roll, pitch, currentYawRad[1]) = euler_from_quaternion(
        [rot.x, rot.y, rot.z, rot.w])

    currentYawDeg[1] = currentYawRad[1]*(180/pi)

    if currentYawDeg[1] < 0:
        currentYawDeg[1] += 360

###########################################################################


def forwardFn(goal_x, goal_y, Omega, dittoNum):
    global start2, currentX, currentY, currentYawRad, currentYawDeg, whichDitto
    start2 = True
    FrwDiff_x = 0
    FrwDiff_y = 0
    eucFrw = 0
    indexFrw = 69  # Error Num

    print("Forwarding")

    # Mafrood Neb3at dittoNum As a String

    for n in range(0, len(whichDitto)):
        print ' n = ', n
        print 'which ditto', whichDitto[n]
        if whichDitto[n] == int(dittoNum[0]):
            indexFrw = n
    print 'indexFrw', indexFrw
    print ' '
    print 'dittoNum', dittoNum[0]
    print 'which ditto 1 ', whichDitto[1]
    while start2:
        FrwDiff_x = goal_x - currentX[indexFrw]
        FrwDiff_y = goal_y - currentY[indexFrw]

        eucFrw = sqrt(pow(FrwDiff_x, 2)+pow(FrwDiff_y, 2))

        if eucFrw >= 0.01:
            # print'Dist. in X to goal.x= ', FrwDiff_x
            # print'Dist. in Y to goal.y= ', FrwDiff_y
            # print("Remaining Distance: "),
            # print(eucFrw)
            # print " "

            for i in str(dittoNum):
                pub["ditto" + i + "/left_wheel_speed"].publish(Omega)
                pub["ditto" + i + "/right_wheel_speed"].publish(Omega)
            # leftFrw.publish(Omega)
            # rightFrw.publish(Omega)

        else:
            print('Stopped Forwarding')
            print(" ")

            for i in str(dittoNum):
                pub["ditto" + i + "/left_wheel_speed"].publish(0)
                pub["ditto" + i + "/right_wheel_speed"].publish(0)
            # leftFrw.publish(0)
            # rightFrw.publish(0)
            start2 = False


def rotate(angle, Omega, dittoNum):
    global start, currentX, currentY, currentYawRad, currentYawDeg, whichDitto
    start = True
    indexRot = 69
    yaw_goal = 0

    print ('Rotating...')

    for n in range(0, len(whichDitto)):
        if whichDitto[n] == int(dittoNum[0]):
            indexRot = n

    save_path = os.path.dirname(__file__)
    name_of_file = "last_yaw_goal"
    completeName = os.path.join(save_path, name_of_file+".txt")
    file1 = open(completeName, "r")

    # Note that position == n-1 for the nth line.
    for position, line in enumerate(file1):
        # If line(position) desired is first line, then position == 0
        if position == int(dittoNum[0]):
            dittoTXT = line

    dittoTXT = float(dittoTXT)
    file1.close()

    yaw_goal = angle + dittoTXT
    if yaw_goal < 0:
        yaw_goal = yaw_goal + 359.99
    elif yaw_goal > 359.99:
        yaw_goal = yaw_goal - 359.99

    file1 = open(completeName, "r")
    list_of_lines = file1.readlines()
    print 'len(list of lines) = ', len(list_of_lines)
    for i in range(0, len(dittoNum)):
       # print 'i =', i
       #i = int(i)
        list_of_lines[int(dittoNum[i])] = (str(yaw_goal))+ "\n"

    file1 = open(completeName, "w")
    file1.writelines(list_of_lines)
    file1.close()

    while start:
        #print('yaw goal - current yaw = ', yaw_goal - currentYawDeg[indexRot])
        if abs(yaw_goal - currentYawDeg[indexRot]) > 0.05:

            if (angle > 0):
                #print 'Angle > 0  : Cuurent Yaw Deg = ', currentYawDeg[indexRot]
                for i in str(dittoNum):
                    pub["ditto" + i + "/left_wheel_speed"].publish(-Omega)
                    pub["ditto" + i + "/right_wheel_speed"].publish(Omega)
            elif angle < 0:
                #print 'Angle < 0  : Cuurent Yaw Deg = ', currentYawDeg[indexRot]
                for i in str(dittoNum):
                    pub["ditto" + i + "/left_wheel_speed"].publish(Omega)
                    pub["ditto" + i + "/right_wheel_speed"].publish(-Omega)
            elif angle == 0:
                Omega = 0.025
                if yaw_goal - currentYawDeg[indexRot] > 0:
                    #print 'Right : Angle = 0, Current Yaw = ', currentYawDeg[indexRot]
                    for i in str(dittoNum):
                        pub["ditto" + i + "/left_wheel_speed"].publish(-Omega)
                        pub["ditto" + i + "/right_wheel_speed"].publish(Omega)
                else:
                    #print 'Left : Angle = 0, Current Yaw = ', currentYawDeg[indexRot]
                    for i in str(dittoNum):
                        pub["ditto" + i + "/left_wheel_speed"].publish(Omega)
                        pub["ditto" + i + "/right_wheel_speed"].publish(-Omega)

        else:
            for i in str(dittoNum):
                    pub["ditto" + i + "/left_wheel_speed"].publish(0)
                    pub["ditto" + i + "/right_wheel_speed"].publish(0)
                    
            print 'Finished Rotating, Current Yaw Deg = ', currentYawDeg[indexRot]
            print 'Finished Rotating, Current Yaw Rad = ', currentYawRad[indexRot]
            start = False


###########################################################################


def main():
    global movingDitto, stableDitto, multiDitto

    print("Single Ditto Controller!")

    rospy.init_node('singleController', anonymous=True, disable_signals=True)

    rospy.Subscriber("AStarPath", path_points, pathAcquisition)
    rospy.wait_for_message("AStarPath", path_points, timeout=10)

    movingDitto = str(currentPath.dOne)
    stableDitto = str(currentPath.dTwo)
    # Raqam El movingDitto Byet7at Fe Awel 5ana
    whichDitto[0] = int(movingDitto)

    rospy.Subscriber("ditto" + movingDitto + "/odom", Odometry, movingDittoCB)

    # Raqam El stableDitto Byet7at Fe Tani 5ana
    print 'stable ditto', stableDitto
    whichDitto[1] = int(stableDitto[0])
    print 'type stable ditto 0 =', type(stableDitto[0])
    print 'type stable ditto 0 =', type(whichDitto[1])

    rospy.Subscriber(
        "ditto" + stableDitto[0] + "/odom", Odometry, stableDittoCB)

    stableDittoSize = len(stableDitto)

    if stableDittoSize > 1:
        multiDitto = True
    elif len(stableDitto) == 1:
        multiDitto = False

    rospy.wait_for_message("ditto" + movingDitto +
                           "/odom", Odometry, timeout=10)
    rospy.wait_for_message("ditto" + stableDitto[0] +
                           "/odom", Odometry, timeout=10)

    pub["ditto" + movingDitto + "/left_wheel_speed"] = rospy.Publisher(
        "ditto" + movingDitto + "/left_wheel_speed", Float32, queue_size=1000)
    pub["ditto" + movingDitto + "/right_wheel_speed"] = rospy.Publisher(
        "ditto" + movingDitto + "/right_wheel_speed", Float32, queue_size=1000)

    for i in str(stableDitto):
        pub["ditto"+i+"/left_wheel_speed"] = rospy.Publisher(
            "ditto" + i + "/left_wheel_speed", Float32, queue_size=1000)
        pub["ditto"+i+"/right_wheel_speed"] = rospy.Publisher(
            "ditto" + i + "/right_wheel_speed", Float32, queue_size=1000)

    #forwardFn(2,1, 0.4, str(movingDitto))
    rotate(45, 0.05 ,str(stableDitto))
    rospy.sleep(0.5)
    rotate(0, 0.1 ,str(stableDitto))
    rotate(0, 0.1 ,str(stableDitto))



if __name__ == '__main__':
    main()
