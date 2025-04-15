import pandas as pandita
import matplotlib.pyplot as plt
import seaborn as sns
import os;

#limpiar la consola
clear = lambda: os.system('cls');
clear();
dataset = pandita.read_csv("./Jobs.csv");

# Preprocesamiento (si no lo hiciste antes)
areas = {
    "Marketing": ["Marketing", "Digital", "SEO", "Advertising", "Content Writer", "Social Media"],
    "Business": ["Sales", "Business Development", "Telecaller", "Relationship Manager", "Corporate Sales"],
    "IT and Development": ["Developer", "Software", "Full Stack", "Python", "PHP", "AI", "Cybersegurity", "Engineer", "Java"],
    "HR": ["Human Resources", "HR", "Recruiter"],
    "Multimedia Design": ["Graphic Designer", "Video Editor", "Illustrator", "Visual"],
    "Finance and Contability": ["Accountant", "Finance", "Auditor"]
}

# Función para clasificar por área
def classify_area(job_title):
    if pandita.isna(job_title):
        return "Other"
    job_title = str(job_title)
    for area, keywords in areas.items():
        if any(keyword in job_title for keyword in keywords):
            return area
    return "Other"

# Aplicar clasificación de áreas
dataset["Job_Area"] = dataset["Type_of_job"].apply(classify_area)

# Función para extraer salarios mínimo y máximo
def extract_salary(salary_str):
    if pandita.isna(salary_str):
        return None, None
    try:
        salary_str = salary_str.replace("₹", "").replace("LPA", "").strip()
        min_salary, max_salary = salary_str.split(" - ")
        return float(min_salary), float(max_salary)
    except:
        return None, None

# Extraer salarios
dataset[["Min_Salary", "Max_Salary"]] = dataset["salary"].apply(lambda x: pandita.Series(extract_salary(x)))
dataset["Avg_Salary"] = dataset[["Min_Salary", "Max_Salary"]].mean(axis=1)

# Definir los gráficos que quieres generar
charts = [
    {"type": "pie", "column": "Job_Area", "title": "Distribución de Áreas de Trabajo"},
    {"type": "bar", "column": "Job_Area", "title": "Salario Promedio por Área"},
    {"type": "hist", "column": "Avg_Salary", "title": "Histograma de Salarios Promedio"},
    {"type": "box", "column": "Avg_Salary", "title": "Boxplot de Salarios Promedio"},
    {"type": "scatter", "x": "Min_Salary", "y": "Max_Salary", "title": "Min vs Max Salary"}
]

# Crear carpeta de salida
output_dir = "graficas"
os.makedirs(output_dir, exist_ok=True)

# Generar gráficas
for i, chart in enumerate(charts):
    plt.figure(figsize=(8, 5))

    if chart["type"] == "pie":
        dataset[chart["column"]].value_counts().plot.pie(autopct="%1.1f%%")
        plt.title(chart["title"])
        plt.ylabel("")  # quitar etiqueta de y

    elif chart["type"] == "bar":
        means = dataset.groupby(chart["column"])["Avg_Salary"].mean().sort_values(ascending=False)
        means.plot(kind="bar", color="skyblue", edgecolor="black")
        plt.title(chart["title"])
        plt.ylabel("Salario Promedio (LPA)")
        plt.xticks(rotation=45)

    elif chart["type"] == "hist":
        dataset[chart["column"]].dropna().plot.hist(bins=15, color="orange", edgecolor="black")
        plt.title(chart["title"])
        plt.xlabel("Salario Promedio (LPA)")

    elif chart["type"] == "box":
        sns.boxplot(x=dataset[chart["column"]])
        plt.title(chart["title"])
        plt.xlabel("Salario Promedio (LPA)")

    elif chart["type"] == "scatter":
        sns.scatterplot(data=dataset, x=chart["x"], y=chart["y"])
        plt.title(chart["title"])
        plt.xlabel("Salario Mínimo")
        plt.ylabel("Salario Máximo")

    # Guardar cada gráfica
    plt.tight_layout()
    plt.savefig(f"{output_dir}/grafico_{i+1}_{chart['type']}.png")
    plt.close()

print("Gráficas generadas correctamente en la carpeta 'graficas'.")