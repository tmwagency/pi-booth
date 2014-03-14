import urllib2
import sys
from collections import defaultdict
import config
import gaugette.rotary_encoder
import gaugette.switch
import Queue
import time
from threading import Thread

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
