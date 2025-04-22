import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Cargar el dataset
dataset = pd.read_csv("prácticas/Jobs.csv")

# Procesar la columna 'experience' para extraer el promedio de años de experiencia
def parse_experience(exp_str):
    if pd.isna(exp_str):
        return np.nan
    try:
        exp_str = exp_str.replace("years", "").strip()
        min_exp, max_exp = exp_str.split("-")
        return (float(min_exp) + float(max_exp)) / 2
    except:
        return np.nan

dataset["Avg_Experience"] = dataset["experience"].apply(parse_experience)

# Procesar la columna 'salary' para extraer el salario promedio
def extract_salary(salary_str):
    if pd.isna(salary_str):
        return np.nan
    try:
        salary_str = salary_str.replace("₹", "").replace("LPA", "").strip()
        min_salary, max_salary = salary_str.split(" - ")
        return (float(min_salary) + float(max_salary)) / 2
    except:
        return np.nan

dataset["Avg_Salary"] = dataset["salary"].apply(extract_salary)

# Eliminar filas con valores faltantes en las columnas relevantes
dataset = dataset.dropna(subset=["Avg_Salary", "Avg_Experience", "location"])


# Codificar la columna 'location' utilizando One-Hot Encoding
dataset_encoded = pd.get_dummies(dataset, columns=["location"], drop_first=True)

# Seleccionar las características para el clustering
features = ["Avg_Salary", "Avg_Experience"] + [col for col in dataset_encoded.columns if col.startswith("location_")]

# Escalar las características
scaler = StandardScaler()
X_scaled = scaler.fit_transform(dataset_encoded[features])


# Calcular la suma de los errores cuadráticos dentro del cluster (WCSS) para diferentes valores de k
wcss = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

# Graficar el método del codo
plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), wcss, marker='o')
plt.title("Método del Codo")
plt.xlabel("Número de Clusters (k)")
plt.ylabel("WCSS")
plt.grid(True)
plt.show()

# Suponiendo que el número óptimo de clusters es 3
optimal_k = 2
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
dataset_encoded["Cluster"] = kmeans.fit_predict(X_scaled)


# Crear un DataFrame con las características originales y los clusters asignados
cluster_data = dataset_encoded.copy()
cluster_data["Cluster"] = dataset_encoded["Cluster"]

# Graficar los clusters en función del salario promedio y la experiencia promedio
plt.figure(figsize=(8, 5))
sns.scatterplot(data=cluster_data, x="Avg_Experience", y="Avg_Salary", hue="Cluster", palette="Set1")
plt.title("Clusters de Empleos según Experiencia y Salario")
plt.xlabel("Experiencia Promedio (años)")
plt.ylabel("Salario Promedio (LPA)")
plt.legend(title="Cluster")
plt.grid(True)
plt.show()
