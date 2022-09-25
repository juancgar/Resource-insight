from fastapi import Request, FastAPI
from pydantic import BaseModel
from typing import Dict
from data_read import popula_flujo_neto

app = FastAPI()


class GraphBase(BaseModel):
    id:str
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
async def get_net_flux(request: Request):
    file = await request.json()
    return popula_flujo_neto(file)
    
