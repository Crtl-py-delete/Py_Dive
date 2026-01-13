# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 17:09:16 2024

@author: mvdhe

PRESS ESCAPE TO STOP A GAME
Vergeet ook niet de pynput te installeren met pip
"""

"Imports"
from random import randint
from time import sleep
from pynput import keyboard
import numpy as np
import sounddevice as sd

"Globals"
global size, player_pos

"Functions"
def play_note(note, octave=4, duration=0.5):
    """Mimic musicalbeeps: play_note("C", 0.3)"""
    base_notes = {
        "C": 261.63,
        "D": 293.66,
        "E": 329.63,
        "F": 349.23,
        "G": 392.00,
        "A": 440.00,
        "B": 493.88}

    note = note.upper()
    if note not in base_notes:
        raise ValueError("Use notes A–G")

    # octave scaling (A4 = 440 Hz reference)
    freq = base_notes[note] * (2 ** (octave - 4))

    #create sinewave with numpy
    fs = 44100
    t = np.linspace(0, duration, int(fs * duration), False)
    tone = np.sin(2 * np.pi * freq * t)
    
    #play the note
    sd.play(tone, fs, blocking=True)

def empty_plot():
    """clear the screen"""
    global screen_matrix
    screen_matrix = [["."] * size for x in range(size)] 
    """screen_matrix = [["."] * size] *size
    geeft een fout: de lists hebben, dan de zelfde id's en dan wijzigen ze allen tegeljk"""
      
    #clear and up
    print("\033[H \033[2J")
    print("\x1b[1;34m") 
    
def led_toggle(target_x, target_y, player_pos):
    
    if target_y > 0:
        screen_matrix[target_y-1][target_x] = "I"
    if target_y != size-1:
        screen_matrix[target_y+1][target_x] = "I"
    if target_x > 0:
        screen_matrix[target_y][target_x -1] = "I"
    if target_x != size-1:
        screen_matrix[target_y][target_x+1] = "I" 

    if target_x == player_pos[0] and target_y == player_pos[1]:
        screen_matrix[target_y][target_x] = "\2"       
    else: screen_matrix[player_pos[1]][player_pos[0]] = "ç"


# Function to handle key press events
def on_press(key):
        global game_is_running
        
        # Update player position based on arrow keys
        if key == keyboard.Key.up and player_pos[1] > 0:
            player_pos[1] -= 1
            
        elif key == keyboard.Key.down and player_pos[1] < size-1:
            player_pos[1] += 1

        elif key == keyboard.Key.left and player_pos[0] > 0:
            player_pos[0] -= 1
            
        elif key == keyboard.Key.right and player_pos[0] < size-1:
            player_pos[0] += 1
            
        if key == keyboard.Key.esc: #Stop the game and listener
            game_is_running = False
            

def image_print(round_nr):
    # Redraw the game screen
    #list comprihention: https://www.youtube.com/watch?v=SNq4C988FjU
    print(f"\tYour {round_nr+1}nd skydive!")
    [print(*y_slices) for y_slices in screen_matrix]
    sleep(0.1)
    
if __name__ == "__main__":
    # Deze manier blokeert het prog niet op de listener, multiprocessing niet nodig:
    listener = keyboard.Listener(
        on_press=on_press)
    listener.start()
    
    "parameters, variabelen"
    # Initialize player position
    player_pos = [10, 10]
    size = 15
    rounds = 2
    n_teller = 0
    r_int_x = randint(0,size-1)
    r_int_y = randint(0,size-1)
    
    "menu loop"
    for round_nr in range(rounds):
        
        sleep(1)
        game_is_running = True
        
        "Game loop"
        while game_is_running:
            empty_plot()
            n_teller += 1
            if n_teller % 25 ==0: 
                r_int_x = randint(0,size-1)
                r_int_y = randint(0,size-1)
            if n_teller % 100 == 0:
                n_teller= 0
            led_toggle(target_x= r_int_x ,target_y= r_int_y , player_pos= player_pos)
            
            image_print(round_nr)
        
        size +=1
    listener.stop() #stops the keyboard listener

    "credits"
    credit = "Disigned by Marius, aka: crtl_alt_delete_"
    
    #Audio
    play_note("G", octave=3, duration= 0.3)
    play_note("F", duration=0.3)
    play_note("B", octave=3, duration=0.3)
    play_note("E", duration=0.3)
    play_note("F", duration=0.3)
    play_note("E", duration=0.3)
    
    for letter in credit:
        sleep(0.07) 
        #my name is bond, james bond
        print(letter, end= "")
    sleep(1.5)
    
