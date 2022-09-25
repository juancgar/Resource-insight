from hashlib import new
import math
import heapq


def calculo_total_neto(ingresos, egresos):  # Recibe un diccionario
    # Regresamos ingreso total y egreso total
    return sum(x for x in ingresos), sum(x for x in egresos)

# Regresa un arreglo de flujo neto sorteado


def popula_flujo_neto(grafo):  # Recibe un diccionario <Object.id, Object>
    net_values = []
    for curObj in grafo:
        nodo = grafo[curObj]
        sinIngresos = nodo["sinIngresos"]
        sinEgresos = nodo["sinEgresos"]
        if sinIngresos or sinEgresos:
            continue
        ingresos = nodo["ingresos"]
        egresos = nodo["egresos"]
        ingreso, egreso = calculo_total_neto(
            ingresos.values(), egresos.values())
        net_values.append((ingreso-egreso, curObj))
    net_values.sort(reverse=True)
    return net_values


def insight_top_3(grafo):  # Recibe un diccionario <Object.id, Object>
    net_values = popula_flujo_neto(grafo)
    insights = []
    # Regresaremos informacion del top 3 de nodos que reciba y envíe información
    top = min(len(net_values), 3)
    for idx in range(top):
        nombre = grafo[net_values[idx][1]]["nombre"]
        insights.append(
            "El nodo " + " es el nodo de distribucion #" + str(idx+1)
        )
    return insights

# Este nodo manda tanto % a su hijo, pero su hijo solo le regresa X %
# Insights sobre ese nodo


def porcentajes_top3_nodos(outputStr, stats, nodo, sumaEgresos, grafo):
    outputStr.append("El nodo de distribucion '")
    outputStr.append(nodo["nombre"])
    outputStr.append("' ofrece:\n")
    for nodeId, cantidad in stats:
        outputStr.append("- ")
        outputStr.append(str(round(cantidad / sumaEgresos * 100, 2)))
        outputStr.append("%")
        outputStr.append(" de sus recursos en el nodo de distribucion '")
        outputStr.append(grafo[nodeId]["nombre"])
        outputStr.append("'\n")


# def obtener_top 3 porcentajes mas relevantes
def insight_porcentajes(grafo, newId):
    nodo = grafo[newId]
    ingresos = nodo["ingresos"]
    egresos = nodo["egresos"]
    _, sumaEgresos = calculo_total_neto(
        ingresos.values(), egresos.values())

    # Guarda valores ordenados de mayor a menor en formato Heapq(<"valor de egreso">, <"id de otro nodo">)
    heap = []  # Ejemplo: [[-40, 'B'],[-30,'C']]
    for keyNode in egresos:  # Itera sobre un diccionario de adyacencias
        heap.append([-1 * egresos[keyNode], keyNode])
    heapq.heapify(heap)
    if heap[0][0]+heap[1][0]+heap[2][0] >= -60:
        return ""

    cantHijos = min(len(heap), 3)
    egresoTop3Nodos = 0
    stats = []  # Var temporal guarda pares en formato Pair()
    for i in range(cantHijos):
        cantEgreso, nodoQueRecibe = heapq.heappop(heap)
        cantEgreso *= -1
        egresoTop3Nodos += cantEgreso
        stats.append((nodoQueRecibe, cantEgreso))

    outputStr = []
    porcentajes_top3_nodos(outputStr, stats, nodo, sumaEgresos, grafo)

    if len(egresos) > 3:
        restante = sumaEgresos-egresoTop3Nodos
        outputStr.append("\n")
        outputStr.append(str(round(restante / sumaEgresos * 100, 2)))
        outputStr.append("% ")
        outputStr.append(
            "Se distribuyen al resto de los nodos de distribucion (son ")
        outputStr.append(str(len(egresos)-3))
        outputStr.append(")")
    newOutStr = "".join(outputStr)
    print("debug", newOutStr)

    return newOutStr


def generar_insights(grafo, newId=None):
    insights = []
    firstInsi = insight_porcentajes(grafo, newId)
    if len(firstInsi) > 0:
        insights.append(firstInsi[0])

    # if len(heap) >= 4:
    # stats.append()
    # if nodo.sinIngresos:
    # insights.append(
    # "El nodo " + nodo.nombre + " ofrece " + sumaEgresos
    # )


a = {
    "nombre": "nodo A",
    "sinIngresos": True,
    "ingresos": {},
    "egresos": {'B': 30, 'C': 20, 'D': 40, 'E': 50, 'F': 7}
}
b = {
    "nombre": "nodo B",
    "sinIngresos": False,
    "ingresos": {'A': 200},
    "egresos": {'C': 5}
}

c = {
    "nombre": "nodo C",
    "sinIngresos": False,
    "ingresos": {'A': 3034, 'B': 5},
    "egresos": {}
}
d = {
    "nombre": "nodo D",
    "sinIngresos": False,
    "ingresos": {'A': 1},
    "egresos": {}
}
e = {
    "nombre": "nodo E",
    "sinIngresos": False,
    "ingresos": {'A': 1},
    "egresos": {}
}
f = {
    "nombre": "nodo F",
    "sinIngresos": False,
    "ingresos": {'A': 1},
    "egresos": {}
}
auxDic = {'A': a, 'B': b, 'C': c, 'D': d, 'E': e, 'F': f}
insight_porcentajes(auxDic, 'A')
