import sys
import re
from collections import Counter

def composer(file):
	r = re.compile("Composer: (.*)" )
	counter = Counter()
	
	for line in file:
		m = r.match(line)
		if m:
			name = m.group(1).strip()
			for n in name.split(';'):
	 			counter[n.strip()] += 1
	 
	for k, v in counter.items():
		print("%s: %d" % (k, v))
	
def century(file):
	# todo
	print('century')

def main():	
	file = sys.argv[1]
	stat = sys.argv[2]	
	
	f = open(file, 'r')
	
	if (stat == 'composer'):
		composer(f)
	elif (stat == 'century'):
		century(f)

main()
