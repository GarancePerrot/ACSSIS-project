from sense_hat import SenseHat
from time import time, sleep
from random import randint
from classes import *

        
        


# ___________________________________________________________________________________________

def main():
    """Does the experiment"""
    sense = SenseHat()
      
    # RGB colors and their complements
    red = (255,0,0)
    cyan = (0,255,255)
    green = (0, 255,0)
    magenta = (255,0,255)
    blue = (0, 0,255)
    yellow = (255, 255, 0)
    
    program_running = True

    while program_running : 
        
        if check_for_exit(sense): #if the player holds the center button for 5 seconds, we exit the program
            program_running = False 
            break
    
        #step 1 : 
        initial_BP, initial_RT = step_1(sense)
        
        #transition : 
        set_timer()
        
        #step 2 : 
        # For now we suggest a fixed BP with 5 seconds inhale and 5 seconds exhale. 
        # Further improvements : suggest other breathing patterns based on further reseach 
        # (for e.g with 5 seconds hold between inhale and exhale)
        
        flag = 1
        
        while flag : #user has to follow a BP and play to RT game over and over until its 
            # RT has been well improved (compared to its initial RT)
            
            if check_for_exit(sense):  #checking again if player wants to exit
                program_running = False
                break
            
            #new_BP = BreathingPattern(5,5, 0) # for now we don't have any new suggestions, 
            # but we still make the user play again to step 2 
            #new_RT = step_2(new_BP)
            
            dif = measure_difference_RTs(initial_RT, new_RT)
            
            if dif < 0.001 :
                sense.show_message("New reaction time has been well improved, game stops now.", text_colour=yellow, back_colour=blue, scroll_speed=0.1) 
                flag = 0
            else : 
                sense.show_message("New reaction time is too long, try again with a new breathing pattern suggestion.", text_colour=yellow, back_colour=blue, scroll_speed=0.1)
        #end while
    #end while
    
    sense.clear()    
    return

   

    
    # game stops 


#_____________________________________________________________________________________________________________________
#  STEP 1 : 



def deduce_breathing_pattern(sense, duration=10):
    # User presses up arrow just before inhaling, inhales, then presses down arrow, then exhales, and so on
    # for a specific duration of time 
    """Deduces the breathing pattern from user button presses.
    args: duration (int, optional): The duration in seconds to measure the breathing pattern. Defaults to 10.
    returns the measured breathing pattern """

    start_time = time()
    inhaling_times = []
    exhaling_times = []
    print("Deducing BP")
    sense.clear()
    #continuously waiting for button press (during specified duration)
    while time() - start_time < duration:
        print(time() - start_time)
        print(time() - start_time - duration)
        event= sense.stick.wait_for_event()
        if event.action == "pressed":          #user input : 
            if event.direction == "up":  # User pressed up arrow, start inhaling
                print("Inhale")
                inhaling_times.append(time() - start_time)
            elif event.direction == "down":  # User pressed down arrow, start exhaling
                print("exhale")
                exhaling_times.append(time() - start_time)
    print ("Done.. calculating")
    #doing a mean of I and E times over the period, and then storing this information
    if inhaling_times and exhaling_times:
        mean_inhaling_time = sum(inhaling_times) / len(inhaling_times)
        mean_exhaling_time = sum(exhaling_times) / len(exhaling_times)
        print("mean inhale, mean exhale",mean_inhaling_time, mean_exhaling_time)
        return BreathingPattern(mean_inhaling_time, mean_exhaling_time, 0)
    else:
        print("Error")
        sense.show_message("Breathing pattern measurement failed, try again.",text_colour= (255, 255, 0), back_colour=(0,0,255), scroll_speed=0.1)
        return None 
    


def measure_simple_reaction_time(sense, duration=20):
    """Reaction Time game for simple reaction time. 
    args : duration (int, optional): The duration in seconds for the experiment. Defaults to 20.
    returns : SimpleRT, the measured simple reaction time
    """

    start_time = time()
    reaction_times = []

    while time() - start_time < duration:
        
        #random delay between 1 and 3 seconds : 
        delay = randint(1, 3)  
        sleep(delay)
        #randomly light up a LED : 
        x, y = randint(0, 7), randint(0, 7) #random coordinates for a LED
        sense.set_pixel(x, y, (255, 255, 255)) # sets pixel to white
        led_on_time = time()

        #we wait for the user to press the Enter key : 
        event = sense.stick.wait_for_event()
        if event.action == "pressed":
            RT = time() - led_on_time
            reaction_times.append(RT)
            sense.clear() # lights off the pixel

    # we compute the mean of the reaction times over the period and store it : 
    if reaction_times:
        mean_RT = sum(reaction_times) / len(reaction_times)
        return SimpleRT(mean_RT)
    else:
        sense.show_message("Reaction Time measurement failed, try again.",text_colour= (255, 255, 0), back_colour=(0,0,255), scroll_speed=0.1)
        return None  
    
    
