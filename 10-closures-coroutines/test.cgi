#!/usr/bin/python

import cgi
import cgitb; cgitb.enable()


print "Content-type:text/html\r\n\r\n"
print '<html>'
print '<head>'
print '<title>Hello Word - First CGI Program</title>'
print '</head>'
print '<body>'
print '<h2>Hello Word! This is my first CGI program</h2>'
print '</body>'
print '</html>'
arguments = cgi.FieldStorage()
print len(arguments)
for i in arguments.keys():
    print arguments[i].value