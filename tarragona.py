# -*- coding: utf-8 -*-
"""Tarragona.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1asgnWspZRIw1jw1sCQC9oaKAIfn-Ae__

#Tarragona

Import data from PI System Explorer to an Excel (problems reading data once we import the document to Google Colab since it gets it as a string, needed to copy/paste to another sheet)
"""

import pandas as pd
from pandas import read_csv

#data = pd.read_excel (r'/content/Datos de Carga Base Tarragona (borrador inicial).xlsx', sheet_name='Hoja1')

data = pd.read_excel (r'/content/Prediccion Carga.Variables Entrada.xlsx', sheet_name='Hoja2')

"""Aqui lo que he hecho es importar la libreria pandas y la voy a utilizar llamandola "pd" por lo que cada vez que salga "pd." estoy llamando a una funcion dentro de esa libreria

Para leer un documento en excel utilizamos esa funcion. Declaramos data y le decimos que lea el documento con nombre X y la hoja numero Y

Es necesario dropear datos?
"""

data['Temp'] = data['Temp'][data['Temp'].between(data['Temp'].quantile(.15), data['Temp'].quantile(.85))]
data['Pneta'] = data['Pneta'][data['Pneta'].between(data['Pneta'].quantile(.15), data['Pneta'].quantile(.85))]
data = data.dropna()

Esto es para coger datos mas especificos. En la hoja de excel ya tengo puesto nombres por lo que ya puedo llamar a cada columna como si fuera una lista

"""Dividimos el dataset en training y testing para entrenar al modelo"""

from sklearn.model_selection import train_test_split, RandomizedSearchCV
# Split-out validation dataset
array = data.values

#Hoja2
X = array[:,0:6]
y = array[:,6]

#Hoja3
#X = array[:,0:1]
#y = array[:,1]

# random_state=0 for reproducibility purposes
# We get 75% for training set
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.25, random_state=10)

"""Utilizamos otra libreria y colocamos los datos, le decimos que las primeras 6 columnas son datos y la 6 es el resultado
Dividimos los datos para entrenar y testear

Mostramos el aspecto del dataset y lo graficamos para ver la tendencia y si hay algún outlier si no hemos hecho la limpia todavía
"""

import matplotlib.pyplot as plt

print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)
print(data.head())

#PLOTTING TREND

plt.figure(figsize=(30,10))
plt.scatter(data['Temp'], data['Pneta'])
plt.scatter(data['Humedad'], data['Pneta'])
plt.xlabel('Temperatura/Humedad')
plt.ylabel('PNeta')
plt.show()

"""##Differents Models Regressors

Se pueden utilizar diferentes modelos, cada modelo entrenara de una manera por lo que hay modelos mas efectivos que otros segun los datos que introduzcamos. Como veis, tenemos que importar mas librerias para poder utilizarlos. 
Clf es el modelo, lo creamos, lo entrenamos y predecimos los resultados con X_test, luego se comparan los resultados entre y_test (los resultados reales) e y_test_pred (los resultados del modelo)

**Decision Tree**
"""

import numpy as np
import math
from sklearn import metrics
from sklearn import tree
from sklearn.neighbors import KNeighborsRegressor

#DECISION TREE REGRESSOR
np.random.seed(0)
# Default hyper-parameters
clf = tree.DecisionTreeRegressor()
clf = clf.fit(X_train, y_train)

y_test_pred = clf.predict(X_test)
print("RMSE =", math.sqrt(abs(metrics.mean_squared_error(y_test, y_test_pred))))
y_train_pred = randomNeigh.predict(X_train)
print("RMSE Neighbors Tunned Train =", math.sqrt(abs(metrics.mean_squared_error(y_train, y_train_pred))))
print(y_train-y_train_pred)

"""**Decision Tree Hiper-Parameter Tunning**

**KNeighbors**
"""

from scipy.stats import uniform, expon
from scipy.stats import randint as sp_randint
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.model_selection import KFold
import time

