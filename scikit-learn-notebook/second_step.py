from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

x, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=0)

clf = SVC()
clf.fit(X_train, y_train)
print(X_test[:10])                      # feature of test
print(y_test[:10])                      # class of test
predicted_clf = clf.predict(X_test)
print(predicted_clf[:10])               # class of predict

# reporting
print(classification_report(y_test, predicted_clf))
print(confusion_matrix(y_test, predicted_clf))

