import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os

clear = lambda: os.system('cls')
clear()

print("Directorio de trabajo actual:", os.getcwd())
# Cargar el dataset
dataset = pd.read_csv("Prácticas/Jobs.csv")

# Función para extraer el valor medio de experiencia
def extract_experience(exp_str):
    if pd.isna(exp_str):
        return None
    try:
        exp_str = exp_str.replace("years", "").strip()
        min_exp, max_exp = exp_str.split("-")
        return (float(min_exp) + float(max_exp)) / 2
    except:
        return None

# Aplicar extracción
dataset["Experience_Years"] = dataset["experience"].apply(extract_experience)

# Limpiar y convertir salario
def extract_salary(salary_str):
    if pd.isna(salary_str):
        return None
    try:
        salary_str = salary_str.replace("₹", "").replace("LPA", "").strip()
        min_salary, max_salary = salary_str.split(" - ")
        return (float(min_salary) + float(max_salary)) / 2
    except:
        return None

dataset["Avg_Salary"] = dataset["salary"].apply(extract_salary)

# Eliminar nulos
dataset = dataset.dropna(subset=["Experience_Years", "Avg_Salary"])

# Ordenar como si fuera una serie temporal por años de experiencia
dataset = dataset.sort_values(by="Experience_Years")

# Preparar variables
X = dataset[["Experience_Years"]]
y = dataset["Avg_Salary"]

# Modelo de regresión lineal
model = LinearRegression()
model.fit(X, y)

# Predecir valores
y_pred = model.predict(X)

# Mostrar resultados
plt.figure(figsize=(10, 6))
plt.scatter(X, y, color="blue", alpha=0.6, label="Salario Real")
plt.plot(X, y_pred, color="red", linewidth=2, label="Línea de Regresión")
plt.xlabel("Años de Experiencia")
plt.ylabel("Salario Promedio (LPA)")
plt.title("Regresión Lineal: Experiencia vs Salario")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Ejemplo de predicción para nuevos valores
nuevos_valores = pd.DataFrame({"Experience_Years": [1.5, 3, 5, 7, 10]})
predicciones = model.predict(nuevos_valores)

for exp, pred in zip(nuevos_valores["Experience_Years"], predicciones):
    print(f"Para {exp} años de experiencia, el salario predicho es {pred:.2f} LPA")
