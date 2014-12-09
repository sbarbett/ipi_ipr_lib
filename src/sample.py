# Copyright 2014 NeuStar, Inc.All rights reserved.
# NeuStar, the Neustar logo and related names and logos are registered
# trademarks, service marks or tradenames of NeuStar, Inc. All other
# product names, company names, marks, logos and symbols may be trademarks
# of their respective owners.
__author__ = 'Shane Barbetta'

import connection, sys

if len(sys.argv) != 2:
    raise Exception('Expected use: python sample.py ip')
    
ip = sys.argv[1]

c = connection.ApiConnection()

print 'IP data:\n%s' % c.get(ip)
print 'Reputation:\n%s' % c.get(ip, True)