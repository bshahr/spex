language: PYTHON
name:     "rfobj"

variable {
 name: "ntrees"
 type: INT
 size: 1
 min:  1 
 max:  10
}

variable { 
name: "minSamplesSplit"
 type: INT
 size: 1
 min:  1
 max:  100
}

variable {
 name: "maxDepth"
 type: INT
 size: 1
 min:  1
 max:  200
}

variable {
 name: "minSamplesLeaf"
 type: INT
 size: 1
 min:  1
 max:  100
}

variable {
 name: "bootstrap"
 type: INT
 size: 1
 min:  0
 max:  1
}

variable {
 name: "maxFeatures"
 type: INT
 size: 1
 min:  1 
 max:  20
}

