from aima.search import hill_climbing, simulated_annealing, exp_schedule
from abia_azamon_problem import AzamonProblem
from azamon_state import generate_initial_state
from azamon_problem_parameters import ProblemParameters, crear_asignacion_ordenada
from abia_azamon import *
from azamon_state import crear_solucio_inicial_baratescares
import random
import statistics
import timeit
import pandas as pd
import matplotlib.pyplot as plt
import csv

def menu_experimentacion():
    print("Menú de Configuración de Experimentación")
    rango_inferior = float(input("Introduce el límite inferior del rango de ponderación de felicidad: "))
    rango_superior = float(input("Introduce el límite superior del rango de ponderación de felicidad: "))
    paso = float(input("Introduce el incremento para cada paso de la ponderación de felicidad: "))
    num_experimentaciones = int(input("Introduce el número de experimentaciones por cada ponderación: "))
    num_paquetes = int(input("Introduce el número de paquetes por experimento: "))
    
    return rango_inferior, rango_superior, paso, num_experimentaciones, num_paquetes

###### EXPERIMENTO 1 #########
def experiment_sols_inicials():
    mitjanes = []
    funcions_inicials = [crear_asignacion_suboptima, crear_solucio_inicial_baratescares, crear_asignacion_ordenada]
    
    for f in funcions_inicials:  
        inicials = []
        finals = []
        iteracions = []
        temps_hill_climbing = []
        print("Función de estado inicial =", f.__name__)
        
        for s in semilla:  
            paquetes = random_paquetes(50, s)
            ofertas = random_ofertas(paquetes, 1.2, 1234)
            params = ProblemParameters(paquetes, ofertas)
            estado_inicial = generate_initial_state(params, f)
            start_time = timeit.default_timer()
            inicials.append(estado_inicial.cost_calcular())
            
            n = hill_climbing(AzamonProblem(estado_inicial))
            end_time = timeit.default_timer()
            temps_hill_climbing.append(end_time - start_time)
            
            finals.append(n.cost_calcular())
            iteracions.append(n.contador)
        
        mitjanes.append([f.__name__, statistics.mean(inicials), statistics.mean(finals), statistics.mean(iteracions), statistics.mean(temps_hill_climbing)])
    
    print(mitjanes)
    for x in mitjanes:
        print(x)
        print()
experiment_sols_inicials()
###### EXPERIMENTO 2 #########
def grafics_boxplot(valors,nombres_categorias):
    #valors es una llista de llistes amb els valors agafats
    labels_experimentacio = ["bat_cares","suboptima","ordenada"]
    i = 1 #la primera posicio es el nom de la categoria
    while i < len(valors[1]):  # zip(*...) agrupa las categorías por tipo
        plt.figure(figsize=(4, 4))
        
        for _ in valors:
            # Añadir un boxplot para cada experimento en la categoría
            categoria = [x[i] for x in valors]
            plt.boxplot(categoria, vert=True, patch_artist=True)
            # Personalizar el gráfico
        plt.xticks(range(1, len(valors) + 1), [x for x in labels_experimentacio])
        plt.xlabel("Mostra")
        plt.ylabel(nombres_categorias[i-1])
        plt.title(f"Boxplot de {nombres_categorias[i-1]} amb SOL_INICIAL")
            # Mostrar el gráfico
        plt.show()
        i+=1
