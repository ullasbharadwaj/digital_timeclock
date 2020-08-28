import os
import time
import ctypes
import subprocess
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox as mb


"""
General configuration and global variable
"""

root= tk.Tk()

root.title("Digital Timeclock")

user32 = ctypes.windll.User32
previous_lock_state = ''
process_name='LogonUI.exe'
callall='TASKLIST'

time_start = 0
time_end = 0

start_flag = end_flag = False
hrs = mins = seconds = '0'

app_run = False

time_label = tk.Label(root, text= 'Work time today: ', fg='green', font=('helvetica', 12, 'bold'))
time_label.grid(row=1, column=0, sticky='nesw')

status_label = tk.Label(root, text= 'Status: Work not started', fg='Black', font=('helvetica', 12, 'bold'))
status_label.grid(row=4, column=0, sticky='nesw')

################################################
################################################

def update_time ():
    global hrs, mins, seconds, start_flag, end_flag
    
    if start_flag == True and end_flag == False:
        current_time = time.time()
        time_diff = (current_time - time_start) # In seconds

        hrs = str( ((int)(time_diff/(60*60))) )
        mins = str( ((int)( (time_diff%(60*60))/60)) )
        seconds = str( ((int)( (time_diff%(60*60)) % 60)) )
    
    if end_flag == True:
        hrs = mins = seconds = '0'
        
    time_label.configure(text = 'Work time today: ' + hrs + ' Hrs:' + mins + ' Mins:' + seconds + ' Secs ')
    root.after(20, update_time)

################################################
################################################    

def start (): 
    global app_run, hrs, mins, seconds, time_pause, time_start, start_flag, end_flag, previous_lock_state
    app_run = True
    end_flag =  False
    previous_lock_state = 'unlocked'
    
    if start_btn['text'] != 'Pause':
        time_start = time.time() - (int(hrs)*3600 + int(mins)*60 + int(seconds))
        start_btn.configure(text='Pause', bg='orange')
        start_flag = True
        status_label.configure(text='Status: Work started')
    else:
        start_btn.configure(text='Resume', bg='lawngreen')
        start_flag = False
        #time_start = time.time() - (int(hrs)*3600 + int(mins)*60 + int(seconds))
        status_label.configure(text='Status: Work paused')

################################################
################################################
        
def end ():  
    global app_run, hrs, mins, seconds, time_end, start_flag, end_flag
    time_end = time.time()
    end_flag = True
    start_flag = app_run = False
    hrs = mins = seconds = '0'
    start_btn.configure(text='Start', bg='lawngreen')
    status_label.configure(text='Status: Work ended')

################################################
"""
    Function to monitor screen for locked 
    and unlocked screens
"""
################################################
   
def check_screen():
    global app_run, user32, previous_lock_state, time_start, hrs, mins, seconds, start_flag, process_name, callall
    message = ''
    if app_run == True:
        outputall = subprocess.check_output(callall)
        outputstringall=str(outputall)
            
        if process_name in outputstringall:#lock_cnt > 4:
            locked = True
        else:
            locked = False
        
        if locked and previous_lock_state == 'unlocked' and start_flag == True:     
            start_btn.invoke()
            previous_lock_state = 'locked'
            print('locked' + time_label['text'])
            
        if locked == False and previous_lock_state == 'locked' and start_flag == False:
            start_btn.invoke()
            previous_lock_state = 'unlocked'
            print('unlocked'+ time_label['text'])
        
    root.after(10, check_screen) 
    
################################################
"""
                Setup buttons
"""
################################################
    
start_btn = tk.Button(text='Start',command=start, bg='lawngreen',fg='black')
start_btn.grid(row=0, column=0, sticky='nesw')

end_btn = tk.Button(text='End',command=end, bg='red',fg='black')
end_btn.grid(row=3, column=0, sticky='nesw')

root.after(10, check_screen)
root.after(20, update_time)
root.mainloop()