# digital_timeclock
A utterly simple digital time clock to keep track of work timings when in home office. This gonna help the folks who are currently working from home and needs to keep track of work hours. 


The digital timeclock, once started, is completely automated with reference to the login activity. This means, as long as the user has logged on to the PC, timer would be running and when user locks the screen, the timer would go into the paused mode. The digital timeclock also offers utility to start, pause and resume the timer at the request of the user manually.


The script is written with Python 3 and the windows executable is generated using pyinstaller.

Procedure to use the script:

1. Clone the repo
2. Setup Python on windows machine
3. Install pyinstaller package using pip. $: pip3 install pyinstaller
4. Generate exe execuatable for windows. $: pyinstaller --onefile TimeClock.py
5. This creates a dist directory with the distributable exe file

This can also be run simply from command line.

$: python TimeClock.py

Hope this helps :-)
