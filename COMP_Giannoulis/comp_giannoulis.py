import numpy as np

def gain_computer(data, threshold, ratio, knee_width=0):
    # Parameters
    # data: input data
    # threshold: level above which compression starts in dB
    # ratio: input/output ratio for signals overshooting the threshold, determines the amount of compression applied
    # knee_width: smoothing the transition from uncompressed to compressed, default: 0

    y_G = np.zeros(data.shape)

    # Sanity checks
    if (knee_width < 0):
        knee_width = 0
        # print("Error! Knee width not positive.")
        # return
    if (ratio < 0):
        ratio = 1
        # print("Error! Ratio not positive.")
        # return

    # Change knee width of 0 to a really small value since eq.4 requires to divide by it
    if (knee_width == 0):
        knee_width = 1e-5
    # Compression characteristics with soft knee, eq. 4
    for i in range(len(data)):
        if ((2 * (data[i] - threshold)) < (-knee_width)):
            y_G[i] = data[i]
        elif ((2 * np.abs(data[i] - threshold)) <= knee_width):
            y_G[i] = (data[i] + (1 / ratio - 1) * (data[i] - threshold + knee_width / 2) ** 2 / (2 * knee_width))
        else:
            y_G[i] = (threshold + (data[i] - threshold) / ratio)
    return y_G


def c_abs(data):
# Returns the absolute value of the input
    return np.abs(data)


def level_detector(data, attack, release, fs=48e3):
    # Parameters
    # data: input
    # attack: Attack time of the compressor in s
    # release: Release time of the compressor in s
    # fs: Sample rate of the system in Hz, default: 48kHz
    y_L = np.zeros(data.shape)
    # Eq. 7
    if (attack == 0):
        attack = 1e-3
    if (release == 0):
        release = 1e-3
    alpha_attack = np.exp(-1 / (attack * fs))
    alpha_release = np.exp(-1 / (release * fs))

    # Level corrected peak detector, Eq. 15
    for i in range(len(data)):
        if (data[i] > y_L[i - 1]):
            y_L[i] = alpha_attack * y_L[i - 1] + (1 - alpha_attack) * data[i]
        else:
            y_L[i] = alpha_release * y_L[i - 1]
    return y_L


def calc_dB(data):
# Returns dB values of a linearized input
    for i in range(len(data)):
        if (data[i] == 0):
            data[i] = 1e-12
    return 20 * np.log10(data)


def linearize(data):
# Returns linearized values of a dB input
    return 10 ** (data / 20)


def rtz(input, attack, release, threshold, ratio, makeup_gain = 0, knee_width = 0, fs = 48e3):
    # Compressor configuration according to Fig.7, a)
    # Return to zero detector
    abs_out_rtz = c_abs(input)
    level_detector_out_rtz = level_detector(data=abs_out_rtz, attack=attack, release=release, fs=fs)
    dB_out_rtz = calc_dB(level_detector_out_rtz)
    gain_computer_out_rtz = gain_computer(data=dB_out_rtz, threshold=threshold, ratio=ratio, knee_width=knee_width)
    makeup_gain_out_rtz = dB_out_rtz - gain_computer_out_rtz + makeup_gain
    control_sig_rtz = linearize(makeup_gain_out_rtz)

    output_rtz = input * control_sig_rtz

    return output_rtz


def rtt(input, attack, release, threshold, ratio, makeup_gain = 0, knee_width = 0, fs = 48e3):
    # Compressor configuration according to Fig.7, b)
    # Return to threshold detector
    abs_out_rtt = c_abs(input) - threshold
    level_detector_out_rtt = level_detector(data=input, attack=attack, release=release, fs=fs) + threshold
    dB_out_rtt = calc_dB(data=level_detector_out_rtt)
    gain_computer_out_rtt = gain_computer(data=dB_out_rtt, threshold=threshold, ratio=ratio, knee_width=knee_width)
    makeup_gain_out_rtt = dB_out_rtt - gain_computer_out_rtt + makeup_gain
    control_sig_rtt = linearize(makeup_gain_out_rtt)

    output_rtt = input * control_sig_rtt

    return output_rtt


def log_det(input, attack, release, threshold, ratio, makeup_gain = 0, knee_width = 0, fs = 48e3):
    # Compressor configuration according to Fig.7, c)
    # Return to threshold detector
    abs_out_log = c_abs(input)
    dB_out_log = calc_dB(data=abs_out_log)
    gain_computer_out_log = dB_out_log - gain_computer(data=dB_out_log, threshold=threshold, ratio=ratio, knee_width=knee_width)
    level_detector_out_log = level_detector(data=gain_computer_out_log, attack=attack, release=release)
    makeup_gain_out_log = makeup_gain - level_detector_out_log
    control_sig_log = linearize(data=makeup_gain_out_log)
    output_log = input * control_sig_log

    return output_log
