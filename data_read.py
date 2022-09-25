import math


def calculo_total_neto(ingresos, egresos):  # Recibe un diccionario
    # Regresamos ingreso total y egreso total
    return sum(x for x in ingresos), sum(x for x in egresos)

# Regresa un arreglo de flujo neto sorteado


def popula_flujo_neto(grafo):  # Recibe un diccionario <Object.id, Object>
    net_values = []
    for curObj in grafo:
        nodo = grafo[curObj]
        if nodo.sinIngresos or nodo.sinEgresos:
            continue
        ingreso, egreso = calculo_total_neto(
            nodo.ingresos.values(), nodo.egresos.values())
        net_values.append((ingreso-egreso, curObj))
    net_values.sort(reverse=True)
    return net_values


def insight_top_3(grafo):  # Recibe un diccionario <Object.id, Object>
    net_values = popula_flujo_neto(grafo)
    insights = []
    # Regresaremos informacion del top 3 de nodos que reciba y envíe información
    top = min(len(net_values), 3)
    for idx in range(top):
        insights.append(
            "El nodo " + grafo[net_values[idx][1]].nombre +
            " es el nodo de distribucion #" + str(idx+1)
        )
    return insights

# Este nodo manda tanto % a su hijo, pero su hijo solo le regresa X %
# Insights sobre ese nodo


def curiosities_about_node(grafo, nombre):
    return
