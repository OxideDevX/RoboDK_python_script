#Данный скрпит позволяет безопасно восстановить соединение с роботом.
from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox
from time import sleep
RDK = Robolink()

#коннектимся к роботу
robot = RDK.Item('Select a robot', ITEM_TYPE_ROBOT)
robot.Connect()

while 1:
    robot.Connect()
    sleep(10)
