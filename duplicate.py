import os
import distutils.core
import re
import random

def write_PBS_script(folder, serial, num, path):
	content = """
#!/bin/bash
#PBS -S /bin/bash

#!/bin/sh
# Script for running serial program, diffuse.

#PBS -l walltime=02:00:00
#PBS -l mem=2000mb
#PBS -t 1-{}
#PBS -r n
#PBS -M ziyucwang@gmail.com
#PBS -m bea
#PBS -V
#PBS -l nodes=1:ppn=4

cd $PBS_O_WORKDIR
echo "Current working directory is `pwd`"
echo PBS_ARRAYID=$PBS_ARRAYID
# Run
echo "Starting run: $(date)"
/home/ziyuw/projects/expSpearmint/job_scripts/runscript.sh {} {} $PBS_ARRAYID
echo "Run complete: $(date)"
""".format(num, folder, serial)
	
	fname = path + 'job_scripts_{}.pbs'.format(serial)
	f = open(fname, 'w')
	f.write(content)
	f.close()

	return fname


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


	fname = write_PBS_script(name, serial, num, getPath('job_scripts/'))


	execute = 'qsub -l walltime=5:00:00, mem=2gb {}'.format(fname)
	print execute

	return serial

if __name__ == '__main__':
	copyFolder('braninpy', 20)
	# copyFolder('hart3py', 20)
	# copyFolder('hart6py', 20)

	
	
