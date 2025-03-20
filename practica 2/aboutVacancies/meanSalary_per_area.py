import pandas as pandita;
import os;

#limpiar la consola
clear = lambda: os.system('cls');
clear();
dataset = pandita.read_csv("./Jobs.csv");

"""
    Because theres different rows with differents description (type_of_job), but with the same area, we define 
    a dictionary to clasify the vacancies per area
"""

areas = {
    "Marketing": ["Marketing", "Digital", "SEO", "Advertising", "Content Writer", "Social Media"],
    "Business": ["Sales", "Business Development", "Telecaller", "Relationship Manager", "Corporate Sales"],
    "IT and Development": ["Developer", "Software", "Full Stack", "Python", "PHP", "AI", "Cybersegurity", "Engineer", "Java"],
    "HR": ["Human Resources", "HR", "Recruiter"],
    "Multimedia Design": ["Graphic Designer", "Video Editor", "Illustrator", "Visual"],
    "Finance and Contability": ["Accountant", "Finance", "Auditor"]
};

def classify_area(job_title):
    if pandita.isna(job_title):
        return "Other"
    job_title = str(job_title)
    for area, keywords in areas.items():
        if any(keyword in job_title for keyword in keywords):
            return area
    return "Other"

def extract_salary(salary_str):
    if pandita.isna(salary_str):
        return None, None
    try:
        salary_str = salary_str.replace("₹", "").replace("LPA", "").strip();
        min_salary, max_salary = salary_str.split(" - ");
        return float(min_salary), float(max_salary);
    except:
        return None, None;

dataset[["Min_Salary", "Max_Salary"]] = dataset["salary"].apply(lambda x: pandita.Series(extract_salary(x)));
dataset["Avg_Salary"] = dataset[["Min_Salary", "Max_Salary"]].mean(axis=1);
dataset["Job_Area"] = dataset["Type_of_job"].apply(classify_area)

salary_by_area = dataset.groupby("Job_Area")["Avg_Salary"].mean();

print(salary_by_area.sort_values(ascending=False));