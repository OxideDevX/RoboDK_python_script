#Данный скрпит позволяет автоматизировать процесс работы конвейерной ленты
from robolink import *   
from robodk import *      
from time import sleep
RDK = Robolink()

conveyor = RDK.Item('Conveyor')

manual_use = mbox('Do you wish for manual or automatic supply of rotors? 0 for manual', entry = True)
manual_use_number = int(manual_use)

r \dev\sda1\home\galas\Desktop\rob2\P2\rotor1forben.STL'

def add_rotor():

    rotor = RDK.AddFile('r \dev\sda1\home\galas\Desktop\rob2\P2\rotor1forben.STL'', conveyor) 
    rotor.setVisible(True, False) 
    rotor_pos_array = [80.889, 9.55, 65, 0.10, 1.658, 10] 
    rotor_pose = TxyzRxyz_2_Pose(rotor_pos_array) 
    rotor.setPose(rotor_pose)
    RDK.setParam('conv', 2)

if manual_use_number == 0:
    while 1:
        state = RDK.getParam('conv') 
        if state == 0: 
            sleep(1) 
            mbox('Запустить движение ленты') #запрос
            add_rotor() #добавление устройства
        else:
            sleep(1)
else:
    while 1: 
        state = RDK.getParam('conv')
        if state == 0: 
            sleep(1)
            add_rotor()
        else:
            sleep(0.5)
