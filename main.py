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
    
    sense.clear()
    # Define some colours
    g = (0, 255, 0) # Green
    b = (0, 0, 0) # Black

    # Set up where each colour will display
    creeper_pixels = [
        g, b, b, b, b, b, b, b,
        b, g, b, b, b, b, b, b,
        b, b, g, b, b, b, g, b,
        b, b, b, g, b, b, g, b,
        b, b, b, b, g, b, g, b,
        b, b, b, b, b, g, g, b,
        b, b, g, g, g, g, g, b,
        b, b, b, b, b, b, b, b
    ]

    # Display these colours on the LED matrix
    sense.set_pixels(creeper_pixels)
    
    if check_for_exit(sense): #if the player holds the center button for 5 seconds, we exit the program
        sense.show_message("End.", text_colour=yellow, back_colour=blue, scroll_speed=0.1)
        return

    #step 1 : 
    initial_BP, initial_RT = step_1(sense)
    if initial_BP is None and initial_RT is None:  # means failure or check_for_exit is true 
        print("Exit or failed to do step 1")
        sense.show_message("End.", text_colour=yellow, back_colour=blue, scroll_speed=0.1)
        return
    
    sense.clear()
    print("Set timer")
    #transition : 
    sense.set_pixels(creeper_pixels)
    
    if check_for_exit(sense):  #checking again if player wants to exit
        sense.show_message("End.", text_colour=yellow, back_colour=blue, scroll_speed=0.1)
        return
        
    res = set_timer(sense, 4)
    if res == 1:
        sense.show_message("End.", text_colour=yellow, back_colour=blue, scroll_speed=0.1)
        return
    
    #step 2 : 
    # For now we suggest a fixed BP with 5 seconds inhale and 5 seconds exhale. 
    # Further improvements : suggest other breathing patterns based on further reseach 
    # (for e.g with 5 seconds hold between inhale and exhale)
    
    flag = 1
    
    while flag : #user has to follow a BP and play to RT game over and over until its 
        # RT has been well improved (compared to its initial RT)
        sense.set_pixels(creeper_pixels)
        if check_for_exit(sense):  #checking again if player wants to exit
            sense.show_message("End.", text_colour=yellow, back_colour=blue, scroll_speed=0.1)
            return
        
        print("Here")
        new_BP = BreathingPattern(0.8,0.8, 0.8) # for now we don't have any new suggestions, 
        # but we still make the user play again to step 2 
        new_RT = step_2(sense,new_BP)
        
        if new_RT is None :
            print("Exit or failed to do step 2")
            sense.show_message("End.", text_colour=yellow, back_colour=blue, scroll_speed=0.1)
            return
            
        
        #if check_for_exit(sense):  #checking again if player wants to exit
        #    sense.show_message("End.", text_colour=yellow, back_colour=blue, scroll_speed=0.1)
        #    return
        

        #some improvement found
        if measure_difference_RTs(initial_RT, new_RT) > 0.00001 :
            sense.show_message("End.", text_colour=yellow, back_colour=blue, scroll_speed=0.1) 
            flag = 0
        else : 
            sense.show_message("Try again.", text_colour=yellow, back_colour=blue, scroll_speed=0.1)
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

    print("Entering deduce_breathing_pattern\n")
    
    
    if check_for_exit(sense): #if the player holds the center button for 5 seconds, we exit the program
        return None
    
    start_time = time()
    inhaling_times = []
    exhaling_times = []
    sense.clear()
    g = (0, 255, 0) # Green
    b = (0, 0, 0) # Black
    r = (255,0,0) #red

    # Set up where each colour will display
    clear_pixels = [
        b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, b, b
    ]
    inhale_exhale_pixels = [
        b, b, b, g, b, b, b, b,
        b, b, g, g, g, b, b, b,
        b, g, b, g, b, g, b, b,
        b, b, b, g, b, b, b, b,
        b, g, b, g, b, g, b, b,
        b, b, g, g, g, b, b, b,
        b, b, b, g, b, b, b, b,
        b, b, b, b, b, b, b, b
    ]
    inhale_pixels = [
        b, b, b, b, b, b, b, b,
        b, b, b, g, b, b, b, b,
        b, b, g, g, g, b, b, b,
        b, g, b, g, b, g, b, b,
        b, b, b, g, b, b, b, b,
        b, b, b, g, b, b, b, b,
        b, b, b, g, b, b, b, b,
        b, b, b, g, b, b, b, b
    ]
    exhale_pixels = [
        b, b, b, g, b, b, b, b,
        b, b, b, g, b, b, b, b,
        b, b, b, g, b, b, b, b,
        b, b, b, g, b, b, b, b,
        b, g, b, g, b, g, b, b,
        b, b, g, g, g, b, b, b,
        b, b, b, g, b, b, b, b,
        b, b, b, b, b, b, b, b
    ]
    wrong_pixels = [
        r, b, b, b, b, b, b, r,
        b, r, b, b, b, b, r, b,
        b, b, r, b, b, r, b, b,
        b, b, b, r, r, b, b, b,
        b, b, b, r, r, b, b, b,
        b, b, r, b, b, r, b, b,
        b, r, b, b, b, b, r, b,
        r, b, b, b, b, b, b, r
    ]
    done_pixels = [
        b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, g, b,
        b, b, b, b, b, g, b, b,
        g, b, b, b, g, b, b, b,
        b, g, b, g, b, b, b, b,
        b, b, g, b, b, b, b, b,
        b, b, b, b, b, b, b, b
    ]

    # Display these colours on the LED matrix
    sense.set_pixels(inhale_exhale_pixels)
    #continuously waiting for button press (during specified duration)
    while time() - start_time < duration:
        event= sense.stick.wait_for_event()
        if event.action == "pressed":          #user input : 
            if event.direction == "up":  # User pressed up arrow, start inhaling
                print("Inhale")
                sense.set_pixels(inhale_pixels)
                inhaling_times.append(time() - start_time)
                for event in sense.stick.get_events():
                    print("ignoring joystick events",event)
            elif event.direction == "down":  # User pressed down arrow, start exhaling
                print("Exhale")
                sense.set_pixels(exhale_pixels)
                exhaling_times.append(time() - start_time)
                for event in sense.stick.get_events():
                    print("ignoring joystick events",event)
            else:
                sense.set_pixels(wrong_pixels)
                for event in sense.stick.get_events():
                    print("ignoring joystick events",event)
    for event in sense.stick.get_events():
        print("ignoring joystick events", event)
    sense.set_pixels(done_pixels)
    sleep(1)                        
    print ("Done.. calculating")
    for event in sense.stick.get_events():
        print("ignoring joystick events", event)
    #doing a mean of I and E times over the period, and then storing this information
    if inhaling_times and exhaling_times:
        mean_inhaling_time = sum(inhaling_times) / len(inhaling_times)
        mean_exhaling_time = sum(exhaling_times) / len(exhaling_times)
        print("mean inhale, mean exhale",mean_inhaling_time, mean_exhaling_time)
        return BreathingPattern(mean_inhaling_time, mean_exhaling_time, 0)
    else:
        print("Error: deduce_breathing_pattern\n")
        sense.show_message("BP : try again",text_colour= (255, 255, 0), back_colour=(0,0,255), scroll_speed=0.1)
        return None 
    


