import os
import time
import ctypes
import subprocess
import pickle

from datetime import date
from datetime import datetime

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
start_date = date.today()

time_label = tk.Label(root, text= 'Work time today: ', fg='green', font=('helvetica', 12, 'bold'))
time_label.grid(row=1, column=0, sticky='nesw')

status_label = tk.Label(root, text= 'Status: Work not started', fg='Black', font=('helvetica', 12, 'bold'))
status_label.grid(row=4, column=0, sticky='nesw')

previous_day_label = tk.Label(root, text= '', fg='green', font=('helvetica', 12, 'bold'))
previous_day_label.grid(row=5, column=0, sticky='nesw')

####### Text File to store daily work hours for User Reference #######
day_record = ''
################################################
################################################

def update_time ():
    global day_record, file_object, start_date, hrs, mins, seconds, start_flag, end_flag
    
    if start_flag == True and end_flag == False:
        current_time = time.time()
        time_diff = (current_time - time_start) # In seconds

        hrs = str( ((int)(time_diff/(60*60))) )
        mins = str( ((int)( (time_diff%(60*60))/60)) )
        seconds = str( ((int)( (time_diff%(60*60)) % 60)) )
        
        end_btn.configure(state='normal')
        
        
    elif start_btn['text'] == 'Start':
        end_btn.configure(state='disabled')
         
    if date.today() != start_date or end_flag == True:
        #import ipdb;ipdb.set_trace()
        start_date = date.today()
        previous_day_label.configure(text='Previous Session: ' + hrs + ' Hrs:' + mins + ' Mins:' + seconds + ' Secs ')
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        day_record += ' , End Time: ' + str(current_time)
        day_record +=  ' :: ' + hrs + ' Hrs: ' + mins + ' Mins: ' + seconds + ' Secs \n'
        dict = {'date':str(start_date), 'hrs': hrs, 'mins': mins, 'secs': seconds}
        pickle.dump( dict, open( "data.pickle", "wb" ) )
        
        try:
            file_object = open('work_hours.txt', 'a+')
        except:
            pass
        file_object.write(day_record)
        file_object.close()
        day_record = ''
        hrs = mins = seconds = '0'
        if end_flag == True:
            end_flag = False
        if start_flag == True:
            end_btn.invoke()
            start_btn.invoke()
        
        
    time_label.configure(text = 'Work time today: ' + hrs + ' Hrs:' + mins + ' Mins:' + seconds + ' Secs ')
    root.after(20, update_time)

################################################
################################################    

def close_cb():
    global day_record, file_object, start_date, hrs, mins, seconds, start_flag, end_flag
    if mb.askokcancel("Quit", "Do you want to quit?"):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        day_record += ' , End Time: ' + str(current_time)
        day_record +=  ' :: ' + hrs + ' Hrs: ' + mins + ' Mins: ' + seconds + ' Secs \n'
        dict = {'date':str(start_date), 'hrs': hrs, 'mins': mins, 'secs': seconds}
        pickle.dump( dict, open( "data.pickle", "wb" ) )
        root.destroy()
    
def start (): 
    global day_record, start_date, app_run, hrs, mins, seconds, time_pause, time_start, start_flag, end_flag, previous_lock_state
    start_date = date.today()

    if start_flag == False:
        try:
            load_dict = pickle.load(open( "data.pickle", "rb" ))
            if load_dict['date'] == str(start_date):
                hrs = load_dict['hrs']
                mins = load_dict['mins']
                seconds = load_dict['secs']
        except:
            pass
            
    if day_record == '':
        now = datetime.now()
        today = now.strftime('%d, %b %Y')
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        day_record += 'Date: ' + str(today) + ' , Start Time: ' + str(current_time)
    
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
            
        if process_name in outputstringall:
            locked = True
        else:
            locked = False
        
        if locked and previous_lock_state == 'unlocked' and start_flag == True:     
            start_btn.invoke()
            previous_lock_state = 'locked'

            
        if locked == False and previous_lock_state == 'locked' and start_flag == False:
            start_btn.invoke()
            previous_lock_state = 'unlocked'

        
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
root.protocol("WM_DELETE_WINDOW", close_cb)
root.mainloop()