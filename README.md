En este repositorio pueden encontrar todo el trabajo realizado para el primer trabajo integrador de Labs de SoyHenry.
En el mismo se encomendó la realización de una API a partir de una base de datos de películas.

Los pasos seguidos en cada instancia son comentados en los mismos archivos.

El primer paso de esta tarea fue realizar la transformación de los datos para que puedan ser analizados y utilizados porteriormente por la API.

La transformación de los datos se puede visualizar en el archivo [Transformacion_datos.ipynb](https://github.com/pacokrapo/fastAPI/blob/main/Transformacion_datos.ipynb).

Una vez transformado el DataSet, el mismo es analizado en [Analisis_Exploratorio.ipynb](https://github.com/pacokrapo/fastAPI/blob/main/Analisis_Exploratorio.ipynb).

El modelo de Machine Learning puede ser visualizado con ejemplos en cada paso en [modeloML.ipynb](https://github.com/pacokrapo/fastAPI/blob/main/modeloML.ipynb).
La explicación del funcionamiento del modelo de Machine Learning puede ser visualizado en [VideoML](https://www.youtube.com/watch?v=ZrU_Kuj84BQ&ab_channel=FranciscoAndr%C3%A9sKrapovickas).

Los pasos comentados de la creación del modelo de Machine Learning se encuentran en [Fast_API.ipynb](https://github.com/pacokrapo/fastAPI/blob/main/Fast_API.ipynb).
En este mismo archivo podemos encontrar las demás funciones de la API.

La API puede ser desplegada con el comando "uvicorn Fast_API:app --reload", desde la consola y sobre la carpeta en donde se encuentra el archivo.
Aparecerá en pantalla la dirección en la que podremos visualizarla.

También puede ser visualizada en https://proyecto-fastapi-ni16.onrender.com/.
Sin embargo, debido a que la necesidad de memoria del modelo de Machine Learning supera la capacidad de memoria que ofrece Render en su versión gratuita, la función /recomendar/ no funciona en este endpoint.

Por último, los datasets utilizados y el dataset transformado se encuentran en la carpeta DataSets.

