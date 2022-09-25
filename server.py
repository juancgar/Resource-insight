from typing import Union
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI
from data_read import popula_flujo_neto

app = FastAPI()

class GraphBase(BaseModel):
    id: int
    nombre: str
    ingresos: int
    egresos: int

class GraphList(BaseModel):
    data: List[GraphBase]

@app.post("/get-net-flux")
async def get_net_flux(data:GraphList):
    return popula_flujo_neto(data)
