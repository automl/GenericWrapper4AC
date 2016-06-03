import sys

from sklearn.linear_model import SGDClassifier
from sklearn.datasets import load_iris
from sklearn import cross_validation

iris = load_iris()

X_train, X_test, y_train, y_test = cross_validation.train_test_split(iris.data, iris.target, test_size=0.4, random_state=0)

sgd = SGDClassifier()

params = iter(sys.argv[1:])

while True:
    try:
        name = next(params)
    except StopIteration:
        break
    value = next(params)
    
    if name == "random_state":
        sgd.random_state = int(value)
        
    elif name == "loss":
        sgd.loss = str(value)
        
    elif name == "penalty":
        sgd.penalty = str(value)
        
    elif name == "alpha":
        sgd.alpha = float(value)
        
    elif name == "learning_rate":
        sgd.learning_rate = str(value)
        
    elif name == "eta0":
        sgd.eta0 = float(value)
        
sgd.fit(X_train,y_train)

print(sgd.score(X_test, y_test))


