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
    nombre1 = grafo[net_values[0][1]["nombre"]]
    insights.append(
        nombre1 +
        " es el principal productor neto de ingresos/egreso"
    )
    nombre2 = grafo[net_values[0][1]["nombre"]]
    insights.append(
        nombre2 +
        " es el segundo lugar de productor neto de ingresos/egreso"
    )
    nombre3 = grafo[net_values[0][1]["nombre"]]
    insights.append(
        nombre3 +
        " es el tercer más grande productor neto de ingresos/egreso"
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


# obtener_top 3 porcentajes mas relevantes
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
    if len(heap) > 3:
        first, keyF = heap[0][0], heap[1][0]
        second, keyS = heap[0][0], heap[1][0]
        if heap[0][0]+second >= -60:
            return ""
        heap.append([first, keyF])
        heap.append([second, keyS])
        heapq.heapify(heap)
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

    return newOutStr


def insight_perdida_recursos(grafo, newId):
    outputStr = []
    nodo = grafo[newId]
    ingresos = nodo["ingresos"]
    egresos = nodo["egresos"]
    _, sumaEgresos = calculo_total_neto(
        ingresos.values(), egresos.values())

    # Contiene un Pair(), 1er valor es el valor de perdida, 2do valor es id del nodo
    nodosPerdida = []
    reciboTotal = 0
    for keyNode in egresos:
        # Guarda cuanto dinero tiene el padre para el hijo
        salienteHijo = egresos[keyNode]
        # Guarda ID del nodo que buscamos a partir del padre
        childNode = grafo[keyNode]["ingresos"]
        # Guarda el ingreso int() que recibe como llave del padre
        ingresoPadre = childNode[newId]
        reciboTotal += ingresoPadre
        if round(ingresoPadre, 2) < round(salienteHijo-0.05, 2):
            nodosPerdida.append(
                (salienteHijo-ingresoPadre, grafo[keyNode]["nombre"]))
    if len(nodosPerdida) == 0 and round(sumaEgresos-0.05, 2) > round(reciboTotal, 2):
        outputStr.append("Observación de seguimiento:\n")
        outputStr.append(
            " - Hay una perdida en la cadena de suministro, la suma de todos los recursos causa una perdida global de ")
        outputStr.append(str(round(sumaEgresos-reciboTotal, 2)))
        outputStr.append(
            "\nSugerimos revisar cada instancia que recibe recursos desde el nodo de distribucion '")
        outputStr.append(nodo["nombre"])
        outputStr.append("'")
        return "".join(outputStr)

    if len(nodosPerdida) > 0:
        nodosPerdida.sort(reverse=True)
        outputStr.append("Observación de seguimiento:\n")
        outputStr.append(
            " - Hay una perdida de recursos, sugerimos revisar el traslado de recursos desde")
        outputStr.append(nodo["nombre"])
        outputStr.append(" a los siguientes nodos de distribucion:\n")
        cantNodes = min(3, len(nodosPerdida))

        for i in range(cantNodes):
            outputStr.append(" - '")
            nodeName = nodosPerdida[i][1]
            outputStr.append(nodeName)
            outputStr.append("' | Este presenta una perdida de: ")
            outputStr.append(str(round(nodosPerdida[i][0], 2)))
            outputStr.append("\n")

        return "".join(outputStr)
    return ""


def generar_insights(grafo, newId=None):
    insights = []
    method = insight_porcentajes(grafo, newId)
    if len(method) > 0:
        insights.append(method[0])

    method = insight_perdida_recursos(grafo, newId)
    if len(method) > 0:
        insights.append(method[0])


a = {
    "nombre": "nodo A",
    "sinIngresos": True,
    "ingresos": {},
    "egresos": {'B': 30, 'C': 20, 'D': 40, 'E': 50, 'F': 7}
}
b = {
    "nombre": "nodo B",
    "sinIngresos": False,
    "ingresos": {'A': 29.98},
    "egresos": {'C': 5}
}

c = {
    "nombre": "nodo C",
    "sinIngresos": False,
    "ingresos": {'A': 19.95, 'B': 5},
    "egresos": {}
}
d = {
    "nombre": "nodo D",
    "sinIngresos": False,
    "ingresos": {'A': 39.99},
    "egresos": {}
}
e = {
    "nombre": "nodo E",
    "sinIngresos": False,
    "ingresos": {'A': 49.95},
    "egresos": {}
}
f = {
    "nombre": "nodo F",
    "sinIngresos": False,
    "ingresos": {'A': 6.99},
    "egresos": {}
}
auxDic = {'A': a, 'B': b, 'C': c, 'D': d, 'E': e, 'F': f}


def threshold_bajo(grafo):
    grafoNeto = popula_flujo_neto(grafo)

    mediaEstadisticagrafoNetoDeDiferencia = 0
    cont = 0
    for x, y in grafoNeto:
        mediaEstadisticaDeDiferencia += x
        cont += 1

    grafoNeto.sort()
