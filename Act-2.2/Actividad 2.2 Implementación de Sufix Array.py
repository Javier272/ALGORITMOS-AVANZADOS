#Luis Fernando Rojo Valdes A01640584
#Javier Solorzano A01645642
def generar_sufijos(cadena):

    n = len(cadena)
    lista_sufijos = []

    for i in range(n):  # O(n)
        sufijo = cadena[i:]
        lista_sufijos.append(sufijo)

    # O(n log n)
    lista_sufijos.sort()

    return lista_sufijos

cadena = input("Ingresa un string \n")

lista_sufijos = generar_sufijos(cadena)

for sufijo in lista_sufijos:
    print(sufijo)
