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


def render_users():
    for key in users.iterkeys():
        print(key)
        for i in range(0,len(users[key])):
            print(" " + users[key][i][0])

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



# Do we want the user file to be pulled every time someone tries to use the photobooth?
# TODO: Find out latency between a new user entering the building and the list getting updated

init_users(config.user_file_url) #url as string

#create the view
render_users()

#request user input to return guid
request_user()















'''
def users_update(userfile_url):
    data = urllib2.urlopen(userfile_url)
    data = data.readlines()
    print "Retrieved userfile"

    prevchar = ""
    lettercount = 0
    

    for line in data:
        vals = line.split(", ")

    

        thischar = vals[1][0].lower()
        print thischar
        if thischar == prevchar:
            lettercount += 1
        else:
            print str(lettercount) + "  usernames begin with " + thischar
            lettercount = 0

        prevchar = thischar

'''

