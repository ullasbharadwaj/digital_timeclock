import os
import time
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox as mb

root= tk.Tk()

root.title("Digital Timeclock for Home Office")


time_start = 0
time_end = 0
time_pause = 0
start_flag = pause_flag = end_flag = False
hrs = mins = seconds = '0'

time_label = tk.Label(root, text= 'Work time today: ', fg='green', font=('helvetica', 12, 'bold'))
#canvas1.create_window(10, 30, window=time_label)
time_label.grid(row=1, column=0, sticky='nesw')

status_label = tk.Label(root, text= 'Status: Work not started', fg='Black', font=('helvetica', 12, 'bold'))
status_label.grid(row=4, column=0, sticky='nesw')

def update_time ():
    global hrs, mins, seconds, start_flag, pause_flag, end_flag
    if start_flag == True and pause_flag == False and end_flag == False:
        current_time = time.time()
        
        time_diff = (current_time - time_start) # In seconds
        hrs = str( ((int)(time_diff/(60*60))) )
        mins = str( ((int)( (time_diff%(60*60))/60)) )
        seconds = str( ((int)( (time_diff%(60*60)) % 60)) )
    
    time_label.configure(text = 'Work time today: ' + hrs + ' Hrs:' + mins + ' Min:' + seconds + ' Secs')
    root.after(100, update_time)
        
def start (): 
    global time_start, start_flag, pause_flag, end_flag
    time_start = time.time()
    start_flag = True
    end_flag = pause_flag = False
    status_label.configure(text='Status: Work started')

def pause ():  
    global time_pause, start_flag, pause_flag, end_flag
    time_pause = time.time()
    pause_flag = True
    start_flag = end_flag = False
    status_label.configure(text='Status: Work paused')

def end ():  
    global time_end, start_flag, pause_flag, end_flag
    time_end = time.time()
    end_flag = True
    start_flag = pause_flag = False
    status_label.configure(text='Status: Work ended')
   
    
start = tk.Button(text='Start',command=start, bg='green',fg='black')
start.grid(row=0, column=0, sticky='nesw')

pause = tk.Button(text='Pause',command=pause, bg='orange',fg='black')
pause.grid(row=2, column=0, sticky='nesw')

start = tk.Button(text='End',command=end, bg='red',fg='black')
start.grid(row=3, column=0, sticky='nesw')

root.after(100, update_time)
root.mainloop()