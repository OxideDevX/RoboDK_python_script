from robolink import *    # RoboDK API импорт
from robodk import *      # Robot toolbox импорт
from time import sleep
import socket
RDK = Robolink()

#задаем параметры для подключения
HOST = "169.254.42.105" #robot ip
PORT = 30002 #port to connect to

# создаем инструмент
robot = RDK.Item('Select a robot', ITEM_TYPE_ROBOT)
tool = RDK.Item('Gripper')

RDK.setSimulationSpeed(1) #запускаем в риал тайме симуляцию

Opening the gripper before moving the robot
robot.Disconnect() 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((HOST, PORT)) 
Setting commands to send to the robot
a = "set_tool_digital_out(0, False)"
b = "\n"
s.send(a.encode() + b.encode()) #отправляем команду на энкодер
s.close() 
robot.ConnectSafe(HOST, 100, 0.5) #переподключнение через тайм аут

robot.setSpeed(1500, 1300, 2500, 280) #задача скорости

conveyor = RDK.Item('Conveyor')
balancing_machine = RDK.Item('Balancing machine')
leaking_test_machine = RDK.Item('Leaking test machine')
engraving_machine = RDK.Item('Engraving machine')

drawer_closed = RDK.Item('Drawer closed')
drawer_open = RDK.Item('Drawer open')
drawer_open_app = RDK.Item('Drawer open app')
drawer_drop_app = RDK.Item('Drawer drop app')
drawer_drop = RDK.Item('Drawer drop')
drawer_pick = RDK.Item('Drawer pick')
drawer_pick_app = RDK.Item('Drawer pick app')
app_app = RDK.Item('App-app')
drawer = RDK.Item('Drawer')

leak_drop = [RDK.Item('Leaking drop 1'), RDK.Item('Leaking drop 2')]
leak_drop_app = [RDK.Item('Leaking drop 1 app'), RDK.Item('Leaking drop 2 app')]
leak_app = RDK.Item('Leak app')
lt_param = ['lt1', 'lt2']
trash = RDK.Item('Trash')
trash_obj = RDK.Item('Trash obj')

engraving_drop = RDK.Item('Engraving drop')
engraving_drop_app1 = RDK.Item('Engraving drop app 1')
engraving_drop_app2 = RDK.Item('Engraving drop app 2')

conveyor_drop_app = RDK.Item('Conveyor drop app')
conveyor_drop = RDK.Item('Conveyor drop')

queue_table = [RDK.Item('Queue 1 table'), RDK.Item('Queue 2 table'), RDK.Item('Queue 3 table')]
queue = [RDK.Item('Queue 1'), RDK.Item('Queue 2'), RDK.Item('Output trolley')]
queue_drop = [RDK.Item('Queue 1 drop app'), RDK.Item('Queue 2 drop app'), RDK.Item('Queue 3 drop app')]

def close_gripper():
    #robot.Disconnect()
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((HOST, PORT))
    #a = "set_tool_digital_out(0, True)"
    #b = "\n"
    #s.send(a.encode() + b.encode())
    #s.close()
    #robot.ConnectSafe(HOST, 100, 0.1)
    
    tool.AttachClosest()
    robot.setSpeed(1500, 1500, 2000, 180) #скорость при разрыве коннекта

def open_gripper(parent):
    #robot.Disconnect()
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.connect((HOST, PORT))
    #a = "set_tool_digital_out(0, False)"
    #b = "\n"
    #s.send(a.encode() + b.encode())
    #s.close()
    #robot.ConnectSafe(HOST, 100, 0.1)
    
    tool.DetachAll(parent)
    robot.setSpeed(1500, 1500, 2000, 180) 

# MoveJ or MoveL command
def queue_target(table, dropping, number):
    target = Mat(queue_drop[table].Pose())
    target_pos = target.Pos()

    robot.setPoseFrame(queue[table])

    row = number % 4
    col = number // 4
    
    target_pos[0] = target_pos[0] + (0 - col) * 90
    target_pos[1] = target_pos[1] + (0 - row) * 90
    target_pos[2] = target_pos[2] - dropping * 200

    target.setPos(target_pos)

    return target

def conveyor_to_drawer():
    robot.setPoseFrame(conveyor)
    robot.MoveL(conveyor_drop)
    close_gripper()
    RDK.setParam('conv', 0)
    robot.MoveL(conveyor_drop_app)
    robot.setPoseFrame(balancing_machine)
    robot.MoveJ(drawer_drop_app)
    robot.MoveL(drawer_drop)
    open_gripper(drawer)
    robot.MoveL(drawer_drop_app)
    robot.MoveL(app_app)
    robot.MoveJ(drawer_open_app)

