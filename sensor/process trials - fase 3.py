import numpy as np

from sklearn import svm, neighbors, tree
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix
from sklearn.neural_network import MLPClassifier


def k_fold(clf_name, clf):
    kf = KFold(n_splits=5, shuffle=True)

    acc = rec1 = rec2 = rec3 = rec4 = prec1 = prec2 = prec3 = prec4 = 0
    for train_index, test_index in kf.split(x):

        # Training phase
        x_train = x[train_index, :]
        y_train = y[train_index]
        clf.fit(x_train, y_train)

        # Test phase
        x_test = x[test_index, :]
        y_test = y[test_index]
        y_pred = clf.predict(x_test)

        # Calculate confusion matrix and model performance
        cm = confusion_matrix(y_test, y_pred)
        acc_i = (cm[0, 0] + cm[1, 1] + cm[2, 2] + cm[3, 3]) / len(y_test)
        rec1_i = cm[0, 0] / (cm[0, 0] + cm[0, 1] + cm[0, 2] + cm[0, 3])
        rec2_i = cm[1, 1] / (cm[1, 0] + cm[1, 1] + cm[1, 2] + cm[1, 3])
        rec3_i = cm[2, 2] / (cm[2, 0] + cm[2, 1] + cm[2, 2] + cm[2, 3])
        rec4_i = cm[3, 3] / (cm[3, 0] + cm[3, 1] + cm[3, 2] + cm[3, 3])
        prec1_i = cm[0, 0] / (cm[0, 0] + cm[1, 0] + cm[2, 0] + cm[3, 0])
        prec2_i = cm[1, 1] / (cm[0, 1] + cm[1, 1] + cm[2, 1] + cm[3, 1])
        prec3_i = cm[2, 2] / (cm[0, 2] + cm[1, 2] + cm[2, 2] + cm[3, 2])
        prec4_i = cm[3, 3] / (cm[0, 3] + cm[1, 3] + cm[2, 3] + cm[3, 3])

        acc += acc_i
        rec1 += rec1_i
        rec2 += rec2_i
        rec3 += rec3_i
        rec4 += rec4_i
        prec1 += prec1_i
        prec2 += prec2_i
        prec3 += prec3_i
        prec4 += prec4_i

    # acc = round(acc/5, 3)
    # rec1 = round(acc/rec1, 3)
    # rec2 = round(acc/rec2, 3)
    # rec3 = round(acc/rec3, 3)
    # rec4 = round(acc/rec4, 3)
    # prec1 = round(acc/prec1, 3)
    # prec2 = round(acc/prec2, 3)
    # prec3 = round(acc/prec3, 3)
    # prec4 = round(acc/prec4, 3)

    acc /= 5
    rec1 /= 5
    rec2 /= 5
    rec3 /= 5
    rec4 /= 5
    prec1 /= 5
    prec2 /= 5
    prec3 /= 5
    prec4 /= 5

    # print('{:<12}|{:<8}|{:<8}|{:<8}|{:<8}|{:<8}|{:<8}|{:<8}|{:<8}|{:<8}'.format(clf_name, acc, rec1, rec2, rec3, rec4, prec1, prec2, prec3, prec4))
    print('{:<12}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}'.format(clf_name, acc, rec1, rec2, rec3, rec4, prec1, prec2, prec3, prec4))


# Data processing
data_files = ['acc_data.txt', 'acc_data_1.txt', 'acc_data_2.txt']
trial_files = ['acc_trials.txt', 'acc_trials_1.txt', 'acc_trials_2.txt']

for data_file, trial_file in zip(data_files, trial_files):
    print(f'Processing data from {data_file} and {trial_file}:')
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

    # Print headers
    print('{:<12}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}|{:<20}'.format(
        'Classifier',
        'ACC',
        'REC1',
        'REC2',
        'REC3',
        'REC4',
        'PREC1',
        'PREC2',
        'PREC3',
        'PREC4'
    ))

    # SVM Linear
    clf_linear = svm.SVC(kernel='linear')
    k_fold('SVM Linear', clf_linear)

    # SVM Radial
    clf_radial = svm.SVC(kernel='rbf')
    k_fold('SVM Radical', clf_radial)

    # k-NN
    clf_knn = neighbors.KNeighborsClassifier(n_neighbors=3)
    k_fold('KNN', clf_knn)

    # Decision Tree
    clf_tree = tree.DecisionTreeClassifier()
    k_fold('Tree', clf_tree)

    # SLP
    clf_slp = MLPClassifier(hidden_layer_sizes=(10), random_state=1, max_iter=10000)
    k_fold('SLP', clf_slp)

    # MLP
    clf_mlp = MLPClassifier(hidden_layer_sizes=(10, 10), random_state=1, max_iter=10000)
    k_fold('MLP', clf_mlp)

    print()
