import numpy as np
import sys
import re

# Obter colunas problema[:,#coluna]
# Obter fila problema[#fila, :]

# lemos o arquivo de entrada para criar a matriz com os coeficientes do problema
def readInput(inputName):
    arr = []
    f = open (inputName,"r")
    f1 = f.readlines()
    contador = 0
    for x in f1:
        arr.append([])
        contador = contador +1
    row = 0
    for x in f1:
        y=0
        while y < len(x):    
            if(x[y] == "-"):
                string =x[y]+x[y+1]
                if(not re.match('^[-+]?[0-9]+$',string)):
                    print("Formato de entrada incorreto \n" ," caractere invalido encontrado : ",string )
                    print("Por favor verifique o arquivo input.txt")
                    wait = input("Pressione qualquer tecla para finalizar.")
                    sys.exit()
                arr[row].append(int(string))
                y = y+1   
            elif(x[y] != "-" and x[y] != " " and x[y] != "\n"):
                if(not re.match('^[-+]?[0-9]+$',x[y])):
                    print("Formato de entrada incorreto \n" ," caractere invalido encontrado : ",x[y] )
                    print("Por favor verifique o arquivo input.txt")
                    wait = input("Pressione qualquer tecla para finalizar.")
                    sys.exit()
                arr[row].append(int(x[y]))
            y = y +1            
        row = row + 1
    print(arr)
    if(not comprovarDimensoes(arr)):
        print("A matriz não possui os coeficientes")
        print("Por favor verifique o arquivo input.txt")
        wait = input("Pressione qualquer tecla para finalizar.")
        sys.exit()
    
    return arr

def comprovarDimensoes(matrix):
    flag = True
    error = 1
    aux = len(matrix[0])
    for x in matrix:
        if(len(x) != aux):
            flag = False
            break
        error = error + 1
    if (not flag):
        print("Primeiro Erro na linha: ",error)
    return flag
    
# Este método irá determinar em quais colunas as variáveis ​​são encontradas na forma canônica factível
# Caso não seja encontrado no FCF, o usuário será notificado e a execução do programa será encerrada
# Irá retornar um array indicando quais são nossas variáveis ​​básicas iniciais
def calcularFCF(problem): 
    linhas = problem.shape[0]
    colunas = problem.shape[1]-1
    flags = []
    solution = []
    for x in range (0,colunas):
        flags.append(True)
    for n in range(0,linhas-1):
        for m in range(0,colunas):
            if(flags[m]):
                if(problem[n][m]== 1):
                    for i in range (n+1,linhas):
                        if(problem[i][m] != 0):
                            flags[m] = False
                    if( flags[m] ): 
                            solution.append(m)
                elif( problem[n][m] != 1 and problem[n][m] != 0 ):
                    flags[m] = False
    aux = np.array(solution)
    if(len(aux) < problem.shape[0]-1):
        print("Esse problema não se encontra solução básica factível")
        wait = input("Pressione qualquer tecla para finalizar.")
        sys.exit()
    return aux

# Neste método se cria a matriz B a partir das soluções máximas factíveis
def crearB(A,B_aux):
    B = np.zeros((A.shape[0] ,len(B_aux)))
    for x in range(0,len(B_aux)):
        B = (np.insert(B, B.shape[1], A[: , B_aux[x]], 1))
    B = B[:,len(B_aux):B.shape[1]]
    print("B = ")
    print (B)
    return B
#Neste método se declara o vetor C 
def crearc_B(c,B_aux):
    values=[]
    for x in range(0,len(B_aux)):
        values.append(c[B_aux[x]])
    c_B = np.array(values)
    print("c_B = ",c_B)
    return c_B

#Neste método será verificado se todos os c sub j são maiores que zero
def comprobar(c_barra):
    flag = True
    for x in range(0,len(c_barra)):
        if(c_barra[x] < 0):
            flag = False
    if flag:
        print("Todos los c_j son mayores o iguales a cero")
    else:
        print("Almenos un c_j no es mayor a cero")
    return flag

# Nesse método calculamos qual será a coluna pivô
# retorna o valor de s
def minCol(c_barra):
    tocompare = []
    for x in range(0,len(c_barra)):
        if(c_barra[x] < 0):
            tocompare.append(c_barra[x])
    min_c = np.amin(tocompare)
    index =list(c_barra).index(min_c)
    print("La columna pivote se ha calculado s = ",index)
    return index


