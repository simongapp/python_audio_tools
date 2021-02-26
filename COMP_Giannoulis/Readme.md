# COMP_Giannoulis
Python implementation of a digital dynamic range compressor based on [Giannoulis](https://www.aes.org/e-lib/browse.cfm?elib=16354).

## Usage
Requires numpy

```python
import numpy as np
import comp_giannoulis as comp

t = np.linspace(0,sig_len,int(fs)*sig_len)
test_signal = np.sin(2*np.pi*400*t)

# Uses the log-detector configuration
signal1 = comp.log_det(input=test_signal, attack=20e-3, release=100e-3, threshold=-5, 
                       ratio=5,  knee_width=20, makeup_gain=0)

# Uses the return to zero detector configuration, functionality not validated
signal2 = comp.rtz(input=test_signal, attack=20e-3, release=100e-3, threshold=-5, 
                   ratio=5,  knee_width=20, makeup_gain=0)

# Uses the return to threshold dector configuration, functionality not validated
signal3 = comp.rtt(input=test_signal, attack=20e-3, release=100e-3, threshold=-5, 
                    ratio=5,  knee_width=20, makeup_gain=0)
```
Check comp_giannoulis.py for optional parameters and access to the single modules.

## Known issues
The authors propose three compressor configurations.  
I only validated the configuration where the detector operates in the logarithmic domain. The other two configurations were added for the sake of completeness.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