#KNEIGHBORS REGRESSOR
np.random.seed(0)
# Default hyper-parameters
neigh = KNeighborsRegressor()
neigh = neigh.fit(X_train, y_train) 
y_test_pred = neigh.predict(X_test)
print("RMSE Neighbors Regressor =", math.sqrt(abs(metrics.mean_squared_error(y_test, y_test_pred))))
y_train_pred = randomNeigh.predict(X_train)
print("RMSE Neighbors Tunned Train =", math.sqrt(abs(metrics.mean_squared_error(y_train, y_train_pred))))

"""**KNeighbors Hiper-Parameter Tunning, Randomized Search CV**

Dentro de cada modelo hay varios parametros. Cuando no los modificas, el modelo coge parametros por defecto pero puedes modificarlos para intentar tener un resultado mas preciso. Al final os dareis cuenta que te dicen cuales son los mejores parametros, con eso podreis ir modificando el modelo
"""

#Neighbors with Hiper-tunning

# Start the timer
start = time.time()

# CV grid
cv_grid = KFold(n_splits=2, shuffle=True, random_state=0)

# Search space
param_grid = {'n_neighbors':list(range(1,11)),
             'weights':["distance", "uniform"],
             'p': [1,2]
             }

budget = 20
# random.seed = 0 for reproducibility
np.random.seed(0)
randomNeigh = RandomizedSearchCV(KNeighborsRegressor(), 
                         param_grid,
                         scoring='neg_mean_squared_error',
                         cv=cv_grid, 
                         n_jobs=1, verbose=1,
                         n_iter=budget
                        )

randomNeigh.fit(X=X_train, y=y_train)

# At this point, clf contains the model with the best hyper-parameters found by gridsearch
# and trained on the complete X_train

# Now, the performance of clf is computed on the test partition

y_test_pred = randomNeigh.predict(X_test)

# End the timer
end = time.time()

print('\n Elapsed time (s): {}.'.format(end - start))

print("RMSE Neighbors Tunned Test =", math.sqrt(abs(metrics.mean_squared_error(y_test, y_test_pred))))

y_train_pred = randomNeigh.predict(X_train)
print("RMSE Neighbors Tunned Train =", math.sqrt(abs(metrics.mean_squared_error(y_train, y_train_pred))))

print("Best parameters :", randomNeigh.best_params_)

for i in range(20):
  print(y_test[i])
  print(y_test_pred[i])
  print('\n')
#PLOTTING RESULTS
#Comparing y_test with Kneighbors prediction and Iberdrola prediction
plt.figure(figsize=(30,10))
plt.plot(y_test, color = "red")
plt.plot(y_test_pred, color = "green")
plt.show()

"""**Random Forrest**"""

from sklearn.ensemble import RandomForestRegressor

#Random Forest
random = RandomForestRegressor()
random = random.fit(X_train, y_train) 
y_test_pred = random.predict(X_test)
y_train_pred = random.predict(X_train)
print("RMSE Random Forest =", math.sqrt(abs(metrics.mean_squared_error(y_test, y_test_pred))))
print("RMSE Random Forest =", math.sqrt(abs(metrics.mean_squared_error(y_train, y_train_pred))))
print(y_train-y_train_pred)

"""**Random Forrest Hiper-Parameter Tunning Grid Search CV**"""

#Random Forest Tunned
# Start the timer
start = time.time()

param_grid = [
{'n_estimators': [3, 10, 30]},
{'bootstrap': [False], 'n_estimators': [3, 10]},
]
random = RandomForestRegressor()
gridRandom = GridSearchCV(random, param_grid, cv=5,
scoring='neg_mean_squared_error')
gridRandom.fit(X_train, y_train)

# End the timer
end = time.time()

print('\n Elapsed time (s): {}.'.format(end - start))

print("RMSE Random Forest Tunned =", math.sqrt(abs(metrics.mean_squared_error(y_test, y_test_pred))))

print("Best parameters :", gridRandom.best_params_)


#final_model = tunNeigh.best_estimator_

#Plot two different points
fig, ax = plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(30)
plt.title("Pred Vs Test", fontsize=24)
plt.scatter(y_test,y_test_pred)

plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
plt.xlabel('Test')
plt.ylabel('Pred')
plt.show()

for i in range(20):
  print(y_test[i])
  print(y_test_pred[i])
  print('\n')