# Neste método calculamos qual será a linha pivô
# retorna o valor de r
# Se não houver A_s's maiores que zero,
# determina que não há solução factível
def minFila(b,A_sBarra,col):  
    global control
    b = b.reshape(1,len(A_sBarra)) 
    tocompare = []
    for x in range(0,b.shape[1]):
        if(A_sBarra[x] > 0):
            tocompare.append( b[0][x]/A_sBarra[x])
    if(len(tocompare) == 0):
        print("Solucion factible no acotada")
        control = False
        return "error"
    else:
        min_f = np.amin(tocompare)
        index =list(tocompare).index(min_f)
        print("A linha pivô foi calculada r = ",index)
        return index

#este método atualiza as variáveis ​​básicas da linha e coluna pivôdef replaceB(B_aux,VB,VNB):
    print("A variavel A",VB," entra em B")
    print("A variavel A",B_aux[VNB]," sai de B")
    B_aux[VNB] = VB
    print("B = ",B_aux)
    return B_aux

# O vetor coluna P^s é criado
def createP_s(a_rs,A_s,col):
    result = []
    for x in range(0,len(A_s)):
        if(x == col):
            result.append(1/a_rs)
        else:
            result.append((A_s[x]*(-1))/a_rs)
    aux = np.array(result)
    print("P_s = ",aux)
    return aux

# A matriz P é criada a partir de uma matriz identidade e do vetor P^s
def createP(P_s,minFila): 
     result = np.identity(len(P_s))
     result[:, minFila] = P_s
     print("P = ")
     print(result)
     return result

# se calcula la inversa de B
def createB_inverse(B_inverse,P):
    result = np.dot(P,B_inverse)
    print("Inversa de B = ")
    print(result)
    return result

def main():
    print("Metodo Simplex Revisado \n \n")
    problem = np.array(readInput("input.txt")) 
    ## Primeira iteração
    print("Problema Inicial = ")
    print(problem)
    A = problem[0:(problem.shape[0] - 1):, 0:(problem.shape[1] - 1)].copy() #Matriz A 
    print("A = ")
    print(A)
    b = problem[0:(problem.shape[0] - 1):,(problem.shape[1] - 1)].copy().reshape(problem.shape[0] - 1,1) # Vetor b (coeficientes)
    print("b = ")
    print(b)
    c = problem[problem.shape[0] - 1,: problem.shape[1] - 1 ].copy() # Vetor c (valores de z)
    print("c = ",c)
    B_aux = calcularFCF(problem) #Vetor B_0
    print("B = ", B_aux)
    B = crearB(A,B_aux)
    B_inverse =np.identity(problem.shape[0]-1)


    c_B = crearc_B(c,B_aux)
    pi_z = np.dot(c_B,B_inverse)
    print("pi_z = ",pi_z)
    c_barra = c - (np.dot(pi_z,A))
    print("c _barra = ",c_barra)
    print("")

    numciclo = 1
    control = True
    ##Agora vamos executar loops até que todos os c_j sejam maiores que zero
    ## ou descobrimos que não há SBF
    while(not comprobar(c_barra) and control):
        print("")
        print("Ciclo numero ",numciclo)

        ColumnaPivote = minCol(c_barra)
        A_sBarra =np.dot(B_inverse,A[:, ColumnaPivote] )
        FilaPivote = minFila(b,A_sBarra,minCol)
        if(FilaPivote == "error"):
            break
        B_aux = replaceB(B_aux,ColumnaPivote,FilaPivote)
        B = crearB(A,B_aux)
        a_rs = A[FilaPivote][ColumnaPivote]
        print("a_rs = ",a_rs)
        P_s = createP_s(a_rs,A_sBarra,FilaPivote)
        P = createP(P_s,FilaPivote)
        B_inverse = createB_inverse(B_inverse,P)
        c_B = crearc_B(c,B_aux)
        pi_z = np.dot(c_B,B_inverse)
        print("pi_z = ",pi_z)
        c_barra = c - (np.dot(pi_z,A))
        print("c_barra = ",c_barra)
        numciclo = numciclo+1
        print("")
        print("")

# assim que a condição for satisfeita, encontraremos o SBF
    if(control == True):
        print("\n \n Soluçao Otima")
        b_barra = np.dot(B_inverse,b)
        print("b_barra = ")
        print(b_barra)
        z_result  = np.dot(pi_z,b)
        print("z = ", z_result)
        if z_result==0:
            print("No existe solucion Factible, z = 0")

main()
wait = input("Pressione qualquer tecla para finalizar.")