def experiment_operadors():
    mitjanes = []
    valors_operadors = [(False,False),(True,False),(False,True),(True,True)]
    valors_operadors = [0,1,2,3]
    
    inicial = []
    for t in valors_operadors: #volem experimentar per cada combinacio de operadorss,
        costes = []
        iteracions = []
        temps_generar_sol = []
        temps_hill_climbing = []
        print(t)
        for s in semillas: #fem n experiments amb la ponderacio y
            paquetes = random_paquetes(50, s)
            ofertas = random_ofertas(paquetes, 1.2, 1234)
            params = ProblemParameters(paquetes,ofertas,0,1,t)
            
            start_time = timeit.default_timer()
            estado_inicial = generate_initial_state(params)
            inicial.append(estado_inicial.cost_calcular())
            n = hill_climbing(AzamonProblem(estado_inicial))
            end_time = timeit.default_timer()
            temps_hill_climbing.append(end_time-start_time)
            
            costes.append(n.cost_calcular())
            iteracions.append(n.contador)
        mitjanes.append([t,costes,iteracions,temps_hill_climbing]) #guardar el resultat dels experiements amb la ponderacio y
    #print(mitjanes)
    labels_experimentacio = ["No Swap","Swap","Swap1","Swap2"]
    nombres_categorias = ["costes","iteracions","temps"]
    with open('resultados.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(["category"] + [f"iteracio {var}" for var in range(num_exp)] + ["average"])
        # Escribir los valores de las listas
        for x in mitjanes:
            i = 0
            index = mitjanes.index(x)
            writer.writerow([labels_experimentacio[index]])
            print(str(x[i]))
            while i <len(nombres_categorias):
                writer.writerow([nombres_categorias[i]] + x[i+1] + [statistics.mean(x[i+1])])
                print(statistics.mean(x[i+1]))
                i+=1
            writer.writerow([""])
    print("CSV generado exitosamente")
    grafics_boxplot(mitjanes,nombres_categorias)

###### EXPERIMENTO 3 #########
if __name__ == '__main__':
    npaq = int(input("Numero de paquetes: "))
    semilla = int(input("Semilla aleatoria: "))
    paquetes = random_paquetes(npaq, semilla)
    ofertas = random_ofertas(paquetes, 1.2, 1234)
    def execute():
        
        #inspeccionar_paquetes(paquetes)
        #inspeccionar_ofertas(ofertas)
        op_cambiar, op_swap = False, True
        parameters = ProblemParameters(paquetes,ofertas,1.5,op_cambiar,op_swap)
        estado_inicial = generate_initial_state(parameters)
        n = simulated_annealing(AzamonProblem(estado_inicial), schedule = exp_schedule(k=1,lam=0.01,limit=500))
        print("ASSIGNACIO FINAL:",n.assignacions)
        print("COST FINAL:", n.cost_calcular(), "FELICITAT FINAL: ",n.felicidad())
        print("num iteracions: ",n.contador)
        print()
        

    from timeit import timeit
    print("time is " ,timeit(execute,number=1))
    costes = [i[0] for i in '''iterations''' ]
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(costes)), costes, marker='o', linestyle='-', color='b')
    #plt.plot(range(len(felicidades)), felicidades, marker='s', linestyle='--', color='r', label='Costes 2')
    plt.xlabel('Iteración (Paso)')
    plt.ylabel('Valor de la Coste')
    plt.title('Progreso de Simulated Annealing')
    plt.grid(True)
    plt.show()
###### EXPERIMENTO 4 #########
rango_inf, rango_sup, num_exp,num_paquetes = 0,3,10,50#menu_experimentacion()
print(f"Número de experimentaciones: {num_exp}")
semillas = [random.randint(0, 1000) for _ in range(num_exp)]
print("SEMILLES DE LA EXPERIMENTACIÓ:",semillas)

