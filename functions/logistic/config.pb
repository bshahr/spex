language: PYTHON
name:     "logistic"

variable {
 name: "lrate"
 type: FLOAT
 size: 1
 min:  0
 max:  10
}

#variable {
# name: "l1_reg" 
# type: FLOAT
# size: 1
# min:  1
# max:  2.7
#}

variable { 
name: "l2_reg"
 type: FLOAT
 size: 1
 min:  0
 max:  1
}

variable {
 name: "batchsize"
 type: INT
 size: 1
 min:  20
 max:  2000
}

variable {
 name: "n_epochs"
 type: INT
 size: 1
 min:  5
 max:  2000
}

# Integer example
#
# variable {
#  name: "Y"
#  type: INT
#  size: 5
#  min:  -5
#  max:  5
# }

# Enumeration example
# 
# variable {
#  name: "Z"
#  type: ENUM
#  size: 3
#  options: "foo"
#  options: "bar"
#  options: "baz"
# }


