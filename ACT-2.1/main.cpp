#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>
#include <iomanip>
using namespace std;


int main(){
    string fileName="prueba.txt";
    int n=8; //n multiplos de 4, 16<=n<=64

    
    ifstream file(fileName, ios::binary);//abrir el archivo en binario para detectar todo tipo de caracteres
    if (!file){
        cerr << "No se puede abrir el archivo "<<fileName<<endl;
        return -1;
    }

    vector<unsigned char> w;
    char c;
    while (file.get(c)){
        w.push_back(static_cast<unsigned char>(c));//leer caracter por caracter y guardarlo en w
    }
    file.close();

    while (w.size() % n != 0){//rellenar con ceros hasta que w.size() sea multiplo de n
        w.push_back((unsigned char)n);
    }

    vector<int> a(n,0);//se crea vector de tamaño n inicializado en 0

    for (size_t i=0; i<w.size(); i++){
        int columna = i%n;

        a[columna] = (a[columna] + w[i]) % 256; //suma los valores en la columna que corresponde
    }

    //convertir a hexadecimal
    stringstream ss;
    for (int i=0; i<n /4; i++){
        ss << hex << setw(2) << setfill('0') << a[i];
    }

    cout <<"Codigo hash: "<<ss.str()<<endl;


    return 0;

}