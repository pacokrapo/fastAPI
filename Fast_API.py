from fastapi import FastAPI
import uvicorn
import pandas as pd

#Para iniciar, en terminal, luego de ubicarse en el directorio de este archivo, ingresar el siguiente comando:
#uvicorn Fast_API:app --reload

#En consola podrá ver el directorio para acceder a la API.
#Ejemplo: http://127.0.0.1:8000/

MoviesDataset = pd.read_csv("movies_dataset_final.csv", sep=',')

app = FastAPI()

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
    if titulo in list(MoviesDataset["title"]):

        pelicula = MoviesDataset[MoviesDataset['title'] == titulo]
        anio_estreno = int(pelicula['release_year'])
        score = float(pelicula['popularity'])

    return {'titulo':titulo, 'anio':anio_estreno, 'popularidad':score}

    
#Función de votos por titulo:    
@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo: str):
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
def get_director(nombre_director):
    lista_peliculas = []
    fecha_lanzamiento = []
    retorno_ind = []
    costo = []
    ganancia = []
    exito = None
    RetornoMax = 0
    for i in range(0,len(MoviesDataset)):
        if nombre_director in MoviesDataset["crew_names"][i]:
            lista_peliculas.append(MoviesDataset["title"][i])
            fecha_lanzamiento.append(MoviesDataset["release_date"][i])
            retorno_ind.append(MoviesDataset["return"][i])
            costo.append(MoviesDataset["budget"][i])
            ganancia.append(MoviesDataset["revenue"][i])
            if MoviesDataset["return"][i]>RetornoMax:
                RetornoMax = MoviesDataset["return"][i]
                exito = MoviesDataset["title"][i]
        else:
            continue
    lista = pd.DataFrame({"Nombre":lista_peliculas, "Release":fecha_lanzamiento, "Retorno": retorno_ind, "Costo": costo, "Ganancia": ganancia})
    listajson = lista.to_json(orient="records")

    return f"El éxito del director {nombre_director} fue la película {exito} con un retorno de {RetornoMax} y su lista de películas fue la siguiente:", listajson