def measure_simple_reaction_time(sense, duration=15):
    """Reaction Time game for simple reaction time. 
    args : duration (int, optional): The duration in seconds for the experiment. Defaults to 20.
    returns : SimpleRT, the measured simple reaction time
    """
    
    print("Entering measure_simple_reaction_time\n")
    for event in sense.stick.get_events():
        print("ignoring joystick events", event)
    start_time = time()
    reaction_times = []
    g = (0, 255, 0) # Green
    b = (0, 0, 0) # Black

    # Set up where each colour will display
    creeper_pixels = [
        g, b, b, b, b, b, b, b,
        b, g, b, b, b, b, b, b,
        b, b, g, b, b, b, g, b,
        b, b, b, g, b, b, g, b,
        b, b, b, b, g, b, g, b,
        b, b, b, b, b, g, g, b,
        b, b, g, g, g, g, g, b,
        b, b, b, b, b, b, b, b
    ]
    done_pixels = [
        b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, g, b,
        b, b, b, b, b, g, b, b,
        g, b, b, b, g, b, b, b,
        b, g, b, g, b, b, b, b,
        b, b, g, b, b, b, b, b,
        b, b, b, b, b, b, b, b
    ]

    # Display these colours on the LED matrix
    sense.set_pixels(creeper_pixels)
    if check_for_exit(sense): #if the player holds the center button for 5 seconds, we exit the program
        return
    while time() - start_time < duration:
        sense.clear()
        
        #random delay between 1 and 2 seconds : 
        delay = randint(1, 2)  
        sleep(0.3)
        #randomly light up a LED : 
        x, y = randint(0, 7), randint(0, 7) #random coordinates for a LED
        sense.set_pixel(x, y, (254, 254, 254)) # sets pixel to white
        
        led_on_time = time()
        #sleep(delay)
        print("here waiting for press" , x, y)
        #we wait for the user to press the Enter key : 
        while True:
            event = sense.stick.wait_for_event()
            if event.action == "released":
                RT = time() - led_on_time
                reaction_times.append(RT)
                print("pressed")
                break
                #sense.clear() # lights off the pixel
            else:
                print(event)
                for event in sense.stick.get_events():
                    print("ignoring joystick events",event) 

    # we compute the mean of the reaction times over the period and store it : 
    if reaction_times:
        mean_RT = sum(reaction_times) / len(reaction_times)
        print("computed mean RT : ", mean_RT )
        sense.set_pixels(done_pixels)
        sleep(1)
        return SimpleRT(mean_RT)
    else:
        print("Error: measure_simple_RT")
        sense.show_message("RT: try again",text_colour= (255, 255, 0), back_colour=(0,0,255), scroll_speed=0.1)
        return None  
    
    
