# -*- coding: utf-8 -*-
"""PortafolioImplementacionM2_Analisis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/A01749373/PortafolioImplementacionAnalisis/blob/main/PortafolioImplementacionM2_Analisis.ipynb

# Ariadna Jocelyn Guzmán Jiménez A01749373
# "  **Análisis y Reporte sobre el desempeño del modelo.** "



---



---

## Lectura de datos
"""

# Librerias
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

columns = ["Sample_Code_Number",
           "Clump_Thickness", 
           "Uniformity_of_cell_size",
           "Uniformity_of_cell_shape",
           "Marginal_Adhesion",
           "Single_Epithelial_Cell_Size",
           "Bare_Nuclei",
           "Bland_Chromatin",
           "Normal_Nucleoli",
           "Mitoses",
           "Class"
           ]
cancer = pd.read_csv("breast-cancer-wisconsin.data", names = columns)
cancer.head()

"""## Entendimiento de los datos"""

# Numero de filas y columnas    
cancer.shape

# Informacion del dataframe
cancer.info()

# Datos estadisticos
cancer.describe()

# Numero de tumores malignos y no malignos
# 2 -> benigno
# 4 -> maligno
cancer['Class'].value_counts()

# Visualizacion de la comparacion entre malignos y benignos
sns.set_style('whitegrid')
sns.countplot(cancer['Class'], palette='RdBu_r')
plt.title("Cantidad de tumores malignos y benignos")
plt.show()

# Tumores benignos o malignos de acuerdo a los datos de cada columna
cols = ["Clump_Thickness", 
        "Uniformity_of_cell_size",
        "Uniformity_of_cell_shape",
        "Marginal_Adhesion",
        "Single_Epithelial_Cell_Size",
        "Bare_Nuclei",
        "Bland_Chromatin",
        "Normal_Nucleoli",
        "Mitoses"]

n_rows = 3
n_cols = 3


fig, axs = plt.subplots(n_rows, n_cols, figsize=(n_cols*3.2,n_rows*3.2))

for r in range(0,n_rows):
    for c in range(0,n_cols):  
        i = r*n_cols+ c     
        ax = axs[r][c]
        sns.countplot(cancer[cols[i]], hue = cancer["Class"], ax = ax, palette='RdBu_r')
        ax.set_title(cols[i])
        ax.legend(title="Class", loc='upper right') 
        
plt.tight_layout()

"""##  Tratamiento de datos"""

# Checar la existencia de datos nulos
cancer.isna().sum()

'''
La base de datos, contaba con un valor "?" en la columna Bare Nuclei,  el cual se utilizaba para indicar un valor no disponible.
Por tanto, es considerado como un valor nulo, solo que representado como un string que por consiguente, tomaba a todos los valores
de la columna como este tipo de dato. 
Para ello, comprobamos la existencia de este valor en el dataset y eliminamos las filas que lo contuvieran. Así, pasaríamos todos 
nuestros datos a números enteros.
'''

'?'	in cancer.Bare_Nuclei.values

cancer = cancer.loc[cancer["Bare_Nuclei"] != '?', :]
cancer.head()

convert_dict = {'Bare_Nuclei': int} 
  
cancer = cancer.astype(convert_dict)

# Verificacion de el tipo de datos de cada columna
cancer.info()

# Eliminacion de la columna ID, ya que no nos servirá los datos de prediccion
cancer = cancer.drop(["Sample_Code_Number"], axis = 1)
cancer.head()

"""## Implementación del algoritmo "Random Forest Classifier"
"""

# Dividir los datos en variables x, y
x = cancer.iloc[:, 0:8]
y = cancer.iloc[:, 9].values

# Dividir el dataset 
from sklearn.model_selection import train_test_split

# Modelo prueba 20% y entrenamiento 60% y validación 20%
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)
x_train2, x_val, y_train2, y_val = train_test_split(x_train, y_train, test_size=0.2, random_state=0) 
x_inf = x_test

# Escalamiento de los datos
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)
x_val = scaler.transform(x_val)

