from typing import Union

from fastapi import FastAPI
from data_read import popula_flujo_neto

app = FastAPI()


def get_flujo_neto():
    # AQUI VA LA LLAMADA
    grafo = []  # [nombre, id, ingresos, egresos]

    popula_flujo_neto(grafo)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
