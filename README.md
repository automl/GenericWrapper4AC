# Generic Wrapper for Algorithm Configuration

The generic wrapper is a base class to easily implement your own interface between your algorithm and an algorithm configurator (such as ParamILS or SMAC).

The generic wrapper is developed and maintained by members of the [ML4AAD](http://www.ml4aad.org) Group at the University of Freiburg and the [Beta Lab](http://www.cs.ubc.ca/labs/beta/) of the university of British Columbia. 

## USAGE

The generic wrapper provides the interfaces to ParamILS and SMAC. Please see the [documentation of SMAC](http://www.cs.ubc.ca/labs/beta/Projects/SMAC/v2.10.03/manual.pdf) for an extensive description of the required interfaces.

The script `generic_wrapper.py` provides the class `AbstractWrapper`. It provides all necessary functions to run your algorithms, including:

  * reading the input format of ParamILS and SMAC
  * limiting the resources (CPU and memory) by using the [runsolver](http://www.cril.univ-artois.fr/~roussel/runsolver/)
  * returning the output in ParamILS and SMAC format
  
You have to implement only two functions

  * `get_command_line_args()`
  *  `get_command_line_args_ext()`
  
See the docstrings and the examples for more details.

## Requirements

Since we use the `runsolver` to limit resources, the generic wrapper can only be used on Linux systems.

## Examples

Please see `./examples/` for some examples with black box functions (no problem instances included) and examples of algorithms with problem instances (i.e., SAT solving). 

We provide a more extensive tutorial for "How to write your own Wrapper" with using the GenericWrapper [here](http://aclib.net/smac/tutorial/genericwrapper/).

## License

The generic wrapper base class is published under a BSD license -- please see LICENSE for more details.
The used runsolver was written by Olivier Roussel and is published under GPLv3.0 -- see `runsolver/` 
Please note that not all code provided in the examples are under a BSD license -- please check the license for these examples separately.

## Contributors

  * Marius Lindauer
  * Katharina Eggensperger
  * Chris Fawcett
  * Frank Hutter