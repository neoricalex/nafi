from sklearn import svm
X = [[0,1], [2,1]]
y = [5,1]
clf = svm.SVR(kernel='poly', C=100, gamma='auto', degree=3, epsilon=.1,
               coef0=1)
clf.fit(X, y) 
print(clf.predict([[7]]))
print(clf.score(X, y, sample_weight=None))
