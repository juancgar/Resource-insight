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
            "El nodo " + nombre + " es el nodo de distribucion #" + str(idx+1)
        )
    return insights

# Este nodo manda tanto % a su hijo, pero su hijo solo le regresa X %
# Insights sobre ese nodo


class object1:
    def __init__(self):
        self.nombre = "nodo A"
        self.sinIngresos = True
        self.ingresos = {}
        self.egresos = {'B': 40, 'C': 30}


class object2:
    def __init__(self):
        self.nombre = "nodo B"
        self.sinIngresos = False
        self.ingresos = {'A': 20}
        self.egresos = {'C': 5}


class object3:
    def __init__(self):
        self.nombre = "nodo C"
        self.sinIngresos = False
        self.ingresos = {'A': 30, 'B': 5}
        self.egresos = {}


def porcentajes_top3_nodos(outputStr, stats, nodo, sumaEgresos, grafo):
    outputStr.append(["El nodo de distribucion '", nodo.nombre, "' ofrece:\n"])
    for nodeId, cantidad in stats:
        print("debug", nodeId, cantidad)
        outputStr.append('- ')
        outputStr.append(str(round(cantidad / sumaEgresos * 100, 2)))
        outputStr.append('%')
        outputStr.append(" de sus recursos en el nodo de distribucion '")
        outputStr.append(grafo[nodeId].nombre)
        outputStr.append("'\n")


def curiosities_about_node(grafo, newId):
    insights = []
    nodo = grafo[newId]
    _, sumaEgresos = calculo_total_neto(
        nodo.ingresos.values(), nodo.egresos.values())

    # Guarda valores ordenados de mayor a menor en formato Heapq(<"valor de egreso">, <"id de otro nodo">)
    heap = []  # Ejemplo: [[-40, 'B'],[-30,'C']]
    for keyNode in nodo.egresos:  # Itera sobre un diccionario de adyacencias
        heap.append([-1 * nodo.egresos[keyNode], keyNode])
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
    if len(heap) > 3:
        outputStr.append("\nEl ")
        restante = sumaEgresos-egresoTop3Nodos
        outputStr.append(str(round(restante / sumaEgresos * 100, 2)))
        # outputStr.append("\nEl resto de los nodos de distribucion (son ")
        # outputStr.append(len(heap)-cantHijos)
        # outputStr.append(") ")
    # newOutStr = "".join(outputStr)
    # if len(cantHijos) <= 3:
    #     outputStr.append("\n")
    #     if egresoTotalCurNode < sumaEgresos-0.05:
    #         outputStr.append("Observación de seguimiento:\n")
    #         outputStr.append(" - Hay una perdida de recursos, se despleg\n")
    #     outputStr.append()
    # if len(cantHijos) > 3:
    #     outputStr.append("\n ")
    #     outputStr.append("\nSus dependencias utilizan el ")
    # print(newOutStr)


    # if len(heap) >= 4:
    # stats.append()
    # if nodo.sinIngresos:
    # insights.append(
    # "El nodo " + nodo.nombre + " ofrece " + sumaEgresos
    # )
a = object1()
b = object2()
c = object3()
auxDic = {'A': a, 'B': b, 'C': c}
#curiosities_about_node(auxDic, 'A')

def threshold_bajo(grafo):
    grafoNeto = popula_flujo_neto(grafo)

    mediaEstadisticagrafoNetoDeDiferencia = 0
    cont = 0
    for x,y in grafoNeto:
        mediaEstadisticaDeDiferencia += x
        cont += 1
    
    
    grafoNeto.sort()
