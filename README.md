[![Project Status: Active - The project has reached a stable, usable state and is being actively developed.](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
[![Build Status](https://travis-ci.com/simetenn/uncertainpy.svg?token=aSp3vyuQyzq8iEpgpnpb&branch=master)](https://travis-ci.com/simetenn/uncertainpy)
[![codecov](https://codecov.io/gh/simetenn/uncertainpy/branch/master/graph/badge.svg?token=BFXnBcPbMA)](https://codecov.io/gh/simetenn/uncertainpy)

![img](https://github.com/simetenn/uncertainpy/blob/master/logo/logo.svg)

# A python toolbox for uncertainty quantification and sensitivity analysis

Uncertainpy is a library for performing uncertainty quantification and sensitivity
analysis of computational models.

## Installation

Uncertainpy can easily be installed using pip:

    pip install uncertainpy

or from source by cloning the Github repository:

    $ git clone https://github.com/simetenn/uncertainpy
    $ cd /path/to/uncertainpy
    $ sudo python setup.py install

### Dependencies

Uncertainpy has the following dependencies:

* `xvfbwrapper`
* `chaospy`
* `tqdm`
* `h5py`
* `multiprocess`
* `numpy`
* `scipy`
* `seaborn`

Additionally Uncertainpy has a few optional dependencies for specific classes of models and for features of the models.
The following external simulators are required for specific models:

* `uncertainpy.NeuronModel`: Requires [Neuron](https://www.neuron.yale.edu/neuron/download) (with Python), a simulator for neurons.
* `uncertainpy.NestModel`: Requires [Nest](http://www.nest-simulator.org/installation) (with Python), a simulator for network of neurons.

And the following Python packages are required for specific features:

* `uncertainpy.EfelFeatures`: `efel`.
* `uncertainpy.NetworkFeatures`: `elephant`, `neo`, and `quantities`.

### Test suite

Uncertainpy comes with an extensive test suite that can be run with the `test.py` script.
For how to use test.py run:

    $ python test.py --help



## Example of Uncertainpy in use

Examples for how to use Uncertainpy can be found in the
[examples](https://github.com/simetenn/uncertainpy/tree/master/examples) folder
as well as in the [documentation]().
Here we show an example,
found in [examples/coffee_cup](https://github.com/simetenn/uncertainpy/tree/master/examples/coffee_cup),
where we examine the changes in temperature of a cooling coffee cup that
follows Newton’s law of cooling:

<!-- \frac{dT(t)}{dt} = -\kappa(T(t) - T_{env}) -->
![img](http://latex.codecogs.com/svg.latex?\frac{dT(t)}{dt}%3D-\kappa(T(t)-T_{env}))

This equation tells how the temperature ![img](http://latex.codecogs.com/svg.latex?T)
of the coffee cup changes with time ![img](http://latex.codecogs.com/svg.latex?t),
when it is in an environment with temperature
![img](http://latex.codecogs.com/svg.latex?T_{env}).
![img](http://latex.codecogs.com/svg.latex?\kappa}) is a proportionality
constant that is characteristic of the system and regulates how fast the coffee
cup radiates heat to the environment.
For simplicity we set the initial temperature to a fixed value, ![img](http://latex.codecogs.com/svg.latex?%24T_0%3D95^\circ\text{C}%24),
and let ![img](http://latex.codecogs.com/svg.latex?\kappa}) and ![img](http://latex.codecogs.com/svg.latex?T_{env}) be uncertain input parameters.

We start by importing the packages we use:

    import uncertainpy as un
    import numpy as np                   # For the time array
    import chaospy as cp                 # To create distributions
    from scipy.integrate import odeint   # To integrate our equation

To create the model we define a Python function `coffee_cup` that
takes the uncertain parameters `kappa` and `T_env` as input arguments.
Inside this function we solve our equation by integrating it using
`scipy.integrate.odeint`,
before we return the results.
The implementation of the model is:

    def coffee_cup(kappa, T_env):
        # Initial temperature and time
        time = np.linspace(0, 200, 150)
        T_0 = 95

        # The equation describing the model
        def f(T, time, kappa, T_env):
            return -kappa*(T - T_env)

        # Solving the equation by integration.
        values = odeint(f, T_0, time, args=(kappa, T_env))[:, 0]

        # Return time and model results
        return time, values

We could use this function directly in `UncertaintyQuantification`,
but we would like to have labels on the axes when plotting.
So we create a `Model` with the above run function and labels:

    # Create a model from coffee_cup function and add labels
    model = un.Model(run_function=coffee_cup,
                    labels=["Time [s]", "Temperature [C]"])

The next step is to define the uncertain parameters.
We give the uncertain parameters in the cooling coffee cup model the following
distributions:

<!-- \begin{align}
    \kappa &= \mathrm{Uniform}(0.025, 0.075), \\
    T_{env} &= \mathrm{Uniform}(15, 25).
\end{align} -->

![img](http://latex.codecogs.com/svg.latex?\begin{align*}%0D%0A\kappa%26%3D\mathrm{Uniform}(0.025%2C0.075)%2C\\\\%0D%0AT_{env}%26%3D\mathrm{Uniform}(15%2C25).%0D%0A\end{align*})


We use Chaospy to create the distributions.

    # Create the distributions
    kappa_dist = cp.Uniform(0.025, 0.075)
    T_env_dist = cp.Uniform(15, 25)

    # Define a parameter list and use it to create the Parameters
    parameter_list = [["kappa", None, kappa_dist],
                      ["T_env", None, T_env_dist]]
    parameters = un.Parameters(parameter_list)


We can now calculate the uncertainty and sensitivity using polynomial chaos
expansions with point collocation,
which is the default option of `quantify`:

    # Set up the uncertainty quantification
    uncertainty = un.UncertaintyQuantification(model=model,
                                                parameters=parameters)

    # Perform the uncertainty quantification using
    # polynomial chaos with point collocation (by default)
    uncertainty.quantify()


## Documentation

The documentation for Uncertainpy can be found [here](),
and an article on Uncertainpy can be found [here]().

## Citation

If you use Uncertainpy in you work, please cite the [Uncertainpy paper]().