def experiment_proporcion_peso():
    exp_proporcion = []
    exp_paquets = []
    rango_proporcion = [1.2,2.6]
    rango_paquets = [50,150]
    p = rango_proporcion[0]
    while p<=rango_proporcion[1]: #volem experimentar per cada valor de ponderacio
        costes = []
        felicidades = []
        temps_hill_climbing = []
        print("proporcion =",p)
        for s in semillas: #fem n experiments amb la ponderacio y
            paquetes = random_paquetes(50, s)
            ofertas = random_ofertas(paquetes, p, 1234)
            params = ProblemParameters(paquetes,ofertas)
            
            start_time = timeit.default_timer()
            estado_inicial = generate_initial_state(params)
            n = hill_climbing(AzamonProblem(estado_inicial))
            end_time = timeit.default_timer()
            temps_hill_climbing.append(end_time-start_time)
            
            costes.append(n.cost_calcular())
            felicidades.append(n.felicidad())
        exp_proporcion.append(statistics.mean(temps_hill_climbing)) #guardar el resultat dels experiements amb la ponderacio y
        p += 0.2
    plt.figure(figsize=(10, 6))
    plt.plot(range(int(rango_proporcion[0]*10),int(rango_proporcion[1]*10)+1,2), exp_proporcion, marker='o', linestyle='-', color='b')
    plt.xlabel('Valor proporcion')
    plt.ylabel('Temps Execució')
    plt.title('Progreso de Hill Climbing')
    plt.grid(True) 
    
    #experiment en funcio de paquets
    num_paquetes = rango_paquets[0]
    while num_paquetes<=rango_paquets[1]: #volem experimentar per cada valor de ponderacio
        costes = []
        felicidades = []
        temps_hill_climbing = []
        print("num_paquetes =",num_paquetes)
        for s in semillas: #fem n experiments amb la ponderacio y
            paquetes = random_paquetes(num_paquetes, s)
            ofertas = random_ofertas(paquetes, 1.2, 1234)
            params = ProblemParameters(paquetes,ofertas)
            
            start_time = timeit.default_timer()
            estado_inicial = generate_initial_state(params)
            n = hill_climbing(AzamonProblem(estado_inicial))
            end_time = timeit.default_timer()
            temps_hill_climbing.append(end_time-start_time)
            
            costes.append(n.cost_calcular())
            felicidades.append(n.felicidad())
        exp_paquets.append(statistics.mean(temps_hill_climbing)) #guardar el resultat dels experiements amb la ponderacio y
        num_paquetes += 10
    plt.figure(figsize=(10, 6))
    plt.plot(range(rango_paquets[0],rango_paquets[1]+1,10), exp_paquets, marker='o', linestyle='-', color='b')
    #plt.plot(range(len(felicidades)), felicidades, marker='s', linestyle='--', color='r', label='Costes 2')
    plt.xlabel('Número Paquetes')
    plt.ylabel('Temps Execució')
    plt.title('Progreso de Hill Climbing')
    plt.grid(True)
    plt.show()    
experiment_proporcion_peso()
rango_paquetes = [50, 150]
incremento_paquetes = 10
num_experimentos = 10

num_paquetes_list = []
costes_iniciales = []
costes_finales = []
tiempos = []
pasos = []

num_paquetes = rango_paquetes[0]
while num_paquetes <= rango_paquetes[1]:
    costes_ini = []
    costes_fin = []
    tiempos_exp = []
    pasos_exp = []

    for _ in range(num_experimentos):  
        paquetes = random_paquetes(num_paquetes, 1234)
        ofertas = random_ofertas(paquetes, 1.2, 1234)
        params = ProblemParameters(paquetes, ofertas)

        estado_inicial = generate_initial_state(params)
        coste_inicial = estado_inicial.cost_calcular()
        costes_ini.append(coste_inicial)

        start_time = timeit.default_timer()
        solucion = hill_climbing(AzamonProblem(estado_inicial))
        tiempo_total = timeit.default_timer() - start_time
        tiempos_exp.append(tiempo_total)
        pasos_exp.append(solucion.contador)

        coste_final = solucion.cost_calcular()
        costes_fin.append(coste_final)

    num_paquetes_list.append(num_paquetes)
    costes_iniciales.append(statistics.mean(costes_ini))
    costes_finales.append(statistics.mean(costes_fin))
    tiempos.append(statistics.mean(tiempos_exp) * 100) 
    pasos.append(statistics.mean(pasos_exp))

    num_paquetes += incremento_paquetes
    print(num_paquetes)

