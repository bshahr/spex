from os import listdir
from os.path import isfile, isdir, join
import numpy as np
import re, os, sys, getopt
from bo.demos.testFuncs import computeBest


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
	try:
		folder = folder+'output/'
		onlyfiles = [ f for f in listdir(folder) if isfile(join(folder, f)) ]
	except:
		return []

	onlyfiles = sorted(onlyfiles)

	l = []
	for path in onlyfiles:
		path = folder + path
		try:
			f = open(path)
			l.append(float(f.read().split('\n')[6].split()[-1]))
		except:
			continue

	l = np.asarray(l[:-1], dtype=float)
	m = np.asarray([np.min(l[:i+1]) for i in range(l.shape[0])])

	lm = np.log10(m - (-computeBest(name[:-2])))

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
	try:
		opts, args = getopt.getopt(argv,"hn:s:",["name=","serial="])
	except getopt.GetoptError:
		print 'test.py -i <name> -o <serial>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'gatherResults.py -n <name> -s <serial>'
			sys.exit()
		elif opt in ("-n", "--name"):
			name = arg
		elif opt in ("-s", "--serial"):
			serial = arg

	if not (name == '' or serial == ''):
		processAll(name, serial)
	else:
		print 'gatherResults.py -n <name> -s <serial>'


if __name__ == '__main__':
	main(sys.argv[1:])