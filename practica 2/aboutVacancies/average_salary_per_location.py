import pandas as pandita;
import os;

#limpiar la consola
clear = lambda: os.system('cls');
clear();
dataset = pandita.read_csv("./Jobs.csv");

# filter minimum and maximum salary
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

salary_by_location = dataset.groupby("location")["Avg_Salary"].mean();
print(salary_by_location.sort_values(ascending=False));

