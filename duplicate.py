import os
import distutils.core
import re
import random

def copyFolder(name='braninpy', num=20):

	def getPath(subfolder):
		lpath = re.sub(r'duplicate.pyc?', subfolder, \
        	os.path.abspath(__file__))
		return lpath

	origPath = getPath('fcts/{}/'.format(name))


	serial = str(random.randint(1e9, 1e10))
	
	for i in range(num):
		destPath = getPath('{0}/{1}-{2}-{3}/'.format(\
			'copies', name, serial, i+1))
		os.mkdir(destPath)
		distutils.dir_util.copy_tree(origPath, destPath)


	print 'serial:', serial
	return serial

if __name__ == '__main__':
	copyFolder()