plt.figure(figsize=(10, 6))
plt.plot(num_paquetes_list, costes_iniciales, 'b-o', label='Coste inicial (€)')
plt.plot(num_paquetes_list, costes_finales, 'g-o', label='Coste final (€)')
plt.plot(num_paquetes_list, pasos, 'y-o', label='Pasos')
plt.plot(num_paquetes_list, tiempos, 'r-o', label='Tiempo (cs)')

plt.xlabel('Número de paquetes')
plt.ylabel('Valores promedio')
plt.title('Impacto del número de paquetes en los resultados')
plt.legend()
plt.grid(True)
plt.show()


###### EXPERIMENTO 5 #########

###### EXPERIMENTO 6 #########
rango_inf, rango_sup, paso, num_exp, num_paquetes = menu_experimentacion()
print(f"Número de experimentaciones: {num_exp}")
semilla = 1234
print("SEMILLAS DE LA EXPERIMENTACIÓN:", semilla)

def experiment_ponderacio_marginal():
    resultados = []
    referencia_inicial = None

    ponderacion_felicidad = rango_inf
    while ponderacion_felicidad <= rango_sup:
        costes = []
        felicidades = []

        print(f"\nPonderación de felicidad actual: {ponderacion_felicidad}")
        
        for _ in range(num_exp):
            paquetes = random_paquetes(num_paquetes, semilla)
            ofertas = random_ofertas(paquetes, 1.2, 1234)
            
            params = ProblemParameters(paquetes, ofertas, pond_felicitat=ponderacion_felicidad)
            estado_inicial = generate_initial_state(params)
            solucion = hill_climbing(AzamonProblem(estado_inicial))

            costes.append(solucion.cost_calcular())
            felicidades.append(solucion.felicidad())
        
        coste_promedio = statistics.mean(costes)
        felicidad_promedio = statistics.mean(felicidades)

        if referencia_inicial is None:
            referencia_inicial = {
                "coste": coste_promedio,
                "felicidad": felicidad_promedio
            }

        delta_felicidad = felicidad_promedio - referencia_inicial["felicidad"]
        delta_coste = coste_promedio - referencia_inicial["coste"]
        margen = delta_felicidad / delta_coste if delta_coste != 0 else 0

        resultados.append({
            "ponderacion_felicidad": ponderacion_felicidad,
            "coste_promedio": coste_promedio,
            "felicidad_promedio": felicidad_promedio,
            "margen_felicidad_coste": margen
        })

        print(f"Coste promedio: {coste_promedio}, Felicidad promedio: {felicidad_promedio}, Margen: {margen}")
        
        ponderacion_felicidad += paso

    df_resultados = pd.DataFrame(resultados)
    print("\nResultados del experimento:")
    print(df_resultados)

    plt.figure(figsize=(12, 6))
    plt.plot(df_resultados["ponderacion_felicidad"], df_resultados["margen_felicidad_coste"], marker='o', linestyle='-')
    plt.xlabel('Ponderación de la Felicidad')
    plt.ylabel('Margen de Felicidad por Coste Adicional')
    plt.title('Margen de Felicidad/Coste Adicional en función de la Ponderación')
    plt.grid(True)
    plt.show()

###### EXPERIMENTO 7 #########
semilla = 1234
print("SEMILLAS DE LA EXPERIMENTACIÓN:", semilla)


