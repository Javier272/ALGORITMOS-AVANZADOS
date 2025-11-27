#verifica que no se haya visitado y este dentro del rango
#O(1)
def valido(x,y,matriz,n):
    if 0 <= x <n and 0 <= y < n and matriz[x][y] == -1:
        return True
    return False

#O(n^2)
def backtracking(x,y,movi, matriz, movimientoX, movimientoY, n):
    #si se han hecho todos los movimientos
    if movi == n*n:
        return True

    #intenta todos los movimientos posibles
    for i in range(8):
        nuevoX = x + movimientoX[i]
        nuevoY = y + movimientoY[i]
        if valido(nuevoX, nuevoY, matriz, n):
            matriz[nuevoX][nuevoY] = movi
            if backtracking(nuevoX, nuevoY, movi+1, matriz, movimientoX, movimientoY, n):
                return True
            #backtrack
            matriz[nuevoX][nuevoY] = -1
    return False


#O(n^2)
def kingsTour(n):
    #crear la matriz de nxn en -1
    matriz = [[-1] * n for _ in range(n)]

    #movimentos que puede hacer el caballo
    movimientoX = [2,1,-1,-2,-2,-1,1,2]
    movimientoY = [1,2,2,1,-1,-2,-2,-1]

    #inicia en posicion 0,0
    matriz[0][0] = 0

    #llama a la funcion de backtracking
    if not backtracking(0,0,1, matriz, movimientoX, movimientoY, n):
        print("No se puede solucinar")
    else:
        #imprime la matriz
        for i in range(n):
            for j in range(n):
                print(matriz[i][j], end=' ')
            print()


if __name__ == "__main__":

    n = int(input("Ingresa el valor de N: "))
    kingsTour(n)
