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

start_flag = end_flag = False
hrs = mins = seconds = '0'


time_label = tk.Label(root, text= 'Work time today: ', fg='green', font=('helvetica', 12, 'bold'))
#canvas1.create_window(10, 30, window=time_label)
time_label.grid(row=1, column=0, sticky='nesw')

status_label = tk.Label(root, text= 'Status: Work not started', fg='Black', font=('helvetica', 12, 'bold'))
status_label.grid(row=4, column=0, sticky='nesw')

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
        
    time_label.configure(text = 'Work time today: ' + hrs + ' Hrs:' + mins + ' Mins:' + seconds + ' Secs')
    root.after(100, update_time)
        
def start (): 
    global hrs, mins, seconds, time_pause, time_start, start_flag, end_flag
    
    end_flag =  False
    
    if start['text'] != 'Pause':
        time_start = time.time() - (int(hrs)*3600 + int(mins)*60 + int(seconds))
        start.configure(text='Pause', bg='orange')
        start_flag = True
        status_label.configure(text='Status: Work started')
        
    else:
        start.configure(text='Resume', bg='lawngreen')
        start_flag = False
        time_start = time.time() - (int(hrs)*3600 + int(mins)*60 + int(seconds))
        status_label.configure(text='Status: Work paused')
        
def end ():  
    global hrs, mins, seconds, time_end, start_flag, end_flag
    time_end = time.time()
    end_flag = True
    start_flag = False
    hrs = mins = seconds = '0'
    start.configure(text='Start', bg='lawngreen')
    status_label.configure(text='Status: Work ended')
   
    
start = tk.Button(text='Start',command=start, bg='lawngreen',fg='black')
start.grid(row=0, column=0, sticky='nesw')

end = tk.Button(text='End',command=end, bg='red',fg='black')
end.grid(row=3, column=0, sticky='nesw')

root.after(100, update_time)
root.mainloop()