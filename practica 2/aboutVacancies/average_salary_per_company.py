import pandas as pandita;
import os;

#limpiar la consola
clear = lambda: os.system('cls');
clear();
dataset = pandita.read_csv("./Jobs.csv");


def filter_experience(years_range):
    if pandita.isna(years_range):
        return None, None;

    try:
        years_range = years_range.replace("years", "").strip();
        min_years, max_years = years_range.split("-");
        return float(min_years), float(max_years);
    except:
        return None, None;

dataset[["min_years", "max_years"]] = dataset["experience"].apply(lambda range: pandita.Series(filter_experience(range)));
dataset["average_experience"] = dataset[["min_years", "max_years"]].mean(axis=1);
experience_by_company = dataset.groupby("company_name")["average_experience"].mean();


print(experience_by_company.sort_values(ascending=False));