def step_1(sense): #returns the initial BP and RT 
    
    print("Entering step 1")
    
    # if check_for_exit(sense): #if the player holds the center button for 5 seconds, we exit the program
    #    return None, None
    
    # Tracking the player’s initial breathing & reaction time 
    BP = deduce_breathing_pattern(sense)
    if BP is None : 
        print("Exit or failed to measure initial breathing pattern")
        return None, None
    
    # for now we are just using a simple RT 
    # further improvements : do experiments for recognition RT and choice RT 
    RT = measure_simple_reaction_time(sense)
    if RT is None : 
        print("Exit or failed to measure initial reaction time")
        return None, None
        
    print("Step 1 done")
    return BP, RT 
        
        
# ________________________________________________________________________________________
#   TRANSITION : 

        
def set_timer(sense, seconds=60): 
    """Sets a timer for a specified number of seconds.
    args : seconds (int, optional), default to 60"""
    print("Transition of 1 min")
    
    if check_for_exit(sense):  #checking again if player wants to exit
        return 1
    
    sense.show_message("Relax",text_colour= (255, 255, 0), back_colour=(0,0,255), scroll_speed=0.1)
    sleep(seconds)
    sense.clear()
    return 0
    
    
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
    
    print("Entering suggested_BP")
    
    start_time = time()

   
   # divide the whole inhaling or exhaling time by 8 (nb rows) to light up at a regular pace
    ti = t_inh/8
    te = t_exh/8
    sense.clear()
    
    while time() - start_time < duration:
        
        # INHALE : light up the rows from bottom to top
        print("inhale")
        for row in range(7, -1, -1): #reverse iteration
            for x in range(8):
                sense.set_pixel(x, row, (255, 255, 255))
                sleep(ti) 
           
        print("hold for ", t_hold)     
        #HOLD : 
        sleep(t_hold)

        # EXHALE : turn off the rows from top to bottom
        print("exhale")
        for row in range(8):
            for x in range(8):
                sense.set_pixel(x, row, (0, 0, 0))
                sleep(te)
    print("Done from breating")
    return 0



def step_2(sense, BP):  
    """ returns the new RT measured after the suggested BP
    args : BP of class BreathingPattern"""
    # User has to follow a suggested breathing pattern, plays again to RT game, 
    # and we measure its new performance
    
    print("Entering step 2") 
    
    inh = BP.get_t_inh()
    exh = BP.get_t_exh()
    hold = BP.get_t_hold()
    
    res = suggested_BP(sense, duration = 20, t_inh=inh, t_exh=exh, t_hold=hold) 
    if res == 1:
        print("Exit")
        return None 
    g = (0, 255, 0) # Green
    b = (0, 0, 0) # Black

    # Set up where each colour will display
    creeper_pixels = [
        g, b, b, b, b, b, b, b,
        b, g, b, b, b, b, b, b,
        b, b, g, b, b, b, g, b,
        b, b, b, g, b, b, g, b,
        b, b, b, b, g, b, g, b,
        b, b, b, b, b, g, g, b,
        b, b, g, g, g, g, g, b,
        b, b, b, b, b, b, b, b
    ]
    sense.clear()
    # Display these colours on the LED matrix
    sense.set_pixels(creeper_pixels)
    sleep(0.1)
    

    if check_for_exit(sense): #if the player holds the center button for 5 seconds, we exit the program
        return
   
    
    new_RT = measure_simple_reaction_time(sense)
    if new_RT is None : 
        print("Failed to measure new reaction time")
        
    return new_RT

    
    
#________________________________________________________________________________________________________
# Measuring performance : 

def measure_difference_RTs(initial_RT, new_RT): 
    print("Entering measure_difference_RTs")
    i_RT = initial_RT.value
    n_RT = new_RT.value
    res = i_RT - n_RT
    print("difference of RTs : ", i_RT, " - ", n_RT," = ", res)
    return res  #not using abs() because we want to make sure that the new is less than the initial  




#___________________________________________________________________________________________________________
# Exiting the program : 

def check_for_exit(sense, hold_time=5):
    """Checks if the user holds the stick to the RIGHT for `hold_time` seconds to exit."""
    
    
    start_hold_time = None  
    event = sense.stick.wait_for_event()
    
    if event.action == "pressed" and event.direction == "right":   #we start counting when the right button is pressed    
        start_hold_time = time()
        
    elif event.action == "released" and event.direction == "right" and start_hold_time: #if the button is released before hold_time seconds, reset the timer
        start_hold_time = None
        
    elif event.action == "held" and event.direction == "right" and start_hold_time: #if the button has been held for `hold_time` seconds
        if time() - start_hold_time >= hold_time:
            
            print("Exiting game")
            sense.show_message("Exit game", text_colour= (255, 255, 0), back_colour=(0,0,255), scroll_speed=0.1)
            return True
    
    for event in sense.stick.get_events():
        print("ignoring joystick events")
    return False 



if __name__ == "__main__":
    main()