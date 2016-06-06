#Wrapper for SGD

This is a more advanced example for optimizing a black box function (here SGD on a fixed data set).

The target algorithm is a simple python script `sgd_ta.py` which loads the iris data set from sklearn, reads the parameter configuration, fits a SGD classifier and prints the accuracy on a holdout set.

The script supports three kind of "instances":

  1. if the instance is "train", we split the data into train, validation and test set, and train SGD on train and evaluate it on valid
  2. if the instance is "test", we split the data into train (train+validation) and test set, and train SGD on train and evaluate it on test
  3. if the instance is "cvX", we split the data into train and test, and further use a k-fold CV on train; the X-th split is used for training and evaluation   

The `SGDWrapper.py` implements the required two functions:

  1. `get_command_line_args()` that generates the command line call by starting with the call of the sgd script, adds the random seed as a parameter called `random_state` (as done in sklearn) and adds all parameters to the command line call
  1. `process_results()` reads only the printed accuracy from the `sgd_ta.py` script and returns it as the quality of the function.
  
An example call of the wrapper would be:

`python examples/SGD/SGDWrapper.py 0 0 5 0 9 -learning_rate constant -eta0 1`

which is translated to 

`python examples/SGD/sgd_ta.py random_state 9 eta0 1 learning_rate constant`

Please note that in contrast to the `BlackBoxPython` example, the resources of the SGD script is indeed limited with the runsolver (here 5 CPU seconds.)


  