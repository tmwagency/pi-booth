<<<<<<< HEAD
=======
import urllib2
import sys
from collections import defaultdict
import config
import gaugette.rotary_encoder
import gaugette.switch
import Queue
import time
from threading import Thread
>>>>>>> 28efcc383bd4916a6ed66ac52c1f62ee0257c6a1


<<<<<<< HEAD
=======
A_PIN  = 7
B_PIN  = 9
SW_PIN = 8



def init_users(q, userfile_url):
    users = defaultdict(list)
    data = urllib2.urlopen(userfile_url)

    for line in data.readlines():
        id, username, _ = line.split(", ", 2)
        users[username[:1].lower()].append((username, id))     
    q.put(users)
    print '---------------got users'
        
def return_users():
    thr = Thread(target=init_users, args=(q, config.user_file_url,))
    thr.start()
    thr.join()
    users = q.get()
    return users

encoder = gaugette.rotary_encoder.RotaryEncoder.Worker(A_PIN, B_PIN)
encoder.start()
switch = gaugette.switch.Switch(SW_PIN)
last_state = None

while 1:
    delta = encoder.get_delta()
    time.sleep(0.02)
    if delta!=0:
        print "rotate %d" % delta

    sw_state = switch.get_state()
    if sw_state != last_state:
        print "switch %d" % sw_state
        last_state = sw_state


>>>>>>> 28efcc383bd4916a6ed66ac52c1f62ee0257c6a1
