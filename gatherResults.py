from os import listdir
from os.path import isfile, isdir, join
import numpy as np
import re, os, sys, getopt
from numpy import genfromtxt
import string


def getPath(subfolder):
	lpath = re.sub(r'gatherResults.pyc?', subfolder, \
    	os.path.abspath(__file__))
	return lpath

def findFolders(name='braninpy', serial='9859162815'):
	cdir = getPath('copies/')
	folders = [ cdir + f + '/' for f in listdir(cdir) \
		if isdir(join(cdir,f)) \
		and f.split('-')[0] == name and f.split('-')[1] == serial]
	return folders


def processFile(name, folder):
	# try:
	# 	folder = folder+'output/'
	# 	onlyfiles = [ f for f in listdir(folder) if isfile(join(folder, f)) ]
	# except:
	# 	return []

	# onlyfiles = sorted(onlyfiles)

	# l = []
	# for path in onlyfiles:
	# 	path = folder + path
	# 	try:
	# 		f = open(path)
	# 		for line in f.read().split('\n'):
	# 			if string.join(line.split()[:2]) == 'Got result':
	# 				l.append(float(line.split()[-1]))
	# 	except:
	# 		continue
	# l = np.asarray(l[:-1], dtype=float)
	# lm = np.asarray([np.min(l[:i+1]) for i in range(l.shape[0])])
	
	d = genfromtxt('{}trace.csv'.format(folder), delimiter=',')[:, [1, 5]]
	_, indices = np.unique(d[:, 1], return_index=True)
	indices = [int(index) for index in indices if index > 0]
	lm = d[indices, 0]
	if lm.shape[0] < 300:
		lm = np.hstack([lm, lm[-1]*np.ones(300-lm.shape[0])])

	return lm


def processAll(name='braninpy', serial='9859162815'):
	folders = findFolders(name, serial)


	all_results = []
	for folder in folders:
		ldis = processFile(name, folder)
		all_results.append(ldis)

	np.save('./result-{}-{}.mat'.format(name, serial), \
		np.vstack(all_results))

def main(argv):                         
	name = ''
	serial = ''
	usage = 'gatherResults.py -n <name> -s <serial>'
	try:
		opts, args = getopt.getopt(argv,"hn:s:",["name=","serial="])
	except getopt.GetoptError:
		print usage
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print usage
			sys.exit()
		elif opt in ("-n", "--name"):
			name = arg
		elif opt in ("-s", "--serial"):
			serial = arg

	if not (name == '' or serial == ''):
		processAll(name, serial)
	else:
		print usage


if __name__ == '__main__':
	main(sys.argv[1:])

