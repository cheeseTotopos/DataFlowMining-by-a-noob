import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

clear = lambda: os.system('cls')
clear()

# Cargar el dataset
dataset = pd.read_csv("./Jobs.csv")

# Clasificación de áreas
areas = {
    "Marketing": ["Marketing", "Digital", "SEO", "Advertising", "Content Writer", "Social Media"],
    "Business": ["Sales", "Business Development", "Telecaller", "Relationship Manager", "Corporate Sales"],
    "IT and Development": ["Developer", "Software", "Full Stack", "Python", "PHP", "AI", "Cybersegurity", "Engineer", "Java"],
    "HR": ["Human Resources", "HR", "Recruiter"],
    "Multimedia Design": ["Graphic Designer", "Video Editor", "Illustrator", "Visual"],
    "Finance and Contability": ["Accountant", "Finance", "Auditor"]
}

def classify_area(job_title):
    if pd.isna(job_title):
        return "Other"
    job_title = str(job_title)
    for area, keywords in areas.items():
        if any(keyword in job_title for keyword in keywords):
            return area
    return "Other"

dataset["Job_Area"] = dataset["Type_of_job"].apply(classify_area)

# Función para extraer salario mínimo y máximo
def extract_salary(salary_str):
    if pd.isna(salary_str):
        return None, None
    try:
        salary_str = salary_str.replace("₹", "").replace("LPA", "").strip()
        min_salary, max_salary = salary_str.split(" - ")
        return float(min_salary), float(max_salary)
    except:
        return None, None

# Aplicar función de salario
dataset[["Min_Salary", "Max_Salary"]] = dataset["salary"].apply(lambda x: pd.Series(extract_salary(x)))
dataset["Avg_Salary"] = dataset[["Min_Salary", "Max_Salary"]].mean(axis=1)

# Eliminar filas con salario promedio faltante
dataset = dataset.dropna(subset=["Avg_Salary"])

# Función para extraer el promedio de experiencia
def extract_experience(exp_str):
    if pd.isna(exp_str):
        return None
    try:
        exp_str = exp_str.replace(" years", "").strip()
        min_exp, max_exp = exp_str.split("-")
        return (float(min_exp) + float(max_exp)) / 2
    except:
        return None

dataset["Avg_Experience"] = dataset["experience"].apply(extract_experience)

# Eliminar filas sin experiencia promedio
dataset = dataset.dropna(subset=["Avg_Experience"])

# Codificar Job_Area y location como variables dummies
X = pd.concat([
    pd.get_dummies(dataset["Job_Area"], prefix="Area"),
    pd.get_dummies(dataset["location"], prefix="Loc"),
    dataset[["Avg_Experience"]]
], axis=1)

y = dataset["Avg_Salary"]

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelo de regresión lineal
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# R² Score
r2 = r2_score(y_test, y_pred)
print(f"R² Score con experiencia y ubicación: {r2:.4f}")

# Gráfico Real vs Predicho
plt.figure(figsize=(8, 5))
plt.scatter(y_test, y_pred, alpha=0.7, color='purple')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
plt.xlabel("Salario Real")
plt.ylabel("Salario Predicho")
plt.title("Modelo Lineal: Real vs Predicho")
plt.grid()
plt.tight_layout()
plt.show()

# Histograma de residuos
residuals = y_test - y_pred
plt.figure(figsize=(8, 4))
sns.histplot(residuals, bins=30, kde=True, color="orange")
plt.title("Distribución de los residuos")
plt.xlabel("Error")
plt.tight_layout()
plt.show()