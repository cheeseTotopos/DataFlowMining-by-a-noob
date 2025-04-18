import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor

clear = lambda: os.system('cls')
clear()
print("Directorio de trabajo actual:", os.getcwd())

# Cargar datos
dataset = pd.read_csv("prácticas/Jobs.csv")

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

# Extraer salarios
def extract_salary(salary_str):
    if pd.isna(salary_str):
        return None, None
    try:
        salary_str = salary_str.replace("₹", "").replace("LPA", "").strip()
        min_salary, max_salary = salary_str.split(" - ")
        return float(min_salary), float(max_salary)
    except:
        return None, None

dataset[["Min_Salary", "Max_Salary"]] = dataset["salary"].apply(lambda x: pd.Series(extract_salary(x)))
dataset["Avg_Salary"] = dataset[["Min_Salary", "Max_Salary"]].mean(axis=1)

# Extraer experiencia promedio
def extract_experience(exp_str):
    if pd.isna(exp_str):
        return None
    try:
        exp_str = exp_str.replace("years", "").strip()
        min_exp, max_exp = exp_str.split("-")
        return (float(min_exp) + float(max_exp)) / 2
    except:
        return None

dataset["Avg_Experience"] = dataset["experience"].apply(extract_experience)

# Limpiar dataset
dataset = dataset.dropna(subset=["Avg_Salary", "location", "Avg_Experience"])

# Codificar variables categóricas
X = pd.get_dummies(dataset[["Job_Area", "location"]])
X["Avg_Experience"] = dataset["Avg_Experience"]

y = dataset["Avg_Salary"]

# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Escalar datos (KNN lo necesita)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Crear y entrenar modelo KNN
knn = KNeighborsRegressor(n_neighbors=5)
knn.fit(X_train_scaled, y_train)

# Predecir
y_pred = knn.predict(X_test_scaled)

# Evaluación
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print(f"R² Score: {r2:.4f}")
print(f"Mean Squared Error: {mse:.4f}")

# Visualizar predicciones vs reales
plt.figure(figsize=(8, 5))
plt.scatter(y_test, y_pred, alpha=0.6, color='teal')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
plt.xlabel("Salario Real")
plt.ylabel("Salario Predicho")
plt.title("KNN: Real vs Predicho")
plt.grid(True)
plt.tight_layout()
plt.show()
