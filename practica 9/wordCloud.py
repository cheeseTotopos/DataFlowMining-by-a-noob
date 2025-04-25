import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

clear = lambda: os.system('cls')
clear()

# Cargar dataset
dataset = pd.read_csv("Prácticas/Jobs.csv")

# Unir todos los textos de la columna "Type_of_job"
text = " ".join(str(job) for job in dataset["Type_of_job"] if pd.notnull(job))

# Crear la nube de palabras
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Mostrar la imagem
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Nube de Palabras: Type_of_job")
plt.show()