def experiment_ponderacio_marginal(rango_inf, rango_sup, paso):
    resultados = []
    referencia_inicial = None

    ponderacion_felicidad = rango_inf
    while ponderacion_felicidad <= rango_sup:
        costes = []
        felicidades = []

        print(f"\nPonderación de felicidad actual: {ponderacion_felicidad}")
        
        for _ in range(num_exp):
            paquetes = random_paquetes(num_paquetes, semilla)
            ofertas = random_ofertas(paquetes, 1.2, 1234)
            
            params = ProblemParameters(paquetes, ofertas, pond_felicitat=ponderacion_felicidad)
            estado_inicial = generate_initial_state(params)
            solucion = simulated_annealing(AzamonProblem(estado_inicial), schedule=exp_schedule(k=1, lam=0.01, limit=1000))

            costes.append(solucion.cost_calcular())
            felicidades.append(solucion.felicidad())
        
        coste_promedio = statistics.mean(costes)
        felicidad_promedio = statistics.mean(felicidades)

        if referencia_inicial is None:
            referencia_inicial = {
                "coste": coste_promedio,
                "felicidad": felicidad_promedio
            }

        # Calcular el margen con respecto a la primera solución
        delta_felicidad = felicidad_promedio - referencia_inicial["felicidad"]
        delta_coste = coste_promedio - referencia_inicial["coste"]
        margen = delta_felicidad / delta_coste if delta_coste != 0 else 0

        resultados.append({
            "ponderacion_felicidad": ponderacion_felicidad,
            "coste_promedio": coste_promedio,
            "felicidad_promedio": felicidad_promedio,
            "margen_felicidad_coste": margen
        })

        print(f"Coste promedio: {coste_promedio}, Felicidad promedio: {felicidad_promedio}, Margen: {margen}")
        
        ponderacion_felicidad += paso

    # Mostrar resultados en un DataFrame para facilitar el análisis
    df_resultados = pd.DataFrame(resultados)
    print("\nResultados del experimento:")
    print(df_resultados)

    # Verificar que el DataFrame no esté vacío antes de graficar
    if not df_resultados.empty:
        # 1. Gráfico del margen de felicidad por coste adicional
        plt.figure(figsize=(10, 6))
        plt.plot(df_resultados["ponderacion_felicidad"], df_resultados["margen_felicidad_coste"], marker='o', linestyle='-')
        plt.xlabel('Ponderación de la Felicidad')
        plt.ylabel('Margen de Felicidad por Coste Adicional')
        plt.title('Margen de Felicidad/Coste Adicional en función de la Ponderación')
        plt.grid(True)
        plt.show()

        # 2. Gráfico del coste y felicidad promedio en función de la ponderación de felicidad
        plt.figure(figsize=(10, 6))
        plt.plot(df_resultados["ponderacion_felicidad"], df_resultados["coste_promedio"], label='Coste Promedio', marker='o')
        plt.plot(df_resultados["ponderacion_felicidad"], df_resultados["felicidad_promedio"], label='Felicidad Promedio', marker='s', color='red')
        plt.xlabel('Ponderación de la Felicidad')
        plt.ylabel('Valores Promedios')
        plt.title('Coste y Felicidad Promedio en función de la Ponderación de Felicidad')
        plt.legend()
        plt.grid(True)
        plt.show()

        # 3. Gráfico combinado de coste y felicidad en un gráfico de doble eje
        fig, ax1 = plt.subplots(figsize=(10, 6))

        ax1.plot(df_resultados["ponderacion_felicidad"], df_resultados["coste_promedio"], color='blue', label="Coste", linewidth=2)
        ax1.set_xlabel('Ponderación de la Felicidad')
        ax1.set_ylabel('Coste', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        # Crear un segundo eje para la felicidad en la misma gráfica
        ax2 = ax1.twinx()
        ax2.plot(df_resultados["ponderacion_felicidad"], df_resultados["felicidad_promedio"], color='red', label="Felicidad", linewidth=2)
        ax2.set_ylabel('Felicidad', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        # Título y leyenda
        plt.title('Coste y Felicidad Promedio en función de la Ponderación de Felicidad')
        fig.tight_layout()  # Ajustar el layout para que no se solapen las etiquetas
        plt.show()
    else:
        print("No se generaron datos suficientes para graficar.")

# Ejecutar el experimento con los valores obtenidos
experiment_ponderacio_marginal(rango_inf, rango_sup, paso)


###### EXPERIMENTO 8 #########

