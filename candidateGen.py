import sys
import os
import itertools
from collections import defaultdict

class candidateGen():
	def __init__(self):
		#transactions:
		#	a b c
		#	a b e
		#	a b c d
		#data:
		#	data[" a b"] = [" c"]
		#	data[" a b"] = [" c"," e"]
		#	data[" a b c"] = [" d"]

		self.data = defaultdict(list)
		self.candidate = []
	def get(self,inputfile,limit):
		count = 0
		try:

			with open(inputfile, "rt") as file:
				for line in file:
					if (limit != -1):
						if (count > limit):
							file.close()
							return
					count +=1
					temp = " ".join(sorted(line.split()))
					temp = temp.strip().rsplit(' ', 1)
					if len(temp) == 1:
						if (" "+temp[0]) not in self.data[" "]:
							self.data[" "].append(" "+temp[0])
						continue
					key,value = temp
					value = " "+value
					key = " " + key
					if (value not in self.data[key]):
						self.data[key].append(value)
						list_item = line.split()
			file.close()
			return
		except RuntimeError:
			print count
			print line
			print "Something wrong when reading file"
			return
	def push(self,transactions,k):
		if k == 1:
			self.data[' '] += transactions
			return
		for t in transactions:
			self.data[''.join(t[0:-1])].append(t[-1])
	def gen(self):
		for key,value in self.data.iteritems():
			if (len(value) >= 2):
				for t1,t2 in itertools.combinations(sorted(value),2):
					new_set = (key + t1 + t2).split()
					flag = True
					if (len(new_set) == 2):
						self.candidate.append([' {}'.format(x) for x in new_set])
						continue
					
					for list_new_item in itertools.combinations(new_set,len(new_set)-1):
						k = " " + (' '.join(list_new_item[0:-1]))

						if k in self.data:
							if ((" " + list_new_item[-1]) not in self.data[k]):
								flag = False
								break
						else:
							flag = False
							break
					if (flag):
						self.candidate.append([' {}'.format(x) for x in new_set])
		self.candidate = sorted(self.candidate)
		return self.candidate
	def write(self,outputfile):
		
		# Write output
		try:
			with open(outputfile, "wt") as file:
				for c in self.candidate:
					line = ''.join(c).strip()
					file.write(line)
					file.write("\n")
			file.close()
		except:
			print "Cannot write file"
			return
			

if __name__ == "__main__":
	"""
	spawner = candidateGen()
	spawner.get("retail1.dat",-1)
	spawner.gen()
	spawner.write("output.dat")
	"""
	#-1 all
	spawner = candidateGen()
	spawner.get(sys.argv[1],-1)
	spawner.gen()
	spawner.write(sys.argv[2])

