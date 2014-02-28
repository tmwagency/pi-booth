'''
Config file, use like this:

import config
print config.truck['color']

'''

#user_file_url = 'http://www.roowilliams.com/reruh.php'
user_file_url = 'http://gps.tmw.co.uk/ajax/user_list.php'




# example to show format/nesting
truck = dict(
    color = 'blue',
    brand = 'ford',
)
city = 'new york'
cabriolet = dict(
    color = 'black',
    engine = dict(
        cylinders = 8,
        placement = 'mid',
    ),
    doors = 2,
)