def balance_drawer_open():
    robot.setPoseFrame(balancing_machine)
    robot.MoveJ(drawer_open)
    robot.MoveL(drawer_closed)
    close_gripper()
    robot.MoveL(drawer_open)
    open_gripper(balancing_machine)
    robot.MoveL(drawer_open_app)

def balance_drawer_close():
    robot.setPoseFrame(balancing_machine)
    robot.MoveL(drawer_open_app)
    robot.MoveL(drawer_open)
    close_gripper()
    robot.MoveL(drawer_closed)
    open_gripper(balancing_machine)
    robot.MoveL(drawer_open)

def drawer_pick_rotor():
    balance_drawer_open()
    robot.setPoseFrame(balancing_machine)
    robot.MoveL(app_app)
    robot.MoveJ(drawer_pick_app)
    robot.MoveL(drawer_pick)
    close_gripper()
    robot.MoveL(drawer_pick_app)
    RDK.setParam('bal_filled', 0)
    q1 = RDK.getParam('q1')
    robot.MoveL(queue_target(0, 0, q1))
    robot.MoveL(queue_target(0, 1, q1))
    open_gripper(queue_table[0])
    robot.MoveL(queue_target(0, 0, q1))
    q1 += 1
    RDK.setParam('q1', q1)
    
def balance_add_rotor():
    balance_drawer_open()
    robot.MoveL(conveyor_drop_app)
    conveyor_to_drawer()
    balance_drawer_close()
    RDK.setParam('bal_filled', 1)

def replace_balance_rotor():
    drawer_pick_rotor()
    robot.MoveJ(conveyor_drop_app)
    conveyor_to_drawer()
    balance_drawer_close()
    RDK.setParam('bal_filled', 1)

def leak_to_queue2(rot_number):
    robot.setPoseFrame(leaking_test_machine)
    robot.MoveJ(leak_app)
    robot.MoveJ(leak_drop_app[rot_number])
    robot.MoveL(leak_drop[rot_number])
    close_gripper()
    robot.MoveL(leak_drop_app[rot_number])
    robot.MoveJ(leak_app)
    RDK.setParam(lt_param[rot_number], 0)
    q2 = RDK.getParam('q2')
    robot.MoveL(queue_target(1, 0, q2))
    robot.MoveL(queue_target(1, 1, q2))
    open_gripper(queue_table[1])
    robot.MoveL(queue_target(1, 0, q2))
    q2 += 1
    RDK.setParam('q2', q2)

def leak_to_engraving(rot_number):
    robot.setPoseFrame(leaking_test_machine)
    robot.MoveJ(leak_app)
    robot.MoveJ(leak_drop_app[rot_number])
    robot.MoveL(leak_drop[rot_number])
    close_gripper()
    robot.MoveL(leak_drop_app[rot_number])
    robot.MoveJ(leak_app)
    RDK.setParam(lt_param[rot_number], 0)
    robot.setPoseFrame(engraving_machine)
    robot.MoveJ(engraving_drop_app2)
    robot.MoveL(engraving_drop_app1)
    robot.MoveL(engraving_drop)
    open_gripper(engraving_machine)
    robot.MoveL(engraving_drop_app2)
    RDK.setParam('eng_filled', 1)

def leak_to_trash(rot_number):
    robot.setPoseFrame(leaking_test_machine)
    robot.MoveJ(leak_app)
    robot.MoveJ(leak_drop_app[rot_number])
    #robot.setRounding(0)
    robot.MoveL(leak_drop[rot_number])
    close_gripper()
    #robot.setRounding(50)
    robot.MoveL(leak_drop_app[rot_number])
    robot.MoveJ(leak_app)
    RDK.setParam(lt_param[rot_number], 0)
    robot.MoveJ(trash)
    open_gripper(trash_obj)
    defect_rotor = trash_obj.Childs()
    defect_rotor[0].Delete()

def engraving_to_output():
    robot.setPoseFrame(engraving_machine)
    robot.MoveJ(engraving_drop_app2)
    robot.MoveL(engraving_drop)
    close_gripper()
    robot.MoveL(engraving_drop_app1)
    robot.MoveL(engraving_drop_app2)
    RDK.setParam('eng_filled', 0)
    q3 = RDK.getParam('q3')
    robot.MoveJ(queue_target(2, 0, q3))
    robot.MoveL(queue_target(2, 1, q3))
    open_gripper(queue_table[2])
    robot.MoveL(queue_target(2, 0, q3))
    q3 += 1
    RDK.setParam('q3', q3)
    robot.setPoseFrame(engraving_machine)
    robot.MoveJ(engraving_drop_app2)

