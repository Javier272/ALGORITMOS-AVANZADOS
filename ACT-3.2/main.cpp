#include <iostream>
#include <vector>
#include <limits>


using namespace std;

// Algoritmo de Floyd-Warshall
void FloydWarshall(vector<vector<int>> matriz, int n){
    // Valor infinito para inicializar las distancias
    int infinito = numeric_limits<int>::max();
    // Matriz de adyacencia
    vector<vector<int>> distancias(n, vector<int>(n,0));
    //contador de comparaciones
    int comp=0;

    //for para llenar la matriz de adyacencia
    for(int i=0; i<n; i++){
        for(int j=0; j<n; j++){
            if(i==j){
                //se inicializa en 0 si es la misma posicion en i y j
                distancias[i][j] = 0;
            }else if(matriz[i][j] != 0){
                //se inicializa con el valor de la matriz original si es diferente de 0
                distancias[i][j] = matriz[i][j];
            }else{
                //se inicializa en infinito el resto de la matriz
                distancias[i][j] = infinito;
            }
        }
    }

    //for para mover el nodo intermedio
    for(int k=0; k<n; k++){
        //for para mover el nodo de inicio
        for(int i=0; i<n; i++){
            //for para mover el nodo de final
            for(int j=0; j<n; j++){
                comp++;
                //valida que la suma de las distancias sea menor a la distancia actual y que no sea infinito
                if(distancias[i][k] !=infinito && distancias[k][j] != infinito && distancias[i][k] + distancias[k][j] < distancias[i][j]){
                    //actualiza la distancia
                    distancias[i][j] = distancias[i][k] + distancias[k][j];
                    //incrementa el contador de comparaciones
                }

            }

        }
    }

    //imprime la matriz de distancias
    for(int i=0; i<n; i++){
        for(int j=0; j<n; j++){
            if( distancias[i][j]== infinito){
                cout<<"INFINITO ";
            }else {
                cout<<distancias[i][j]<<" ";
            }
        }
        cout<<endl;
    }

    cout<<"Numero de comparaciones con Floyd: "<<comp<<endl;


}

void Dijkstra(vector<vector<int>> matriz, int n){
    // Valor infinito para inicializar las distancias
    int infinito = numeric_limits<int>::max();

    // Vector para almacenar las distancias desde el nodo origen
    vector<int> distancias(n, infinito);
    // Vector para marcar los nodos visitados
    vector<bool> visitados(n, false);

    int comp=0;

    distancias[n-1]= 0;

    for(int i=0; i<n-1; i++){
        //la distancia minima se inicializa en infinito
        int minDist = infinito;
        int minIndex = -1;


        for(int j=0; j<n; j++){
            comp++;
            if(!visitados[j] && distancias[j] < minDist){
                minDist = distancias[j];
                minIndex = j;
            }
        }

        if(minIndex == -1){
            break; // Todos los nodos adyacentes han sido visitados
        }
        visitados[minIndex] = true;

        for(int k=0; k<n; k++){
            comp++;
            //valida que el nodo no haya sido visitado y que la distancia no sea infinito
            if(matriz[minIndex][k] != 0 && !visitados[k] && distancias[minIndex] != infinito && distancias[minIndex] + matriz[minIndex][k] < distancias[k]){
                //actualiza la distancia
                distancias[k] = distancias[minIndex] + matriz[minIndex][k];
                
            }
        }
    }

    for(int i=0; i<n; i++){
        if(distancias[i] == infinito){
            cout<<"INFINITO ";
        }else{
            cout<<distancias[i]<<" ";
        }
    }
    cout<<endl;

    cout<<"Numero de comparaciones con Dijkstra: "<<comp<<endl;

}


int main(){
    int n=20;
    vector<vector<int>> matriz{
        {0, 3, -2, 4, 7, 1, -3, 2, 6, 9, 4, -5, 7, 8, 3, 1, 5, 6, -4, 2},
        {3, 0, 5, 2, -1, 4, 7, 2, 1, 6, -3, 2, 8, 4, 1, 5, 7, -2, 6, 3},
        {-2, 5, 0, 3, 4, -1, 2, 7, 3, 1, 2, 4, -3, 6, 5, 8, 2, 4, 7, 1},
        {4, 2, 3, 0, 5, 6, 7, -2, 8, 1, 4, 3, 2, 9, 1, 4, 5, 6, 2, 7},
        {7, -1, 4, 5, 0, 2, 3, 8, 9, 4, 7, 1, 5, 6, 8, 3, 1, 5, 2, 6},
        {1, 4, -1, 6, 2, 0, 5, 3, 1, 8, 2, 7, 6, -2, 4, 5, 7, 2, 3, 8},
        {-3, 7, 2, 7, 3, 5, 0, 4, 2, 6, 1, 8, 2, 7, 9, 4, 1, 5, 2, 7},
        {2, 2, 7, -2, 8, 3, 4, 0, 5, 1, 2, 7, 9, 6, 2, 5, 7, 8, 2, 3},
        {6, 1, 3, 8, 9, 1, 2, 5, 0, 2, 4, 7, 8, 1, 6, 3, 5, 7, 2, 9},
        {9, 6, 1, 1, 4, 8, 6, 1, 2, 0, 7, 2, 5, 8, 3, 7, 9, 4, 1, 2},
        {4, -3, 2, 4, 7, 2, 1, 2, 4, 7, 0, 6, 8, 2, 3, 9, 4, 5, 1, 7},
        {-5, 2, 4, 3, 1, 7, 8, 7, 7, 2, 6, 0, 3, 1, 6, 7, 2, 5, 4, 8},
        {7, 8, -3, 2, 5, 6, 2, 9, 8, 5, 8, 3, 0, 6, 7, 5, 8, 2, 3, 7},
        {8, 4, 6, 9, 6, -2, 7, 6, 1, 8, 2, 1, 6, 0, 9, 4, 5, 7, 2, 3},
        {3, 1, 5, 1, 8, 4, 9, 2, 6, 3, 3, 6, 7, 9, 0, 3, 6, 7, 8, 4},
        {1, 5, 8, 4, 3, 5, 4, 5, 3, 7, 9, 7, 5, 4, 3, 0, 2, 1, 7, 6},
        {5, 7, 2, 5, 1, 7, 1, 7, 5, 9, 4, 2, 8, 5, 6, 2, 0, 4, 7, 3},
        {6, -2, 4, 6, 5, 2, 5, 8, 7, 4, 5, 5, 2, 7, 7, 1, 4, 0, 5, 2},
        {-4, 6, 7, 2, 2, 3, 2, 2, 2, 1, 1, 4, 3, 2, 8, 7, 7, 5, 0, 4},
        {2, 3, 1, 7, 6, 8, 7, 3, 9, 2, 7, 8, 7, 3, 4, 6, 3, 2, 4, 0}
    };



    FloydWarshall(matriz, n);
    Dijkstra(matriz, n);

    return 0;
}