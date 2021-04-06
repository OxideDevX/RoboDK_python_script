#This script will reset all the parameters in the workspace, as well as remove all current rotors

from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox

RDK = Robolink()

#Resets robot
robot = RDK.Item('Select a robot', ITEM_TYPE_ROBOT)
robot.setJoints([0, -90, -90, 0, 90, 0])

balancing_machine = RDK.Item('Balancing machine')

#Deletes rotors
rotor = RDK.Item('rotor')
while rotor.Valid():
    rotor.Delete()
    rotor = RDK.Item('rotor')

#Resets parameters
RDK.setParam('q1', 0)
RDK.setParam('q2', 0)
RDK.setParam('q3', 0)
RDK.setParam('bal_time', 0)
RDK.setParam('bal_filled', 0)
RDK.setParam('lt_time', 0)
RDK.setParam('lt1', 0)
RDK.setParam('lt2', 0)
RDK.setParam('eng_time', 0)
RDK.setParam('eng_filled', 0)
RDK.setParam('conv', 0)

#Resets drawer
drawer = RDK.Item('Drawer')
drawer_pos_array = [0, 110, 0, 0, 0, 0]
drawer_pose = TxyzRxyz_2_Pose(drawer_pos_array)
drawer.setParent(balancing_machine)
drawer.setPose(drawer_pose)

#Sets the robot reference frame
base = RDK.Item('UR5 Base')
robot.setPoseFrame(base)
