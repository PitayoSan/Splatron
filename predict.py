import numpy as np

from sklearn import svm, neighbors, tree
from sklearn.model_selection import KFold
import pickle


# Data processing
data_file = './sensor/acc_data.txt'
trial_file = './sensor/acc_trials.txt'

x = np.array([])
y = np.array([])
with open(data_file, 'r') as data_cm, open(trial_file, 'r') as trials_cm:
    data = data_cm.readlines()
    trials = trials_cm.readlines()
    for trial in trials:
        line = trial.split()
        category = int(line[0])
        current_line = int(line[1]) - 1
        upper_limit = int(line[2])
        while current_line < upper_limit:
            y = np.append(y, category)
            x = np.append(x, [float(x) for x in data[current_line].split()])
            current_line += 1
    x = x.reshape(y.size, 3)

predict = []
for i in range(3):
    predict.append(i + 1.)

# k-NN
clf = neighbors.KNeighborsClassifier(n_neighbors=3)
kf = KFold(n_splits=5, shuffle=True)
for train_index, test_index in kf.split(x):
    # Training phase
    x_train = x[train_index, :]
    y_train = y[train_index]
    clf.fit(x_train, y_train)

    # Test phase
    x_test = x[test_index, :]
    y_test = y[test_index]

with open('pickled_clf', 'wb') as pickled_clf:
    pickle.dump(clf, pickled_clf)

print("The classifier was trained and pickled")
