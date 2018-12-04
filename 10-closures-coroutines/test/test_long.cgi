#!/usr/bin/python

import cgi
import cgitb; cgitb.enable()
import time

print "Content-type:text/html\r\n\r\n"
print '<html>'
print '<head>'
print '<title>Hello Word - First CGI Program</title>'
print '</head>'
print '<body>'
print '<h2>Hello Word! This is my first CGI program</h2>'
print '<p>Script 10 second sleep</p>'
arguments = cgi.FieldStorage()
for i in arguments.keys():
    print arguments[i].value
time.sleep(10)
print '</body>'
print '</html>'

