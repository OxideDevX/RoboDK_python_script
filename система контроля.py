from robolink import *    
from robodk import *      
from time import sleep
RDK = Robolink()

sleep_time = 0 

leaking_test_machine = RDK.Item('Leaking test machine')

rotor_pos_array1 = [346, 541, 245.5, 3.141593, 0, 0]
rotor_pos_array2 = [196, 541, 245.5, 3.141593, 0, 0]

def get_input():
    rotor_states = mbox('Enter rotor states: 0 not existing, 1 for success, 2 for defect', entry = True)
    rotor_state_number = int(rotor_states)
    return rotor_state_number

while 1:

    done = False
    waiting = True

    while waiting: 
        rotor1_param = RDK.getParam('lt1')
        rotor2_param = RDK.getParam('lt2')

        if rotor1_param == 0 and rotor2_param == 0: 
            waiting = False 
        sleep(0.5)
    
    while not done: 
        rotor_state_number = get_input() 
        rot = [rotor_state_number // 10, rotor_state_number % 10] 

        if rot[0] < 3 and rot[0] >= 0 and rot[1] < 3 and rot[1] >= 0: 
            done = True

    current_sleep_timer = sleep_time

    RDK.setParam('lt_time', sleep_time) 
    while current_sleep_timer > 0: 
        sleep(1)
        current_sleep_timer -= 1
        RDK.setParam('lt_time', current_sleep_timer)
    
    for i in range(2): 
    if i == 0:
            RDK.setParam('lt1', rot[i])
        else:
            RDK.setParam('lt2', rot[i])

        #r'C:\Users\galas\Desktop\rob2\P2\rotor1forben.STL'

        if rot[i] > 0: 
            rotor = RDK.AddFile('/home/benjamin/Documents/RoboDK/station_objects/rotor.stl', leaking_test_machine) #Rotor is added from path and has parent leak_testing_machine
            rotor.setVisible(True, False) 
            rotor_pose = 0
            if i == 0: 
                rotor_pose = TxyzRxyz_2_Pose(rotor_pos_array1)
            else:
                rotor_pose = TxyzRxyz_2_Pose(rotor_pos_array2)
            rotor.setPose(rotor_pose) 

    


    
