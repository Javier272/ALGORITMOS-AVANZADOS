#include <iostream>
#include <string>
#include <sstream>
#include <fstream>
#include <vector>

using namespace std;


string leerArchivo(const string &nombreArchivo){
    string caracteres, linea;

    ifstream archivo(nombreArchivo);
    if(!archivo.is_open()){
        cerr <<"No se puede abrir"<<nombreArchivo<<endl;
        return "";
    }

    while (getline(archivo, linea)){
        caracteres += linea;
    }

    archivo.close();
    return caracteres;
    
}

vector<int> tablaLPS(const string &patron){
    int m = patron.size();
    vector<int> lps(m,0);
    int len = 0;
    int i = 1;

    while (i < m){
        if (patron[i] == patron[len]){
            len++;
            lps[i] = len;
            i++;
        } else {
            if (len != 0){
                len = lps[len - 1];
            } else {
                lps[i] = 0;
                i++;
            }
        }
    }
    return lps;
}


int kmp(const string &texto, const string &patron){
    int n = texto.size();
    int m = patron.size();
    if (m==0 || n==0){
        return -1;
    }
    vector<int> lps = tablaLPS(patron);
    int i = 0; //texto
    int j = 0; //patron


    while (i < n){
        if (patron[j] == texto[i]){
            i++;
            j++;
        }
        if (j == m){
            return i-j;

        }
        if (i<n && texto[i] != patron[j]){
            if (j != 0){

                j=lps[j-1];
            } else{

                i++;
            }
        }
    }
    return -1;

}


void palindromoLargo(const string &s, int &inicio, int &fin){
    int n= s.size();

    if(n==0){
        inicio= fin=0;
        return;
    }

    vector<vector<bool>> dp(n, vector<bool>(n,false));
    inicio=0;
    int maxLength=1;

    for(int i=0; i<n; i++){
        dp[i][i]=true;
    }

    for(int len=2; len<=n; len++){
        for(int i=0; i<=n-len; i++){
            int j=i+len-1;

            if(s[i] == s[j] && (len==2 || dp[i+1][j-1])){
                dp[i][j]= true;
                if(len> maxLength){
                    maxLength=len;
                    inicio=i;
                }
            }
        }
    }

    fin=inicio+maxLength-1;
    inicio++;
    fin++;
}


void stringMasLargo(const string &t1, const string &t2, int &inicio, int &fin){
    int n1= t1.size();
    int n2= t2.size();

    vector<vector<int>> dp(n1+1, vector<int>(n2+1,0));
    int maxLength=0;
    int posfin=0;

    for(int i=1; i<=n1; i++){
        for(int j=1; j<=n2; j++){
            if(t1[i-1] == t2[j-1]){
                dp[i][j]= dp[i-1][j-1]+1;
                if(dp[i][j]> maxLength){
                    maxLength= dp[i][j];
                    posfin=i - 1;
                }
            }
        }
    }

    if(maxLength==0){
        inicio=fin=0;
        return;
    }

    inicio=posfin - maxLength +2;
    fin=posfin + 1;
}

int main(){
    //lee los archivos
    string transmission1= leerArchivo("transmission1.txt");
    string transmission2= leerArchivo("transmission2.txt");
    string mcode1= leerArchivo("mcode1.txt");
    string mcode2= leerArchivo("mcode2.txt");
    string mcode3= leerArchivo("mcode3.txt");


    //los guarda en vectores para recorrer cada archivo mas facil
    vector<string> transmissions={transmission1,transmission2};
    vector<string> mcodes={mcode1,mcode2,mcode3};

    //recorre cada transmission
    for (int j=0; j<2; j++){

        //recorre cada mcode
        for(int i=0; i<3; i++){
            int pos= kmp(transmissions[j], mcodes[i]);

            if(pos != -1){
                cout<<"transmission"<<j+1<<" es "<<"TRUE"<<" para mcode"<<i+1<<" secuecia: "<<pos+1<<endl;
            } else{
                cout<<"transmission"<<j+1<<" es "<<"FALSE"<<" para mcode"<<i+1<<endl;
            }
        }
        
    }

    //ciclo para recorrer cada transmission y encontrar el palindromo mas largo
    for(int j=0; j<2; j++){
        int inicio=0;
        int fin=0;

        palindromoLargo(transmissions[j], inicio, fin);
        cout<<"transmission"<<j+1<<": palindromo desde "<<inicio<<" a "<<fin<<endl;
    }


    //encotrar el substring mas largo entre las dos transmissions
    int inicio=0;
    int fin=0;
    stringMasLargo(transmission1, transmission2, inicio, fin);
    cout<<"substring mas largo entre transmission1 y transmission2 desde "<<inicio<<" a "<<fin<<endl;

    return 0;
}