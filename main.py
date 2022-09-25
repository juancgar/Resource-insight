from typing import Union
from typing import Dict
from pydantic import BaseModel
from fastapi import FastAPI
from data_read import popula_flujo_neto

app = FastAPI()


class GraphBase(BaseModel):

    nombre: str
    ingresos: int
    egresos: int
    sinIngresos: bool
    sinEgresos: bool

@app.get("/")
def home():
    return {"message":"Hello TutLinks.com"}
    
#regresa un arreglo de tuplas con su id y el valor neto ordenado de mayor a menor
#parametro json y regresa un arreglo
@app.post("/get-net-flux")
def get_net_flux(data:Dict[str,GraphBase]):
    return popula_flujo_neto(data)
    
    
