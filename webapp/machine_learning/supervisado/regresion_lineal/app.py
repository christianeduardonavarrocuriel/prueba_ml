import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math 
import joblib

#scikit-learn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 1. Cargar y describir el Dataset

df = pd.read_csv("casas.csv")

print("Resumen Estadístico")
print(df.describe())
print(df.info())

# 2. Graficar los datos para observar la distribución

plt.figure(figsize=(8,8))
sns.scatterplot(data=df, x="metros_cuadrados", y="precio",color="green", alpha=0.7)
plt.title("Relación entre metros cuadrados y precio")
plt.xlabel("Metros Cuadrados")
plt.ylabel("Precio Millones de Pesos")
plt.grid(True)
plt.savefig("grafica.png")


# 3. Seleccionar las caracteristicas
X = df[["metros_cuadrados"]]
y = df["precio"]


# 4. Dividir los datos en Train y Test

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=123)

print("Datos de entrenamiento")
print(f"Datos totales: {len(X)}") # 100
print(F"Datos de entrenamiento: {len(X_train)}") # 80%
print(f"Datos de prueba: {len(X_test)}") # 20%

print(f"Primeros 5 datos de entrenamiento: {X_train.head()}")
print(f"Primeros 5 datos de prueba: {X_test.head()}")

# 5. Entrenamiento del modelo

modelo = LinearRegression()

modelo.fit(X_train, y_train)

print(f"Pendiente {modelo.coef_[0]:.2f}")
print(f"Intersección {modelo.intercept_:.2f}")

# 6. Realizar predicciones

y_pred = modelo.predict(X_test)

comparativa = pd.DataFrame({"Real": y_test, "Predicho": y_pred})

print(comparativa.head())

# 7. Evaluación del model

mse = mean_squared_error(y_test, y_pred)
rmse = math.sqrt(mse)

r2 = r2_score(y_test, y_pred)

print(f"Error cuadrático medio (MSE): {mse:.2f}") 
print(f"Raíz del error cuadrático medio (RMSE): {rmse:.2f}")
print(f"Coeficiente de determinación (R2): {r2:.2f}")

# 8. Visualizar los resultados

plt.figure(figsize=(8,8))
plt.scatter(X_test,y_test, color="red", label="Datos Reales (test)",alpha=0.7)
plt.plot(X_test, y_pred, color="green", linewidth=2, label="Línea de regresión")

plt.title("Regresión Lineal: Predicción de Precios")
plt.xlabel("Metros Cuadrados")
plt.ylabel("Precio en Millones de Pesos")
plt.legend()
plt.grid(True)
plt.savefig("predicciones.png")

# 9. Exportar el modelo

nombre_modelo = "precios_casas.pkl"
joblib.dump(modelo, nombre_modelo)

# 10. Cargar y usar el modelo

modelo_cargado = joblib.load(nombre_modelo)

# 175 - 2,650M
# 150 - 2,275M
nuevas_casas = pd.DataFrame(
    {
        "metros_cuadrados":[175,150]
    }
)

nuevos_precios = modelo_cargado.predict(nuevas_casas)

print(nuevos_precios)