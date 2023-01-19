from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Union, List
from jwt_manager import create_token

app=FastAPI()
app.title="Mi aplicacion con FastAPI"
app.version = "0.0.1"

class User(BaseModel):
    email:str
    password: str


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2023)
    rating: Union[int, float] = Field(..., gt=0.0, le=10.0)
    category: str = Field(..., min_length=1, max_length=10)

    class Config:
        schema_extra={
            "example":{
                "id":1,
                "title":"Mi pelicula",
                "overview":"Descripcion de la pelicula",
                "year":2018,
                "rating": 6.8,
                "category":"drama"
            }
        }

movies = [
    {
        "id":1,
        "title":"Avatar",
        "overview":"En un exuberante planeta llamado Pandora viven los Na'vi...",
        "year":"2009",
        "rating":7.8,
        "category":"action"
    },
    {
        "id":2,
        "title":"Terminator",
        "overview":"En una ciudad utopica existe un androide llamado terminator...",
        "year":"2001",
        "rating":5.3,
        "category":"drama"
    }
]

###---------- GET ------------------
@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1> Hello world! </h1>')

##########################
@app.post('/login', tags=['auth'])
def login(user: User):
    return user
##########################

@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(status_code=404, content=[])

@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [item for item in movies if item["category"]==category]
    return JSONResponse(content=data)

###---------- POST ------------------

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie( movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201 ,content={"message":"Se ha registrado la pelicula"})

###---------- PUT ------------------

@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id:int, movie: Movie) -> dict:
    for item in movies:
        if item["id"]==id:
            item["title"]=movie.title
            item["overview"]=movie.overview
            item["year"]=movie.year
            item["rating"]=movie.rating
            item["category"]=movie.category
            return JSONResponse(status_code=200, content={"message":"Se ha modificado la pelicula"})   

###---------- DELETE ------------------

@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id:int) -> dict:
    for item in movies:
        if item["id"]==id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={"message":"Se ha eliminado la pelicula"})

