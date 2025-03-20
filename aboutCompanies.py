import pandas as pandita;
import os;

#limpiar la consola
clear = lambda: os.system('cls');
clear();
dataset = pandita.read_csv("./Jobs.csv");

"""
    NUMERO DE EMPRESAS POR LOCACIÓN

    el número de veces que aparece la locación en los registros, por lo tanto, este print representa 
    las locaciones con más empresas, independientemente que contraten o no.
"""
print(dataset["location"].value_counts());

"""
    NÚMERO DE EMPLEOS QUE OFRECE CADA EMPRESA

    Ya que los registros son empleos, pueden haber varias empresas con diversos empleos. El siguiente print
    muestra cuantas veces está contratando cada empresa.
"""
hiring_companies = dataset[dataset["actively_hiring"] == 1];
top_hiring = hiring_companies["company_name"].value_counts();

print(top_hiring);


"""
    LOCACIONES CON EMPRESAS QUE SÍ CONTRATAN
"""

top_hiring_locacions = hiring_companies["location"].value_counts();
print(top_hiring_locacions);
