# Example with GenericWrapper for a black box function in Python

This example shows how to provide a wrapper for a Python function using the genericWrapper.
Here, we want to optimize the Branin function, see `braninWrapper.BraninWrapper._get_branin_value()`.
It is a 2-dim function with inputs x1 and x2.

As written in the general README,
you have two provide two functions for the generic wrapper:

  * `get_command_line_args()`
  * `get_command_line_args_ext()`
  
For blackbox functions, we provide with `abstractBlackBoxWrapper.AbstractBlackBoxWrapper` an abstract instantiation of `generic_wrapper.AbstractWrapper` that implements these two functions. 
Still the function to evaluate the black box function is missing, i.e., `AbstractBlackBoxWrapper.get_value()`.
  

`braninWrapper.braninWrapper.get_value()` provides a simple function to convert the provided parameter configuration dictionary in to the arguments for the function `BraninWrapper._get_branin_value()`.

You can run this example on the command line by:

`python examples/BlackBoxPython/braninWrapper.py 0 0 0 0 0 -x1 0 -x2 2`

You don't have care about the leading zeros in the call in this example.
It is only important to note that the value of x1 is set to 0 and x2 to 2.
The Branin function will evaluate to 35.6021126423 for this input.
Therefore, the output include the following line:

Result for ParamILS: SAT, 0, -1, 35.6021126423, 0

