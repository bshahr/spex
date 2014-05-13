from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cross_validation import cross_val_score
import numpy as np
import os, re
from sklearn.datasets import fetch_mldata

def rfwine(n_estimators=20, max_depth=15, \
		min_samples_split=5, min_samples_leaf=30, bootstrap=0, max_features=5):
	lpath = re.sub(r'rfobj.pyc?', '', \
        os.path.abspath(__file__))

	features = np.load('{}mnistFeatures.npy'.format(lpath))
	labels = np.load('{}mnistFeatures.npy'.format(lpath))

	mnist = fetch_mldata('MNIST original')
	features = mnist['data']
	labels = mnist['target']
	
	clf = RandomForestClassifier(n_estimators=n_estimators, \
		max_depth=max_depth, min_samples_split=min_samples_split, \
		min_samples_leaf=min_samples_leaf, bootstrap=bootstrap, \
		max_features=max_features, random_state=0)
	scores = cross_val_score(clf, features, labels)
	return 1. - scores.mean()


def main(job_id, params):
	n_estimators=params['ntrees']
	max_depth=params['maxDepth']
	min_samples_split = params['minSamplesSplit']
	min_samples_leaf = params['minSamplesLeaf']
	bootstrap = params['bootstrap']
	max_features = params['maxFeatures'][0]
	
	return rfwine(n_estimators=n_estimators, max_depth=max_depth, \
		min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, \
		bootstrap=bootstrap, max_features=max_features)



if __name__ == "__main__":
	print rfwine(n_estimators=10, max_depth=None, \
		min_samples_split=2, min_samples_leaf=1, bootstrap=True, max_features='auto')