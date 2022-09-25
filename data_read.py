def calculo_total_neto(ingresos, egresos):  # Recibe un diccionario
    # Regresamos ingreso total y egreso total
    return sum(x for x in ingresos), sum(x for x in egresos)


def popula_flujo_neto(grafo):
    net_values = []
    for nodo in grafo:
        if nodo.sinIngresos or nodo.sinEgresos:
            continue
        ingreso, egreso = calculo_total_neto(
            nodo.ingresos.values(), nodo.egresos.values())
        net_values.append((ingreso-egreso, nodo.id))
    net_values.sort(reverse=True)
    return net_values