def step_1(sense): #returns the initial BP and RT 
    
    # Tracking the player’s initial breathing & reaction time 
    BP = deduce_breathing_pattern(sense)
    if BP is None : 
        sense.show_message("Failed to measure initial breathing pattern", text_colour= (255, 255, 0), back_colour=(0,0,255), scroll_speed=0.1)
    
    
    # for now we are just using a simple RT 
    # further improvements : do experiments for recognition RT and choice RT 
    RT = measure_simple_reaction_time(sense)
    if RT is None : 
        sense.show_message("Failed to measure initial reaction time", text_colour= (255, 255, 0), back_colour=(0,0,255), scroll_speed=0.1)
        
    return BP, RT 
        
        
# ________________________________________________________________________________________
#   TRANSITION : 

        
def set_timer(seconds=60): 
    """Sets a timer for a specified number of seconds.
    args : seconds (int, optional), default to 60"""
    time.sleep(seconds)
    
    
#__________________________________________________________________________________________
# STEP 2 : 


def suggested_BP(sense, duration=20, t_inh=5, t_exh=5, t_hold=0): #void called in step 2
    """Suggests a breathing pattern where the rows of LED matrix light up 
    and down according to the inhaling time t_inh and exhaling time t_exh. 
    args: duration (int): The duration in seconds, default 20 sec
        t_inh (float) : time for each row to light up, seconds
        t_exh (float): time for each row to turn off, seconds
    """
    # For now, we do not take any input to see if the user follows the suggestion, 
    # we trust him to follow the suggested BP
    # Further improvement : take input from user to make sure he follows the BP
    # (e.g up and down arrows as before, where he has to press up when starting to exhale,
    # down when starting to exhale, and we measure the difference between when all the rows 
    # are enlightened and when he presses the up arrow)
    
    start_time = time()

   
   # divide the whole inhaling or exhaling time by 8 (nb rows) to light up at a regular pace
    ti = t_inh/8
    te = t_exh/8
    
    
    while time() - start_time < duration:
        # INHALE : light up the rows from bottom to top
        for row in range(7, -1, -1): #reverse iteration
            for x in range(8):
                sense.set_pixel(x, row, (255, 255, 255))
                sleep(ti) 
                
        #HOLD : 
        sleep(t_hold)

        # EXHALE : turn off the rows from top to bottom
        for row in range(8):
            for x in range(8):
                sense.set_pixel(x, row, (0, 0, 0))
                sleep(te)



def step_2(sense, BP):  
    """ returns the new RT measured after the suggested BP
    args : BP of class BreathingPattern"""
    # User has to follow a suggested breathing pattern, plays again to RT game, 
    # and we measure its new performance 
    
    inh = BP.get_t_inh()
    exh = BP.get_t_exh()
    hold = BP.get_t_hold()
    
    suggested_BP(sense, duration = 20, t_inh=inh, t_exh=exh, t_hold=hold) 
    
    new_RT = measure_simple_reaction_time(sense)
    if new_RT is None : 
        sense.show_message("Failed to measure new reaction time", text_colour= (255, 255, 0), back_colour=(0,0,255), scroll_speed=0.1)
        
    return new_RT

    
    
#________________________________________________________________________________________________________
# Measuring performance : 

def measure_difference_RTs(initial_RT, new_RT): 
    
    i_RT = initial_RT.value
    n_RT = new_RT.value
    
    return i_RT - n_RT  #not using abs() because we want to make sure that the new is less than the initial  




#___________________________________________________________________________________________________________
# Exiting the program : 

def check_for_exit(sense, hold_time=5):
    """Checks if the user holds the center button for `hold_time` seconds to exit."""
    start_hold_time = None  
    for event in sense.stick.get_events():
        if event.action == "pressed" and event.direction == "middle":   #we start counting when the middle button is pressed    
            start_hold_time = time()
            
        elif event.action == "released" and event.direction == "middle" and start_hold_time: #if the button is released before hold_time seconds, reset the timer
            start_hold_time = None
            
        elif event.action == "held" and event.direction == "middle" and start_hold_time: #if the button has been held for `hold_time` seconds
            if time() - start_hold_time >= hold_time:
                sense.show_message("Exiting the game", text_colour= (255, 255, 0), back_colour=(0,0,255), scroll_speed=0.1)
                return True
    return False           


if __name__ == "__main__":
    main()