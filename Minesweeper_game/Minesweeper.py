import random
import os


# CREA LA MATRIZ TABLA
def diseno_tabla(hileras, columnas, val):
    tabla = []
    for i in range(hileras):
        tabla.append([])
        for j in range(columnas):
            tabla[i].append(val)
    return tabla


# IMPRIME EL TABLERO
def mostrar_tabla(tabla):
    for hileras in tabla:
        print("_", end=" ")
    print("_")
    for hileras in tabla:
        print("|", end=" ")
        for elemento in hileras:
            print(elemento, end=" ")
        print("|")
    for hileras in tabla:
        print("_", end=" ")
    print("_")


# COLOCA LA BOMBAS EN LA MATRIZ TABLA
def colocar_bombas(tabla, bombas, hileras, columnas):
    num = 0
    bombas_invisibles = []
    while num < bombas:
        y = random.randint(0, hileras - 1)
        x = random.randint(0, columnas - 1)
        if tabla[y][x] != 9:
            tabla[y][x] = 9
            num += 1
            bombas_invisibles.append((y, x))
    return tabla, bombas_invisibles


# RECORRE LAS CASILLAS ALREDEDOR DE UNA MINA Y VA CUENTA LAS MINAS QUE TOCAN LAS CASILLAS RECORRIDAS
def colocar_pistas(tabla, hileras, columnas):
    for y in range(hileras):
        for x in range(columnas):
            if tabla[y][x] == 9:
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if 0 <= y + i <= hileras - 1 and 0 <= x + j <= columnas - 1:
                            if tabla[y + i][x + j] != 9:
                                tabla[y + i][x + j] += 1
    return tabla

# DESCUBRE UNA PARTE DEL MAPA CUANDO SE MUESTRA UN 0
def llenado(invisible, enpantalla, y, x, hileras, columnas, val):
    ceros = [(y, x)]
    while len(ceros) > 0:
        y, x = ceros.pop()
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                # comprueba que se esté dentro de la tabla
                if 0 <= y + i <= hileras - 1 and 0 <= x + j <= columnas - 1:
                    if enpantalla[y + i][x + j] == val and invisible[y + i][x + j] == 0:
                        enpantalla[y + i][x + j] = 0
                        if (y + i, x + j) not in ceros:
                            ceros.append((y + i, x + j))
                    else:
                        enpantalla[y + i][x + j] = invisible[y + i][x + j]
    return enpantalla

# RECORRE LA TABLA COMPROBANDO POR *
def tabla_entera(tabla, hileras, columnas, val):
    for y in range(hileras):
        for x in range(columnas):
            if tabla[y][x] == val:
                return False
    return True


# IMPRIME LAS INSTRUCCIONES AL COMIENZO DEL JUEGO JUEGO
def interfaz():
    print(" _________________________________ ")
    print("|          BIENVENIDO A           |")
    print("|           BUSCAMINAS            |")
    print("|                                 |")
    print("|       W/A/S/D ►► MOVERSE        |")
    print("|                                 |")
    print("|          M ►► MOSTRAR           |")
    print("|                                 |")
    print("|     B/V ►► MARCAR/DESMARCAR     |")
    print("|                                 |")
    print("|_________________________________|")
    print("\n")


# IMPRIME LAS INSTRUCCIONES DURANTE EL JUEGO
def menu():
    print()
    opcion = input(" W/A/S/D ►► MOVERSE\n M ►► MOSTRAR\n B/V ►► MARCAR/DESMARCAR\n ►►")
    return opcion


# CONVIERTE LOS CEROS EN ESPECIOS
def sustituir_ceros(tabla):
    for i in range(columnas01):
        for j in range(columnas01):
            if tabla[i][j] == 0:
                tabla[i][j] = " "
    return tabla


