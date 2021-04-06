from robolink import *    
from robodk import *      
from time import sleep
RDK = Robolink()

while 1:
 
    bal_filled = RDK.getParam('bal_filled')
    
    if bal_filled == 1:
        bal_time = 8

    
        while bal_time > 0:
            sleep(2)
            bal_time -= 1
            RDK.setParam('bal_time', bal_time)
            
        while bal_filled == 1:
            sleep(0.5)
            bal_filled = RDK.getParam('bal_filled')

    sleep(0.2) 
# по умолчанию 0.2 секунды(не менять!)
