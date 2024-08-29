import random

import copy

#FUNCIONES

def obtener_direcciones():   

    """Direccion random"""

    lista_copia = direcciones.copy()         # Pide una variable externa
    random.shuffle(lista_copia)

    return lista_copia

#Dificultades

def pedir_dificultades():

    """Pide el nivel 1, 2 o 3"""

    dificultades = ["Facil","Medio","Dificil"]
    
    print("Seleccione la dificultad:")
    for i in range(len(dificultades)):
        cadena = str("➣ "+ " " + str(i+1)+"." + " "  + dificultades[i])
        print( (cadena))
    
    d = input(">")

    return d
        
    
#Verificacion de Dificultades

def verificar_dif(d):

    """Verifica que el usuario dio una respuesta valida"""

    flag = False
    while flag == False:
        if d == "1":
            flag = True
        elif d == "2":
            flag = True
        elif d == "3":
            flag = True
        else:
            d = pedir_dificultades()

    return d
        
#Palabras para la sopa de letras  

def palabraRandom(archivo):

    try:
        file = open(r"C:\Users\gabit\Escritorio\python\practicas\primer año\cuatri2\palabras.txt", mode = "rt",encoding="latin-1")                                      #Abre el archivo
    except FileNotFoundError:
        print("no se pudo encontrar el archivo, intente con otra ruta")
    except UnboundLocalError:
        print("no se pudo encontrar el archivo, intente con otra ruta")
    else:
        for i in range(random.randint(1,2000)):
            word = file.readline()
    
    return word    

def obtener_palabras(c, archivo):

    palabras = []                       #Segun la dificultad elige 8, 12, 16

    if c == "1": 
        cant = 8
        max_long = 10
    elif c == "2":
        cant = 12
        max_long = 12
    elif c =="3":
        cant = 16
        max_long = 15
    
    file = open(archivo, mode = "rt",encoding="latin-1")       
    while len(palabras)< cant:
        palabra = palabraRandom(archivo)
        if palabra not in palabras and len(palabra)<max_long:
            palabras.append(palabra.strip())
    file.close()
    
    return palabras

#Generacion de matriz

def generar_matriz(d):        

    """Crea la matriz segun la dificultad"""

    #d = d.lower()
    matriz = []
    if d == "1":
        matriz = [[0]*10 for i in range(10)]
    elif d == "2":
        matriz = [[0]*15 for i in range(15)]
    elif d == "3":
        matriz = [[0]*20 for i in range(20)]          
    return matriz 
        
#Verificacion de espacios

def hay_espacio(matriz,palabra,fila,columna,direccion):

    """Se fija si la palabra tendra lugar o no"""

    for letra in palabra:                                                                       
        if fila < 0 or columna < 0 or columna >= len(matriz) or fila >= len(matriz):        #El comienzo debe estar dentro la matriz    
            return False
        elif matriz[fila][columna] != 0 and matriz[fila][columna] != letra:                 #El lugar a cambiar debe ser 0 o la misma letra
            return False
        else:                                                                               #Va sumando x,y segun como sea la direccion
            fila += direccion[0]                                                            #Si va para abajo solo suma y, x va a sumar 0
            columna += direccion[1]

    return True

#Rellena la matriz 

def rellenar_matriz(matriz):

    """Rellena la matriz con palabras random del abecedario"""

    for i in range(len(matriz)):                                            
        for j in range(len(matriz)):
            if matriz[i][j] == 0:                                                  #Todo lo que es 0 se intercambia por una letra al azar
                matriz[i][j] = random.choice(abecedario)                           #Usan una variable externa

#Acomoda las palabras

def acomodar_palabra(matr,palabra,direcciones, inicios):             # CAMBIAR Limite de intentos, returns, siempre te elimina una direccion

    cont = 0
    while cont < 50:
        x = random.randint(0,len(matr))
        y = random.randint(0,len(matr))
        for i in range(7):
            direc = direcciones[i]
            if hay_espacio(matr,palabra,x,y,direc):
                inicios.append([x, y])
                for letras in palabra:
                    letra = letras.upper()
                    matr[x][y] = letra
                    x += direc[0]  
                    y += direc[1] 
                return matr
        cont += 1

    return False

#Imprime matriz

def print_matrix(matrix,palabras):                     
    for index in range(len(matrix)):
        line = matrix[index]
        for char in line:
            print(char, end=" ")
        try:
            print(f" | {palabras[index]}")
        except:
            print(' | ')
                        
#Muestra solucion 

def mostrar_solucion(matriz_solucion):        # Antes de rellenbr la matriz, crea otra nueva matriz intercambiando 0 por .
    print("Aqui esta la solucion: ")

    for fila in matriz_solucion:
        for elemento in fila:
            if elemento == 0:
                print( "%3s" %("∙"),end="")
            else: 
                print("%3s" %(elemento),end="")
        print()

#PROGRAMA PRINCIPAL

abecedario = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z"]


print("BIENVENIDO A LA SOPA DE LETRAS DEL GRUPO 2")

direcciones = [
    (1,0), #abajo
    (-1,0), #arriba
    (0,1), #derecha
    (0,-1), #izquierda
    (-1,1), #diagonal ar d
    (-1,-1), #diagonal ar i
    (1,1), #diagonal ab d
    (1,-1) #diagonal ab i
]

dificultad = pedir_dificultades()
dificultad = verificar_dif(dificultad)
matriz = generar_matriz(dificultad)
palabras = obtener_palabras(dificultad,r"C:\Users\gabit\Escritorio\python\practicas\primer año\cuatri2\palabras.txt")

inicios = []
for palabra in palabras:
    a = acomodar_palabra(matriz,palabra,obtener_direcciones(), inicios)
    while a == False:
        a = acomodar_palabra(matriz,palabraRandom("palabras.txt"),obtener_direcciones(), inicios)

#-----------------------------------------------------------
palabras_coordenadas = {}

for palabra in palabras:
    for inicio in inicios:
        palabras_coordenadas[palabra] = inicio
        inicios.remove(inicio)
        break
# print(palabras_coordenadas)
for key, value in palabras_coordenadas.items():
    print(key,":",value)
#-----------------------------------------------------------
matriz_solucion = copy.deepcopy(matriz)           

rellenar_matriz(matriz)

print_matrix(matriz,palabras)

intentos = 0
cont_encontradas = 0

while intentos < 3 and cont_encontradas < len(palabras):
    respuesta_solucion = input("Escriba la palabra encontrada (escriba 'solucion' para ver las respuestas):  ")

    if respuesta_solucion == "solucion":
        mostrar_solucion(matriz_solucion)
    if respuesta_solucion.upper() in palabras_coordenadas.keys():
        encontrada = respuesta_solucion.upper()
        fila, columna = input("De las coordenadas del inicio de la palabra ('fila columna'), empezando desde 1 1: ").split()
        coordenada = [int(fila)-1, int(columna)-1]
        if coordenada == palabras_coordenadas[respuesta_solucion.upper()]:
            print("correcto")
            palabras_coordenadas.pop(encontrada)
            cont_encontradas += 1
        else:
            intentos += 1
            print(("incorrecto") , "te quedan", 3-intentos,"vidas")
            
    else:
        intentos += 1
        print(("incorrecto") , "te quedan", 3-intentos,"vidas")
        
    if intentos == 3:
        print( "perdiste")
        print("la solucion era: ")
        mostrar_solucion(matriz_solucion)
        break
    if cont_encontradas == len(palabras):
        print("ganaste!!!")
        print("tuviste",intentos,"errores")
        break