# Aplicacion de Random Forest
from sklearn.ensemble import RandomForestClassifier

for i in range (0, 12, 2):
  if (i > 0):
    forest = RandomForestClassifier(n_estimators = i, criterion = 'entropy', random_state = 0)
    model = forest.fit(x_train, y_train)
    print('Random Forest Classifier Training Accuracy with {} estimators: {}'.format(i, forest.score(x_train, y_train)))
    print('Random Forest Classifier Test Accuracy with {} estimators: {}'.format(i, forest.score(x_test, y_test)))
    print('Random Forest Classifier Validation Accuracy with {} estimators: {} \n'.format(i, forest.score(x_val, y_val)))

"""## Comparación del mejor y peor modelo"""

forest2 = RandomForestClassifier(n_estimators = 2, criterion = 'entropy', random_state = 0)
model2 = forest2.fit(x_train, y_train)

forest10 = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
model10 = forest10.fit(x_train, y_train)

print('Best vs worst train accuracy: {}'.format(forest10.score(x_train, y_train) - forest2.score(x_train, y_train)))
print('Best vs worst test accuracy: {}'.format(forest10.score(x_test, y_test) - forest2.score(x_test, y_test)))
print('Best vs worst validate accuracy: {}'.format(forest10.score(x_val, y_val) - forest2.score(x_val, y_val)))

# Dado lo anterior, nos damos que a mayores estimadores, mayor precisión en la precisión del modelo, por lo que utilizaremos en esta ocasión 10 estimadores
forest = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
model = forest.fit(x_train, y_train)
# Muestra de las características importantes de la implementación
print("Random Forest Classifier Feature importances:", model.feature_importances_)

# Visualizacion de importancias
plt.barh(x.columns.values, model.feature_importances_, color = ["#C7CEEA", "#FFDAC1", "#FF9AA2", "#E0FEFE", "#FFFFD8", "#B5EAD7"])
plt.title("Importancias por columna")
plt.show()

# Parametros e informacion de la implementacion del modelo
print("Random Forest Classifier Feature Params:")
forest.get_params()

# Calculo de predicciones del modelo
predictions =  model.predict(x_test)
validation = []
for i in range(len(predictions)):
  if (predictions[i] == y_test[i]):
    validation.append("✅")
  else:
    validation.append("❌")

print("=" * 20, "Predicciones con 10 estimadores", "=" * 20, "\n")
print("Predicciones: ", predictions)
print("Valores estimados: ", y_test)



print("=" * 70)
print("Tabla de comparación")
print("=" * 70)
df = pd.DataFrame(x_inf)
df["Prediction"] = predictions
df["Estimated"] = y_test
df["Validate"] = validation
df

# Matriz de confusion
from sklearn.metrics import confusion_matrix
sns.set()
f,ax=plt.subplots()
matrix = confusion_matrix(y_test, predictions)
print(matrix, "\n")

colormap = sns.color_palette("pastel")
sns.heatmap(matrix, annot = True, ax = ax, cbar = False, cmap = colormap) 
ax.set_title('Matriz de confusión')
ax.set_xlabel('Predicciones')
ax.set_ylabel('Estimados') 
plt.show()

from mlxtend.plotting import plot_learning_curves
plot_learning_curves(x_train, y_train, x_test, y_test, forest)
plt.title("Train vs Test")
plt.ylim(-0.2, 0.2)
plt.legend(["Training set", "Test set"])
plt.xlabel("Train and Test")
plt.ylabel("Error")
plt.show()

plot_learning_curves(x_train, y_train, x_val, y_val, forest)
plt.ylim(-0.2, 0.2)
plt.title("Train vs validation")
plt.legend(["Training set", "Validation set"])
plt.xlabel("Train and Validation")
plt.ylabel("Error")
plt.show()

"""## Errores medios 
*Diferencia entre los valores estimados y los predecidos.*
"""

from sklearn import metrics
print("Error absoluto medio:", metrics.mean_absolute_error(y_test, predictions))
print("Error cuadrático medio: ", metrics.mean_squared_error(y_test, predictions))