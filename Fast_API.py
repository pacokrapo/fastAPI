from fastapi import FastAPI
import uvicorn
import pandas as pd

#Para iniciar, en terminal, luego de ubicarse en el directorio de este archivo, ingresar el siguiente comando:
#uvicorn Fast_API:app --reload

#En consola podrá ver el directorio para acceder a la API.
#Ejemplo: http://127.0.0.1:8000/

#También pueden acceder a la API en https://proyecto-fastapi-ni16.onrender.com/


MoviesDataset = pd.read_csv("movies_dataset_final.csv", sep=',')

app = FastAPI()

MoviesOverviews = []
MoviesTitle = []

for i in range(len(MoviesDataset)):
    MoviesOverviews.append(MoviesDataset["overview"][i])
    MoviesTitle.append(MoviesDataset["title"][i])

from nltk.tokenize import word_tokenize

for i in range(len(MoviesOverviews)):
    if type(MoviesOverviews[i]) == str: 
        MoviesOverviews[i] = word_tokenize(MoviesOverviews[i])
    else:
        MoviesOverviews[i] = []

import string

MoviesOverviews2 = [[] for _ in range(len(MoviesOverviews))]

for i in range(len(MoviesOverviews)):
    for word in MoviesOverviews[i]:
        for letter in word:
            if letter in string.punctuation:
                word=word.replace(letter,"")
        MoviesOverviews2[i].append(word)

MoviesOverviews3 = [[] for _ in range(len(MoviesOverviews))]

for i in range(len(MoviesOverviews2)):
    for word in MoviesOverviews2[i]:
        if word != "":
            MoviesOverviews3[i].append(word)

MoviesOverviews4 = [[] for _ in range(len(MoviesOverviews))]

for i in range(len(MoviesOverviews3)):
    for word in MoviesOverviews3[i]:
        word = word.lower()
        MoviesOverviews4[i].append(word)

MoviesOverviews5 = [[] for _ in range(len(MoviesOverviews))]

for i in range(len(MoviesOverviews4)):
    for word in MoviesOverviews4[i]:
        if len(word)>=3:
            MoviesOverviews5[i].append(word)

from nltk.corpus import stopwords

nltk.download("stopwords")

a=set(stopwords.words('english'))

MoviesOverviews6 = [[] for _ in range(len(MoviesOverviews))]

for i in range(len(MoviesOverviews5)):
    MoviesOverviews6[i] = [word for word in MoviesOverviews5[i] if word not in a]


from gensim import corpora, models, similarities


generador_elementos = (elemento for elemento in MoviesOverviews6)


diccionario = corpora.Dictionary(generador_elementos)


ListaCorpus = []

for i in range(len(MoviesOverviews6)):
    ListaCorpus.append(diccionario.doc2bow(MoviesOverviews6[i]))

tfidf = models.TfidfModel(ListaCorpus)

corpus_tfidf = tfidf[ListaCorpus]

index = similarities.MatrixSimilarity(corpus_tfidf)


#Pantalla de inicio
@app.get("/")
def inicio():
    return "Opciones: /cantidad_filmaciones_mes  /cantidad_filcaciones_dia  /score_titulo  /votos_titulo  /actor  /director"

#Función de cantidad de filmaciones por mes:
@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes: str):
    mes = str(mes)
    if len(mes)<2:
        mes="0"+mes
    cantidad = 0
    for i in range(0,len(MoviesDataset)):
        if MoviesDataset['release_date'][i][5:7] == mes:
            cantidad += 1
    return {'mes':mes, 'cantidad':cantidad}

#Función de cantidad de filmaciones por dia:
@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia: str):
    dia = str(dia)
    if len(dia)<2:
        dia="0"+dia
    cantidad = 0
    for i in range(0,len(MoviesDataset)):
        if MoviesDataset['release_date'][i][8:10] == dia:
            cantidad += 1
    return {'dia':dia, 'cantidad':cantidad}

#Función de puntaje por titulo:
@app.get('/score_titulo/{titulo}')
def score_titulo(titulo: str):  
    titulo = titulo.title()
    if titulo in list(MoviesDataset["title"]):

        pelicula = MoviesDataset[MoviesDataset['title'] == titulo]
        anio_estreno = int(pelicula['release_year'])
        score = float(pelicula['popularity'])

    return {'titulo':titulo, 'anio':anio_estreno, 'popularidad':score}

    
#Función de votos por titulo:    
@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo: str):
    titulo = titulo.title()
    if titulo in list(MoviesDataset["title"]):

        pelicula = MoviesDataset[MoviesDataset['title'] == titulo]
        cantidad_votos = int(pelicula['vote_count'])
        votos_promedio = float(pelicula['vote_average'])
        anio_estreno = int(pelicula['release_year'])

        if cantidad_votos < 2000:
            return f"La película {titulo} no tiene suficientes votos"
        else:
            return {'titulo':titulo, 'anio':anio_estreno, 'voto_total':cantidad_votos, 'voto_promedio':votos_promedio}

    else:
        return f"La película {titulo} no se encuentra en el registro"
    
#Función para conocer más sobre un actor:
@app.get("/actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    nombre_actor = nombre_actor.title()
    lista_peliculas = []
    lista_retornos = []
    for i in range(0,len(MoviesDataset)):
        if nombre_actor in MoviesDataset["cast_names"][i]:
            lista_peliculas.append(MoviesDataset["title"][i])
            lista_retornos.append(MoviesDataset["return"][i])
        else:
            continue
    cantidad_peliculas = len(lista_peliculas)
    retorno_total = sum(lista_retornos)
    retorno_promedio = sum(lista_retornos)/len(lista_retornos)
    if len(lista_peliculas)>=1:
        return {'actor':nombre_actor, 'cantidad_filmaciones':cantidad_peliculas, 'retorno_total':retorno_total, 'retorno_promedio':retorno_promedio}
    else:
        return f"No se registran peliculas para dicho actor"


#Función para conocer mas sobre un director:
@app.get("/director/{nombre_director}")
def get_director(nombre_director: str):
    nombre_director = nombre_director.title()
    lista_peliculas = []
    fecha_lanzamiento = []
    retorno_ind = []
    costo = []
    ganancia = []
    for i in range(0,len(MoviesDataset)):
        if nombre_director in MoviesDataset["crew_names"][i]:
            lista_peliculas.append(MoviesDataset["title"][i])
            fecha_lanzamiento.append(MoviesDataset["release_date"][i])
            retorno_ind.append(MoviesDataset["return"][i])
            costo.append(MoviesDataset["budget"][i])
            ganancia.append(MoviesDataset["revenue"][i])
        else:
            continue
    
    retorno_total= sum(retorno_ind)

    diccionario = {"Nombre":lista_peliculas, "Release":fecha_lanzamiento, "Retorno": retorno_ind, "Costo": costo, "Ganancia": ganancia}

    return {'director':nombre_director, 'retorno_total_director':retorno_total, 
    'peliculas':diccionario["Nombre"], 'anio':diccionario["Release"], 'retorno_pelicula':diccionario["Retorno"], 
    'budget_pelicula':diccionario["Costo"], 'revenue_pelicula':diccionario["Ganancia"]}

#Funcion para conocer peliculas recomendadas a partir de un titulo:
@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    titulo = titulo.title()
    posicion = MoviesTitle.index(titulo)

    similitudes = index[corpus_tfidf[500]]

    documentos_similares_indices = similitudes.argsort()[::-1][1:6]

    Titulos = []
    for i in range(len(documentos_similares_indices)):
        Titulos.append(MoviesTitle[documentos_similares_indices[i]])

    return {'lista recomendada': Titulos}