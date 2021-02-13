# Eq_Regalia

Python implementation of a tuneable IIR filter based on [Regalia](https://ieeexplore.ieee.org/document/1165037).  
First order implementation allows to set a variable frequency in either HPF or LPF mode.  
Second order implementation allows to set a variable frequency, gain and Q-factor as a notch filter.

## Usage
Requires numpy
```python
import numpy as np
import eq_regalia as eq

# Creates the x and y values for the transfer function in the z-domain for a first order HPF
x,y = eq.first_order(freq=100)
# Creates the x and y values for the transfer function in the z-domain for a first order LPF
x,y = eq.first_order(freq=100, filter="lpf")

# # Creates the x and y values for the transfer function in the z-domain for a second order filter
x,y = eq.second_order(freq=800, gain=6, Q_fac=3)
```
Check the eq_regalia.py for optional parameters

## Known issues
The second order filter results in different filter widths for negative gains compared to positive gains.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
