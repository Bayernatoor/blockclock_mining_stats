# BLOCKCLOCK SLUSHPOOL STAT DISPLAYER

A basic Python script that allows you to broadcast current slushpool bitcoin mining info from your user profile directly to your BlockClock Mini (https://blockclockmini.com/)

![thsblockclock](https://user-images.githubusercontent.com/55212954/158614788-8b850940-fb42-4c6b-ae84-7055e81db1b9.jpg)

**Display the following Slushpool tags:**

1. Confirmed Reward
2. Unconfirmed Rewards
3. Estimated Reward
4. Alltime Reward
5. Hashrate 5m
6. Hashrate 60m
7. Hashrate 24h
8. Hashrate Scoring
9. Active Workers
10. Offline Workers
11. Estimate Hash Rate
12. USD Market Price
13. EUR Market Price
14. GBP Market Price
15. Sats per Dollar
16. Mempool Transactions
17. Difficulty Retarget Date
18. Blockchain Height
19. Moscow Time

*Got requests for other tags? Let me know!*

----------------------

## Setup:

First you'll want to obtain your **Blockclock's IP** address as well as a **Slushpool Auth Token**.

### Getting your Blockclock IP address:

This assume's that you have already setup your Blockclock Mini. 

If you need your Blockclock's IP, press on the second button from the top on the right side of the Blockclock. 

You'll see an IP address, likely in the 5th square. Enter that IP in a browser. 

You'll now have access to your Blockclock's settings page. On the **Display Page**, go down to **Display Preferences**, set **Screen Update Rate** to **Manual**.

That is all! 

### Getting your Slushpool Auth Token:

Login:
https://slushpool.com/login/

1. Click on the icon on the right of your username in the top right corner.
2. Click on **Devices**
3. Click on **Access Profiles**
4. Click on **Create New**
5. Add a username. **Access Permissions** can be set to **read-only**. 
   Check-off **Allow access to web APIs**, click **Generate new token** and copy that **Auth Token**. 
   FInally, click on **Create Access Profile**.

**Keep that IP address and Auth Token handy.**

### Get the script and setup

Open a terminal and ```cd``` into any directory you wish to store the script, run the following commands:

```
git clone https://github.com/Bayernatoor/blockclock_mining_stats.git && cd blockclock_mining_stats

python3 -m venv env && . env/bin/activate && pip install -r requirements.txt 
```

*After running the above command you should be in the virtual environment. You'll want to make sure you are active the virtual enviro every time you run the app. To enter you run ```. env/bin/activate``` from within the ```blockclock_slushpool``` directory then ```cd blockclock_slushpool``` to access the directory to run the script ```python3 blockclock_slushpool.py```. To exit the virtual environment enter ```deactivate``` in the terminal while in the project  directory.* 

Now let's add that IP and Auth Token to the script, enter the following: 

```
cd blockclock_slushpool

nano blockclock_slushpool.py
```

If you do not have **nano** installed simply open the **blockclock_slushpool.py** file with a text editor.

Add your Slushpool Auth Token and your Blockclock IP address at the top of the file **(you'll see variables asking for that info, remove the text and the < > but add the IP and Token within the  quotes - "IP". )**

**Now save that file and close it**

*Warning: make sure not to push or publish this file online since it now contains private information. These will be separated out of the main script in a later update.*

### Run the app

From within the **blockclock_slushpool/blockclock_slushpool** directory run the following:

```
python3 blockclock_slushpool.py
```
If you get an error such as: ```can't open file ... [Errno 2] No such file or directory```

Double check that you are in the correct directory, it should contain the file called ```blockclock_slushpool.py```.

The script will start, you can follow the instructions in the terminal.

------------------------------------

**I hope you enjoy. This is a little project to help me better learn Python and bitcoin.**

**I plan to continue updating this script, the setup needs to be improved and the overall structure of the app as well. Got any tips/improvements/feedback or notice some bugs i'd love to hear about it! Just open an issue!** :D
