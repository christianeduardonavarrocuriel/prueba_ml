import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import joblib
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# scikit-learn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 1. Cargar y describir el Dataset

df = pd.read_csv("ice-cream.csv")

print("Primeras filas del Dataset")
print(df.head())

print("Resumen Estadístico")
print(df.describe())
print(df.info())

# 2. Graficar los datos para observar la distribución

plt.figure(figsize=(8, 8))
sns.histplot(df["IceCreamsSold"], kde=True, color="blue")
plt.title("Distribución de Helados Vendidos")
plt.xlabel("Helados Vendidos")
plt.ylabel("Número de días")
leyenda = [
    Patch(facecolor="blue", alpha=0.5, edgecolor="black",
          label="Barras: días por rango de ventas"),
    Line2D([0], [0], color="blue", linewidth=2,
           label="Línea: comportamiento general de las ventas"),
]
plt.legend(handles=leyenda, loc="upper left", frameon=True)
plt.grid(True)
plt.savefig("grafica_helados.png")

plt.figure(figsize=(8, 8))
sns.scatterplot(data=df, x="Temperature", y="IceCreamsSold", color="green", alpha=0.7)
plt.title("Relación entre temperatura y helados vendidos")
plt.xlabel("Temperatura")
plt.ylabel("Helados Vendidos")
plt.grid(True)
plt.savefig("temperatura_helados.png")

# 3. Seleccionar las características

X = df[["Temperature", "Rainfall"]]
y = df["IceCreamsSold"]

# 4. Dividir los datos en Train y Test

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=123
)

print("Datos de entrenamiento")
print(f"Datos totales: {len(X)}")
print(f"Datos de entrenamiento: {len(X_train)}")
print(f"Datos de prueba: {len(X_test)}")

print("Primeros 5 datos de entrenamiento:")
print(X_train.head())
print("Primeros 5 datos de prueba:")
print(X_test.head())

# 5. Entrenamiento del modelo

modelo = LinearRegression()
modelo.fit(X_train, y_train)

print("Coeficientes:")
print(f"Temperature: {modelo.coef_[0]:.2f}")
print(f"Rainfall: {modelo.coef_[1]:.2f}")
print(f"Intersección: {modelo.intercept_:.2f}")

# 6. Realizar predicciones

y_pred = modelo.predict(X_test)

comparativa = pd.DataFrame({
    "Real": y_test,
    "Predicho": y_pred
})

print("Comparación de resultados")
print(comparativa.head())

# 7. Evaluación del modelo

mse = mean_squared_error(y_test, y_pred)
rmse = math.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"Error cuadrático medio (MSE): {mse:.2f}")
print(f"Raíz del error cuadrático medio (RMSE): {rmse:.2f}")
print(f"Coeficiente de determinación (R2): {r2:.2f}")

# 8. Visualizar los resultados

plt.figure(figsize=(8, 8))
plt.scatter(y_test, y_pred, color="red", label="Datos Reales", alpha=0.7)

limites = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
plt.plot(limites, limites, color="green", linewidth=2, label="Predicción perfecta")

plt.title("Regresión Lineal: Resultados Reales y Predichos")
plt.xlabel("Helados Vendidos Reales")
plt.ylabel("Helados Vendidos Predichos")
plt.legend()
plt.grid(True)
plt.savefig("predicciones_helados.png")

# 9. Exportar el modelo

nombre_modelo = "modelo_helados.pkl"
joblib.dump(modelo, nombre_modelo)

# 10. Cargar el modelo y hacer predicciones

modelo_cargado = joblib.load(nombre_modelo)

nuevos_datos = pd.DataFrame({
    "Temperature": [75.0, 60.0],
    "Rainfall": [0.10, 0.50]
})

nuevas_predicciones = modelo_cargado.predict(nuevos_datos)

print("Nuevas predicciones")
print(nuevos_datos)
print(nuevas_predicciones)
