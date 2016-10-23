from collections import Counter, defaultdict
from candidateGen import candidateGen
import sys
import os
class myApriori():
	def __init__(self):
		self.item = defaultdict(list)
		self.total = 0.0
		self.f = []
		self.f_sup = defaultdict(float)
		return
	def get(self,inputfile,limit):
		count = 0
		try:
			with open(inputfile, 'rt') as file:
				for line in file:
					if (limit != -1):
						if (count > limit):
							file.close()
							return
					count += 1
					transaction = line.split()
					for t in transaction:
						self.item[" "+t].append(count)
					self.total += 1
			file.close()
			return

		except RuntimeError:
			print "myApriori: Something wrong when reading file"
			return

	def apriori(self,minsupport):
		k = 1 
		self.f.append(([]))
		self.f.append(([]))
		for key,value in self.item.iteritems():
			if ((len(value)/self.total) >= minsupport):
				self.f[k].append(key)
				self.f_sup[key] = (len(value)/self.total) 
		self.f[k] = sorted(self.f[k])

		k = 2
		self.f.append(([]))
		while (len(self.f[k-1]) != 0):
			spawner = candidateGen()
			spawner.push(self.f[k-1],k-1)

			candidate = spawner.gen()

			for item in candidate:
				#intersection
				l = []
				for i in item:
					l.append(self.item[i])
				count = len(set(l[0]).intersection(*l))

				if (count/self.total >= minsupport):
					self.f[k].append(item)
					self.f_sup[''.join(item)] = (count/self.total)

			k += 1
			self.f.append(([]))
		return self.f
	def write(self,outputfile):
		# Write output
		try:
			with open(outputfile, "wt") as file:
				for i in self.f:
					for j in i:
						line = ''.join(j)
						file.write(str(self.f_sup[line]))
						file.write(line)
						file.write("\n")
			file.close()
		except ValueError:
			print "Cannot write file"
			return
if __name__ == "__main__":
	"""
	rule = myApriori()
	rule.get("retail.dat",-1)
	rule.apriori(0.01)
	rule.write("output1.dat")
	"""
	rule = myApriori()
	rule.get(sys.argv[1],-1)
	minsup = float(sys.argv[3])
	rule.apriori(minsup)
	rule.write(sys.argv[2])
	