def queue2_to_engraving():
    q2 = RDK.getParam('q2')
    q2 -= 1
    robot.MoveJ(queue_target(1, 0, q2))
    robot.MoveL(queue_target(1, 1, q2 ))
    close_gripper()
    robot.MoveL(queue_target(1, 0, q2))
    RDK.setParam('q2', q2)
    robot.setPoseFrame(engraving_machine)
    robot.MoveJ(engraving_drop_app2)
    robot.MoveL(engraving_drop_app1)
    robot.MoveL(engraving_drop)
    open_gripper(engraving_machine)
    robot.MoveL(engraving_drop_app2)
    RDK.setParam('eng_filled', 1)

side = 1

while 1:
    bal_filled = RDK.getParam('bal_filled')
    conv = RDK.getParam('conv')
    q1 = RDK.getParam('q1')
    bal_time = RDK.getParam('bal_time')

    new_round = False 
    lt = [RDK.getParam('lt1'), RDK.getParam('lt2')]
    eng_filled = RDK.getParam('eng_filled')
    eng_time = RDK.getParam('eng_time')
    q2 = RDK.getParam('q2')
    q3 = RDK.getParam('q3')    
    
    if conv == 1 and bal_filled == 0:
        if side == 2:
            robot.setPoseFrame(leaking_test_machine)
            robot.MoveJ(leak_app)

        side = 1
        balance_add_rotor()
        RDK.setParam('bal_time', 8) 
        continue 

    if conv == 1 and bal_filled == 1 and bal_time == 0 and q1 < 16:
        if side == 2:
            robot.setPoseFrame(leaking_test_machine)
            robot.MoveJ(leak_app)

        side = 1
        replace_balance_rotor()
        RDK.setParam('bal_filled', 1)
        RDK.setParam('bal_time', 8)
        continue

    for i in range(2):
        if lt[i] != 1: 
        continue
        
        if eng_filled == 0:
            if side == 1:
                robot.setPoseFrame(leaking_test_machine)
                robot.MoveJ(leak_app)

            side = 2
            leak_to_engraving(i)
            RDK.setParam('eng_time', 8)
            new_round = True 
            break 

        if eng_filled == 1 and eng_time == 0 and q3 < 16:
            if side == 1:
                robot.setPoseFrame(leaking_test_machine)
                robot.MoveJ(leak_app)

            side = 2
            engraving_to_output()
            leak_to_engraving(i)
            RDK.setParam('eng_time', 8)
            new_round = True
            break

    if new_round:
        continue
        
    if q2 != 0 and eng_filled == 0:
        if side == 1:
            robot.setPoseFrame(leaking_test_machine)
            robot.MoveJ(leak_app)

        side = 2
        queue2_to_engraving()
        RDK.setParam('eng_time', 8)
        continue

    if q2 != 0 and eng_filled == 1 and eng_time == 0 and q3 < 16:
        if side == 1:
            robot.setPoseFrame(leaking_test_machine)
            robot.MoveJ(leak_app)

        side = 2
        engraving_to_output()
        robot.setPoseFrame(engraving_machine)
        robot.MoveL(engraving_drop_app2)

        lt = [RDK.getParam('lt1'), RDK.getParam('lt2')]

        skip = False
        
        for i in range(2): 
            if lt[i] == 1:
                leak_to_engraving(i)
                RDK.setParam('eng_time', 8)
                skip == True
                break

        if skip:
            continue
        
        queue2_to_engraving()
        RDK.setParam('eng_time', 8)
        continue

    for i in range(2):

        if lt[i] == 1 and q2 < 16:
            if side == 1:
                robot.setPoseFrame(leaking_test_machine)
                robot.MoveJ(leak_app)

            side = 2
            leak_to_queue2(i)
            lt[i] = 0
            new_round = True
            break


        if lt[i] == 2:
            if side == 1:
                robot.setPoseFrame(leaking_test_machine)
                robot.MoveJ(leak_app)

            side = 2
            leak_to_trash(i)
            lt[i] = 0
            new_round = True
            break
            
    if new_round:
        continue
   
    if bal_filled == 1 and q1 < 16 and bal_time == 0:
        if side == 2:
            robot.setPoseFrame(leaking_test_machine)
            robot.MoveJ(leak_app)

        side = 1
        drawer_pick_rotor()

        conv = RDK.getParam('conv')

        if conv == 1:
            balance_add_rotor()
            RDK.setParam('bal_time', 8)
        
        balance_drawer_close()
        continue

    if eng_filled == 1 and eng_time == 0 and q3 < 16:
        if side == 1:
            robot.setPoseFrame(leaking_test_machine)
            robot.MoveJ(leak_app)

        side = 2
        engraving_to_output()
        continue


    
    
