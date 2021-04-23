import numpy as np

from scipy import stats
from scipy import signal
import matplotlib.pyplot as plt

data = np.loadtxt('acc_data.txt')
data_stats = np.loadtxt('acc_trials.txt', dtype='int')

fs = 50
window_size = int(fs * 0.5)
n_signals = data.shape[1]

trials = {}

for step in data_stats:
    for index in range(step[1], step[2], window_size):
        print('Step: ', step[0], ' - ', 'Lower lim: ', index, ' - ', 'Upper lim: ', index + window_size - 1)

        if not step[0] in trials:
            trials[step[0]] = []

        trials[step[0]].append([index, index + window_size - 1])

mean_values = {}

for mov in trials:
    print('Movement: ', mov)
    mean_values[mov] = []

    for win in trials[mov]:
        print('\tWindow: ', win)

        mean_v = []
        for s in range(n_signals):
            sig = data[win[0]:win[1] + 1, s]
            mean_v.append(np.average(sig))

        mean_values[mov].append(mean_v)

mean_mean_values = []
moves = []

for mov in mean_values:
    print('Movement: ', mov)
    moves.append(str(mov))
    values = np.array(mean_values[mov])
    mean_mean_values.append(values.mean(0))

print(mean_mean_values)

fig, axs = plt.subplot(1, n_signals)

for s in range(n_signals):
    vals = [row[s] for row in mean_mean_values]
    axs[s].bar(moves, vals)
    axs[s].set_title('Signal: ' + str(s + 1))

fig.suptitle('Average values')

plt.show()