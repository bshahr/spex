import os
import distutils.core
import re
import random

def write_PBS_script(num, path, codeline, serial):
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
#PBS -l nodes=1:ppn=2

cd $PBS_O_WORKDIR
echo "Current working directory is `pwd`"
echo PBS_ARRAYID=$PBS_ARRAYID
# Run
echo "Starting run: $(date)"
{}
echo "Run complete: $(date)"
""".format(num, codeline)
	
	fname = path + 'job_scripts_{}.pbs'.format(serial)
	f = open(fname, 'w')
	f.write(content)
	f.close()

	return fname


def getPath(subfolder):
	lpath = re.sub(r'duplicate.pyc?', subfolder, \
    	os.path.abspath(__file__))
	return lpath


def prepareSpearmint(name='braninpy', num=20):

	

	origPath = getPath('fcts/{}/'.format(name))


	serial = str(random.randint(1e9, 1e10))
	
	for i in range(num):
		destPath = getPath('{0}/{1}-{2}-{3}/'.format(\
			'copies', name, serial, i+1))
		os.mkdir(destPath)
		distutils.dir_util.copy_tree(origPath, destPath)


	line = '{}job_scripts/runscript.sh {} {} $PBS_ARRAYID'.\
		format(getPath(''), name, serial)

	fname = write_PBS_script(num, getPath('job_scripts/'), line, serial)


	execute = 'qsub -l walltime=5:00:00,mem=2gb {}'.format(fname)
	print execute

	return serial

def preparePybo(name='branin', num=20):

	serial = str(random.randint(1e9, 1e10))
	line = 'python {}job_scripts/runSynthetic.py -n {} -s {} -a $PBS_ARRAYID'.\
		format(getPath(''), name, serial)

	fname = write_PBS_script(num, getPath('job_scripts/'), line, serial)

	execute = 'qsub -l walltime=5:00:00,mem=2gb {}'.format(fname)
	print execute

	return serial


if __name__ == '__main__':
	# prepareSpearmint('braninpy', 20)
	preparePybo('branin', 20)
	# copyFolder('hart3py', 20)
	# copyFolder('hart6py', 20)

	
	
