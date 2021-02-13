import numpy as np

def first_order(freq, fs=48e3, filter="hpf", band_limit=True):
### Parameters
# freq: Center frequency in Hz
# fs: Sampling rate in Hz, default: 48kHz
# filter: High pass or low pass filter, default: high pass
# band_limit: Limits the bandwidth of the filter in the range of 0.1Hz to fs/2, default: True

    # Fixed values, can be changed if desired
    Q_fac = 5
    gain = -20

    # Sanity checks
    if(fs==0):
        print("Error! fs needs to be greater than 0")
        return
    if(freq==0 or freq>fs/2):
        print("Error! Center frequency ot of range 0.1 to fs/2")
        return

    # Calculate 3dB point left from center frequency
    # Source: http://www.sengpielaudio.com/calculator-cutoffFrequencies.htm
    if(filter=="lpf"):
        f1 = freq*(np.sqrt(1.0+1.0/(4.0*Q_fac**2.0))-1.0/(2.0*Q_fac))
    elif(filter=="hpf"):
        f1 = freq*(np.sqrt(1.0+1.0/(4.0*Q_fac**2.0))+1.0/(2.0*Q_fac))
    # Limit bandwidth of the filter if desired
    if(band_limit):
        if(f1<0.1):
            f1 = 0.1
        if(f1>fs/2):
            f1 = fs/2

    # Convert to rad
    freq = 2*np.pi*freq
    f1 = 2*np.pi*f1

    # Calculate factor, Equation 8
    a = (np.tan(f1/2.0/fs)-1.0)/(np.tan(f1/2.0/fs)+1.0)
    K = (10.0**(gain/20.0))

    # Vector for z
    f = np.logspace(0.1,np.log10(fs/2),int(fs/2))
    z = np.exp(1j * 2*np.pi * f/fs)
    # Equation 7
    A = (z**(-1)+a)/(1.0+a*z**(-1))
    # Equation 6
    if(filter=="lpf"):
        H_first_order = (1/2)*(1.0+A)+(1/2)*K*(1.0-A)
    elif(filter=="hpf"):
        H_first_order = (1/2)*(1.0-A)+(1/2)*K*(1.0+A)

    return f, H_first_order

def second_order(freq, gain, Q_fac=5, fs=48e3, band_limit=True):
### Parameters
# freq: Center frequency in Hz
# gain: Gain at center frequency in dB
# Q_fac: Q-Factor, default: 5
# fs: Sampling rate in Hz, default: 48kHz
# band_limit: Limits the bandwidth of the filter in the range of 0.1Hz to fs/2, default: True

    # Sanity checks
    if(fs==0):
        print("Error! fs needs to be greater than 0")
        return
    if(Q_fac==0):
        print("Error! Q factor needs to be greater than 0")
        return
    if(freq==0 or freq>fs/2):
        print("Error! Center frequency ot of range 0.1 to fs/2")
        return
    # Calculate 3dB points left and right from center frequency
    # Source: http://www.sengpielaudio.com/calculator-cutoffFrequencies.htm
    f1 = freq*(np.sqrt(1.0+1.0/(4.0*Q_fac**2))-1.0/(2.0*Q_fac))
    f2 = freq*(np.sqrt(1.0+1.0/(4.0*Q_fac**2))+1.0/(2.0*Q_fac))
    # Limit bandwidth of the filter if desired
    if(band_limit):
        if(f1<0.1):
            f1 = 0.1
        if(f2>fs/2.0):
            f2 = fs/2.0

    band = f2-f1

    # Convert to rad
    freq = 2*np.pi*freq
    band = 2*np.pi*band

    # Calculate factors, Equation 11a) ff
    a = (1.0-np.tan(band/2.0/fs))/(1.0+np.tan(band/2.0/fs))
    b = -np.cos(freq/fs)
    K = (10.0**(gain/20.0))

    # Vector for z
    f = np.logspace(np.log10(1),np.log10(fs/2),int(fs/2))
    z = np.exp(1j * 2.0*np.pi * f/fs)
    # Equation 10
    A = (z**(-2)+b*(1.0+a)*z**(-1)+a)/(1.0+b*(1.0+a)*z**(-1)+a*z**(-2))
    # Equation 6
    H_second_order = (1/2)*(1.0+A)+(1/2)*K*(1.0-A)

    return f, H_second_order

