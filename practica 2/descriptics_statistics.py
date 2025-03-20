import pandas as pandita;
import os;

#limpiar la consola
clear = lambda: os.system('cls');
clear();
dataset = pandita.read_csv("./Jobs.csv");

"""
    El count de la primera impresión, simboliza el número de empresas que están contratando, ya que el dataset
    en caso de no estar contratando, no deja un cero, sino que deja el espacio vacío en el registro.
"""
print(dataset["actively_hiring"].describe());
print(dataset["Type_of_job"].value_counts());

"""
    el número de veces que aparece la locación en los registros, por lo tanto, este print representa 
    las locaciones con más empresas, independientemente que contraten o no.
"""
print(dataset["location"].value_counts());