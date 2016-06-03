import sys

from sklearn.linear_model import SGDClassifier
from sklearn.datasets import load_iris
from sklearn import cross_validation

iris = load_iris()

X_train, X_test, y_train, y_test = cross_validation.train_test_split(iris.data, iris.target, test_size=0.4, random_state=0)

params = iter(sys.argv[2:])

while True:
    try:
        name = next(params)
    except StopIteration:
        break
    value = next(params)
    
    if name == "random_state":
        random_state = int(value)+1
        
    elif name == "loss":
        loss = str(value)
        
    elif name == "penalty":
        penalty = str(value)
        
    elif name == "alpha":
        alpha = float(value)
        
    elif name == "learning_rate":
        learning_rate = str(value)
        
    elif name == "eta0":
        eta0 = float(value)
    
sgd = SGDClassifier(random_state=random_state,
                    loss=loss,
                    penalty=penalty,
                    alpha=alpha,
                    learning_rate=learning_rate,
                    eta0=eta0)    
    
#print(sgd.loss, sgd.penalty, sgd.alpha, sgd.learning_rate, sgd.eta0)
        
sgd.fit(X_train,y_train)

if sys.argv[1] == "train":
    print(-1 * sgd.score(X_train, y_train))
else:
    print(-1 * sgd.score(X_test, y_test))


