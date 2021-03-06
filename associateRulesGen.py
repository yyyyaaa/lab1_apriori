from collections import defaultdict
import sys
import itertools
class associateRulesGen():
	def __init__(self):
		self.sup = defaultdict(float)
		self.f = defaultdict(list)
		self.rule = []
		self.conf_rule = []
		return
	def get(self,inputfile):
		try:
			with open(inputfile, "rt") as file:
				for line in file:
					sup,can = line.strip().split(' ', 1)
					self.sup[can] = float(sup)
					can = can.split()
					self.f[len(can)].append(can)
			file.close()
			return
		except RuntimeError:
			print "Something wrong when reading file"
			return
	def apgen(self,f,k,h,m,minconf):
		if (k > m+1) and (len(h[m]) != 0):
			for t1,t2 in itertools.combinations(h[m],2):
				h.append([])
				#if (m==1):
				#	t1 = [t1]
				#	t2 = [t2]
				if (t1[:-1] == t2[:-1]):
					t = t1+t2[-1:]
					rule = [[x for x in f if x not in t],t]
					if (self.sup[" ".join(f)]/self.sup[" ".join(rule[0])] >= minconf):
						self.rule.append(rule)
						self.conf_rule.append(self.sup[" ".join(f)]/self.sup[" ".join(rule[0])])
						h[m+1].append(rule[1])
			self.apgen(f,k,h,m+1,minconf)


	def gen(self,minconf,k):

		for f in self.f[k]:
			#print f
			h = [[],[]]
			m = 1
			for p in itertools.permutations(f):
				#print p
				rule = [list(p[:-1]),[p[-1]]]
				if (self.sup[" ".join(rule[0])] == 0.0):
					continue
				if (self.sup[" ".join(f)]/self.sup[" ".join(rule[0])] >= minconf):
					self.rule.append(rule)
					self.conf_rule.append(self.sup[" ".join(f)]/self.sup[" ".join(rule[0])])
					h[m].append(rule[1])

			self.apgen(f,k,h,m,minconf)
		
		#for rule in self.rule:
		#	print rule

	def write(self,outputfile):
		# Write output
		count = 0
		try:
			with open(outputfile, "wt") as file:
				for rule in self.rule:
					line = "{0:.2f} ".format(self.conf_rule[count]) +' '.join(rule[0]) + " -> " + ' '.join(rule[1])
					file.write(line)
					file.write("\n")
					count += 1
			file.close()
		except:
			print "Cannot write file"
			return
if __name__ == "__main__":
	"""
	rulegen = associateRulesGen()
	rulegen.get("output1.dat")
	k = 1
	if (k>1):
		rulegen.gen(0.4,k)
	else:
		for key in rulegen.f.keys():
			print key
			rulegen.gen(0.1,key)
	rulegen.write("output2.dat")
	"""
	rulegen = associateRulesGen()
	rulegen.get(sys.argv[1])
	k = int(sys.argv[4])
	minconf = float(sys.argv[3])
	if (k>1):
		rulegen.gen(minconf,k)
	else:
		for key in rulegen.f.keys():
			rulegen.gen(minconf,key)
	rulegen.write(sys.argv[2])