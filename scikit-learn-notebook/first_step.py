from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.datasets import load_iris, make_regression, fetch_california_housing
from sklearn.model_selection import train_test_split, cross_validate, RandomizedSearchCV
from sklearn.metrics import accuracy_score
from scipy.stats import randint

rfc = RandomForestClassifier(random_state=0)            # estimator: tahminci
X = [[1, 2, 3], [11, 12, 13]]
y = [0, 1]
print(rfc.fit(X, y))

print(rfc.predict(X))

print(rfc.predict([[4, 5, 6], [14, 15, 16]]))

z = [[-3, 5], [1, -10]]
stanScalar = StandardScaler().fit(z).transform(z)
print(stanScalar)
print(type(stanScalar))

# Pipelines: chaining pre-processors and estimators

# creating a pipeline object
pipe = make_pipeline(StandardScaler(),
                     LogisticRegression(random_state=0))

# loading iris dataset and split them into trains and tests
iris_X, iris_y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(iris_X, iris_y, random_state=0)

pipe.fit(X_train, y_train)
print(accuracy_score(pipe.predict(X_test), y_test))

# Model Evaluation

X, y = make_regression(n_samples=1000, random_state=0)
lr = LinearRegression()

# 5-fold by default
result = cross_validate(lr, X, y)
print(result)
print(result['test_score'])

# Automatic parameter searches
X_california, y_california = fetch_california_housing(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X_california, y_california, random_state=0)

param_distributions = {'n_estimators': randint(1, 5),
                       'max_depth': randint(5, 10)}

search = RandomizedSearchCV(estimator=RandomForestRegressor(random_state=0),
                            n_iter=5,
                            param_distributions=param_distributions,
                            random_state=0)

print(search.fit(X_train, y_train))
print(search.best_params_)

print(search.score(X_test, y_test))

