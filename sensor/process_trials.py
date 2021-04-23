import numpy as np

from scipy import stats
from scipy import signal
import matplotlib.pyplot as plt

data = np.loadtxt('acc_data.txt')
data_stats = np.loadtxt('acc_trials.txt', dtype='int')

fs = 15
window_size = int(fs * 0.25)
n_signals = data.shape[1]

trials = {}

for step in data_stats:
    for index in range(step[1], step[2], window_size):
        print('Step: ', step[0], ' - ', 'Lower lim: ', index, ' - ', 'Upper lim: ', index + window_size - 1)

        if not step[0] in trials:
            trials[step[0]] = []

        trials[step[0]].append([index, index + window_size - 1])

mean_values = {}
std_values = {}
kurtosis_values = {}
skew_values = {}

for mov in trials:
    print('Movement: ', mov)
    mean_values[mov] = []
    std_values[mov] = []
    kurtosis_values[mov] = []
    skew_values[mov] = []

    for win in trials[mov]:
        print('\tWindow: ', win)

        mean_v = []
        std_v = []
        kurtosis_v = []
        skew_v = []
        for s in range(n_signals):
            sig = data[win[0]:win[1] + 1, s]
            mean_v.append(np.average(sig))
            std_v.append(np.std(sig))
            kurtosis_v.append(stats.kurtosis(sig))
            skew_v.append(stats.skew(sig))

        mean_values[mov].append(mean_v)
        std_values[mov].append(std_v)
        kurtosis_values[mov].append(kurtosis_v)
        skew_values[mov].append(skew_v)

mean_mean_values = []
mean_std_values = []
mean_kurtosis_values = []
mean_skew_values = []
moves = []

for mov in mean_values:
    print('Movement: ', mov)
    moves.append(str(mov))

    mevalues = np.array(mean_values[mov])
    sdvalues = np.array(std_values[mov])
    kuvalues = np.array(kurtosis_values[mov])
    skvalues = np.array(skew_values[mov])

    mean_mean_values.append(mevalues.mean(0))
    mean_std_values.append(sdvalues.mean(0))
    mean_kurtosis_values.append(kuvalues.mean(0))
    mean_skew_values.append(skvalues.mean(0))

fig, axs = plt.subplots(n_signals, 4)

for s in range(n_signals):
    vals = [row[s] for row in mean_mean_values]
    axs[s, 0].bar(moves, vals)
    axs[s, 0].set_title('Mean -S' + str(s + 1))

for s in range(n_signals):
    vals = [row[s] for row in mean_std_values]
    axs[s, 1].bar(moves, vals)
    axs[s, 1].set_title('STD - S' + str(s + 1))

for s in range(n_signals):
    vals = [row[s] for row in mean_kurtosis_values]
    axs[s, 2].bar(moves, vals)
    axs[s, 2].set_title('Kurtosis - S' + str(s + 1))

for s in range(n_signals):
    vals = [row[s] for row in mean_skew_values]
    axs[s, 3].bar(moves, vals)
    axs[s, 3].set_title('Skew - S' + str(s + 1))

fig.suptitle('Average values')

plt.show()
