import pandas as pandita
import scipy.stats as stats
import os

clear = lambda: os.system('cls')
clear()
dataset = pandita.read_csv("./Jobs.csv")

areas = {
    "Marketing": ["Marketing", "Digital", "SEO", "Advertising", "Content Writer", "Social Media"],
    "Business": ["Sales", "Business Development", "Telecaller", "Relationship Manager", "Corporate Sales"],
    "IT and Development": ["Developer", "Software", "Full Stack", "Python", "PHP", "AI", "Cybersegurity", "Engineer", "Java"],
    "HR": ["Human Resources", "HR", "Recruiter"],
    "Multimedia Design": ["Graphic Designer", "Video Editor", "Illustrator", "Visual"],
    "Finance and Contability": ["Accountant", "Finance", "Auditor"]
}

def classify_area(job_title):
    if pandita.isna(job_title):
        return "Other"
    job_title = str(job_title)
    for area, keywords in areas.items():
        if any(keyword in job_title for keyword in keywords):
            return area
    return "Other"

# Aplica la clasificación a la columna correspondiente
dataset["Job_Area"] = dataset["Type_of_job"].apply(classify_area)

# Función para extraer el salario
def extract_salary(salary_str):
    if pandita.isna(salary_str):
        return None, None
    try:
        salary_str = salary_str.replace("₹", "").replace("LPA", "").strip()
        min_salary, max_salary = salary_str.split(" - ")
        return float(min_salary), float(max_salary)
    except:
        return None, None

# Aplicar extracción
dataset[["Min_Salary", "Max_Salary"]] = dataset["salary"].apply(lambda x: pandita.Series(extract_salary(x)))

# Calcular el salario promedio
dataset["Avg_Salary"] = dataset[["Min_Salary", "Max_Salary"]].mean(axis=1)

# Comparar salario promedio entre áreas
grouped_data = [group["Avg_Salary"].dropna().values for name, group in dataset.groupby("Job_Area")]

# ANOVA
anova_result = stats.f_oneway(*grouped_data)
print("ANOVA result:", anova_result)

# Kruskal-Wallis
kruskal_result = stats.kruskal(*grouped_data)
print("Kruskal-Wallis result:", kruskal_result)
