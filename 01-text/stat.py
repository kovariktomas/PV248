#!/usr/bin/env python3

import sys
import re
from collections import Counter

def composer(file):
	r = re.compile("Composer: (.*)" )
	
	r1 = re.compile("(.*)(\((\+)*\d{4}(.*)\)){1}")
	counter = Counter()
	
	for line in file:
		m = r.match(line)
		if m:
			name = m.group(1).strip()
			for n in name.split(';'):
				match = r1.match(n);
				if match:
	 				counter[match.group(1).strip()] += 1
				elif (not (n =="")):
	 				counter[n.strip()] += 1
	 
	for k, v in counter.items():
		print("%s: %d" % (k, v))
	
def century(file):
	r = re.compile("Composition Year: (.*)(\d{4})(.*)")
	
	r2 = re.compile("Composition Year: (\d{2})th century(.*)")
	
	r1 = re.compile("(\d{4})(.*)")
	counter = Counter()
	
	for line in file:
		m = r.match(line)
		m1 = r2.match(line)
		if m:
			group1 = m.group(1).strip()
			year = r1.match(group1)
			if year:
				counter[(int(year.group(1).strip()[:2])+1)] += 1
				
			group2 = m.group(2).strip()
			year = r1.match(group2)
			if year:
				counter[(int(year.group(1).strip()[:2])+1)] += 1
				
			group3 = m.group(3).strip()
			year = r1.match(group3)
			if year:
				counter[(int(year.group(1).strip()[:2])+1)] += 1
		elif m1:
			century = m1.group(1).strip()
			counter[int(century)] += 1
				
	for k, v in counter.items():
		print("%sth century: %d" % (k, v))
		
def key(file):
	r = re.compile("Key: (.*)" )
	counter = Counter()
	
	for line in file:
		m = r.match(line)
		if m:
			name = m.group(1).strip()
			for n in name.split(';'):
				for n1 in n.split(','):
					for n2 in n1.split(' '):
						if (n2.strip() == "c"):
							counter[n2.strip()] += 1
						elif (n2.strip()=="C"):
							counter[n2.strip()] += 1
	 
	for k, v in counter.items():
		print("Key %s: %d" % (k, v))

def main():	
	file = sys.argv[1]
	stat = sys.argv[2]	
	
	f = open(file, 'r')
	
	if (stat == 'composer'):
		composer(f)
	elif (stat == 'century'):
		century(f)
	elif (stat == 'key'):
		key(f)

main()
