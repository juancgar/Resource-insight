from urllib import request
from fastapi import Request, FastAPI
from pydantic import BaseModel
from typing import Dict
import insights as dr
import mqtt as mqtt
app = FastAPI()


class GraphBase(BaseModel):
    id: str
    nombre: str
    ingresos: int
    egresos: int
    sinIngresos: bool
    sinEgresos: bool


@app.get("/")
def home():
    return {"message": "Hello TutLinks.com"}

# regresa un arreglo de tuplas con su id y el valor neto ordenado de mayor a menor
# parametro json y regresa un arreglo


@app.post("/get-net-flux")
async def get_net_flux(request: Request):
    file = await request.json()
    return dr.insight_top_3(file)


@app.post("/get-node-with-more-error")
async def get_node_with_more_error(request: Request):
    file = await request.json()
    return dr.insight_mayor_riesgo_de_shortage(file)

@app.post("/mqtt-demonstration")
async def mqtt_demonstration(request:Request):
    file = await request.json()
    mqtt.run()
    return {200}
