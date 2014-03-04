import urllib2
import sys
from collections import defaultdict
import config

users = defaultdict(list)

def init_users(userfile_url):
    data = urllib2.urlopen(userfile_url)

    for line in data.readlines():
        id, username, _ = line.split(", ", 2)
        users[username[:1].lower()].append((username, id))

    #print(users.keys())

def return_users():
    init_users(config.user_file_url)
    return sorted(users)


def render_users():
    init_users(config.user_file_url)
    for key in sorted(users.iterkeys()):
        print(key)
        for name, value in users[key]:
            print(" " + name)

def request_user():
    input_var = raw_input("Enter your username: ")
    get_user_guid(input_var)
    
def get_user_guid(input_var):
    input_var_key = input_var[:1].lower()
    if input_var == 'c':
        print 'exit'
        sys.exit()
    try:
        guid = [s for s in users[input_var_key] if input_var in s][0][1]
        print ("The guid for your username is: " + guid)
    except IndexError:
        print "Username not found, try again or type 'c' to cancel."
        request_user()

#render_users()