# DEFINE EL NUMERO DE COLUMNAS, HILERAS Y BOMBAS
def dificultad():
    global columnas01, hileras01, bombas

    print("1. FACIL (10x10, 15 MINAS)")
    print("2. MEDIO (15x15, 75 MINAS)")
    print("3. DIFICIL (20x20, 200 MINAS)")
    difi = input("ELIGE LA DIFICULTAD: ")

    try:
        int(difi)
        h = True
    except ValueError:
        h = True
    else:
        if 1 <= int(difi) <= 3:
            h = False

    while h:
        print("1. FACIL (10x10, 15 MINAS)")
        print("2. MEDIO (15x15, 75 MINAS)")
        print("3. DIFICIL (20x20, 200 MINAS)")
        difi = input("ELIGE LA DIFICULTAD: ")

        try:
            int(difi)
            # h = False
        except ValueError:
            h = True
        else:
            if 1 <= int(difi) <= 3:
                h = False

    difi = int(difi)

    if difi == 1:
        columnas01 = 10
        hileras01 = 10
        bombas = 15
    elif difi == 2:
        columnas01 = 15
        hileras01 = 15
        bombas = 75
    elif difi == 3:
        columnas01 = 20
        hileras01 = 20
        bombas = 200
    return columnas01, hileras01, bombas


columnas01, hileras01, bombas = dificultad()
print(hileras01, columnas01, bombas)

enpantalla = diseno_tabla(hileras01, columnas01, "*")

invisible = diseno_tabla(hileras01, columnas01, 0)
invisible, bombas_invisibles = colocar_bombas(invisible, hileras01, hileras01, columnas01)
invisible = colocar_pistas(invisible, hileras01, columnas01)

y = random.randint(2, hileras01 - 3)
x = random.randint(2, columnas01 - 3)

real = enpantalla[y][x]
enpantalla[y][x] = "○"

interfaz()
mostrar_tabla(enpantalla)

minas_marcadas = []

ejecutando = True
ganar = False

while ejecutando:
    a = menu()
    if a == "w" or a == "W":
        if y == 0:
            y = 0
        else:
            enpantalla[y][x] = real
            y -= 1
            real = enpantalla[y][x]
            enpantalla[y][x] = "○"

    elif a == "s" or a == "S":
        if y == hileras01 - 1:
            y = hileras01 - 1
        else:
            enpantalla[y][x] = real
            y += 1
            real = enpantalla[y][x]
            enpantalla[y][x] = "○"

    elif a == "a" or a == "A":
        if x == 0:
            x = 0
        else:
            enpantalla[y][x] = real
            x -= 1
            real = enpantalla[y][x]
            enpantalla[y][x] = "○"

    elif a == "d" or a == "D":
        if x == columnas01 - 1:
            x = columnas01 - 1
        else:
            enpantalla[y][x] = real
            x += 1
            real = enpantalla[y][x]
            enpantalla[y][x] = "○"

    elif a == "b" or a == "B":
        if real == "*":
            enpantalla[y][x] = "▲"
            real = enpantalla[y][x]
            if (y, x) not in minas_marcadas:
                minas_marcadas.append((y, x))

    elif a == "v" or a == "V":
        if real == "▲":
            enpantalla[y][x] = "*"
            real = enpantalla[y][x]
            if (y, x) in minas_marcadas:
                minas_marcadas.remove((y, x))

    elif a == "m" or a == "M":
        if invisible[y][x] == 9:
            enpantalla[y][x] = "◙"
            ejecutando = False
            ganar = False

        elif invisible[y][x] != 0:
            enpantalla[y][x] = invisible[y][x]
            real = enpantalla[y][x]

        elif invisible[y][x] == 0:
            enpantalla[y][x] = 0
            enpantalla = llenado(invisible, enpantalla, y, x, hileras01, columnas01, "*")
            enpantalla = sustituir_ceros(enpantalla)
            real = enpantalla[y][x]

    # BORRA LA PANTALLA E IMPRIME LA NUEVA TABLA
    os.system("cls")
    interfaz()
    mostrar_tabla(enpantalla)

    # EVALUA SI EL TABLERO ESTÁ TERMINADO
    if tabla_entera(enpantalla, hileras01, columnas01, "*") and \
            sorted(bombas_invisibles) == sorted(minas_marcadas) and \
            real != "*":
        ganar = True
        ejecutando = False

if ganar:
    print(" _________________________________ ")
    print("|                                 |")
    print("|            YOU WIN!             |")
    print("|_________________________________|")

else:
    print(" _________________________________ ")
    print("|                                 |")
    print("|            YOU LOSE!            |")
    print("|_________________________________|")
    print(" _________________________________ ")
    print("|                                 |")
    print("|            GAME OVER            |")
    print("|_________________________________|")

q = input(print("PRESIONES ENTER PARA FINALIZAR"))
