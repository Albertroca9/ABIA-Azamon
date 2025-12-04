from __future__ import annotations
from abia_azamon import *
from aima.search import hill_climbing, Problem
from typing import List, Set, Generator
from azamon_problem_parameters import ProblemParameters
from azamon_operator import *
from abia_azamon_problem import *
import math 
import matplotlib.pyplot as plt

#from experimentacio import exp_parameters

iterations = []
felicidades = []

def asignable_estricta(paquete, oferta):
        return not ((paquete.prioridad != 0 or oferta.dias != 1)
                    and (paquete.prioridad != 1 or oferta.dias != 2)
                    and (paquete.prioridad != 1 or oferta.dias != 3)
                    and (paquete.prioridad != 2 or oferta.dias != 4)
                    and (paquete.prioridad != 2 or oferta.dias != 5))
def asignable(paquete, oferta):
    if paquete.prioridad == 0:
        return oferta.dias <= 1  # Prioridad 0 requiere que el paquete llegue en 1 día o menos
    elif paquete.prioridad == 1:
        return oferta.dias <= 3  # Prioridad 1 permite hasta 3 días
    elif paquete.prioridad == 2:
        return oferta.dias <= 5  # Prioridad 2 permite hasta 5 días
    return False  # Por si se da una prioridad no válida

class StateRepresentation(object):
    def __init__(self,params, oferta_por_paquete, contador,first = None):
        self.params = params
        self.params.l_paquetes = params.l_paquetes
        self.params.l_ofertas = params.l_ofertas
        self.assignacions = oferta_por_paquete
        self.contador = contador+1

        if first:
            #print("ASSIGNACIÓ INICIAL:",self.assignacions)
            #print("COST INICIAL:",self.cost_calcular(), "FELICITAT INICIAL: ",self.felicidad())
            iterations.append((self.cost_calcular(),self.assignacions))
            felicidades.append(self.felicidad())
        
        #print("felicidad",self.felicidad())
    
    def copy(self) -> StateRepresentation:
        return StateRepresentation(self.params,self.assignacions.copy(),self.contador)

    def __repr__(self) -> str:
        return f"self.params.l_ofertas={str(self.params.l_ofertas)} | {self.params.l_paquetes}"

    # Utilitzarem aquesta funció auxiliar per trobar el contenidor
    # que conté un paquet determinat


    def generate_actions(self) -> Generator[AzamonOperator, None, None]:
        # Primer calculem l'espai lliure de cada oferta
        free_spaces = []
        """for p_i, o_i in enumerate(self.assignacions):
                pes_p_i = self.params.l_paquetes[p_i].peso
                if o_i in free_spaces:
                    free_spaces[o_i] = free_spaces[o_i] - pes_p_i
                else:
                    free_spaces[o_i] = self.params.l_ofertas[o_i].pesomax - pes_p_i"""
        for oferta_i in range(len(self.params.l_ofertas)): #iterar sobre els les ofertes
            peso_oferta_i = self.params.l_ofertas[oferta_i].pesomax #tenir el pes max de cada oferta
            for p_i,o in enumerate(self.assignacions): #saber on està cada paquet
                if o == oferta_i: #mirar si el paquet en qüestió es troba a la oferta
                    peso_oferta_i = peso_oferta_i - self.params.l_paquetes[p_i].peso #restar el pes del paquet
            free_spaces.append(peso_oferta_i) #
        ## Recorregut contenidor per contenidor per saber quins paquets podem moure
        if self.params.op_cambiar:   
            for oferta_j in range(len(self.params.l_ofertas)):
                for p_i in range(len(self.params.l_paquetes)):
                    if self.assignacions[p_i] == oferta_j:
                        for oferta_k in range(len(self.params.l_ofertas)):
                            # Condició: contenidor diferent i té espai lliure suficient i es assignable
                            if oferta_j != oferta_k and free_spaces[oferta_k] >= self.params.l_paquetes[p_i].peso and \
                            asignable(self.params.l_paquetes[p_i],self.params.l_ofertas[oferta_k]):
                                yield CambiarOferta(p_i, oferta_j, oferta_k)
        if self.params.op_swap:
            # Intercanviar paquets
            for paquete_1 in range(len(self.params.l_paquetes)):
                for paquete_2 in range(len(self.params.l_paquetes)):
                    if paquete_1 != paquete_2:
                        oferta_i = self.assignacions[paquete_1]
                        oferta_j = self.assignacions[paquete_2]

                        if oferta_i != oferta_j:
                            peso_oferta_i = self.params.l_paquetes[oferta_i].peso
                            peso_oferta_j = self.params.l_paquetes[oferta_j].peso

                            # Condició: hi ha espai lliure suficient per fer l'intercanvi
                            # (Espai lliure del contenidor + espai que deixa el paquet >= espai del nou paquet)
                            if free_spaces[oferta_i] +peso_oferta_i >= peso_oferta_j and free_spaces[oferta_j] + peso_oferta_j >=peso_oferta_i \
                            and asignable(self.params.l_paquetes[paquete_1],self.params.l_ofertas[oferta_j]) and asignable(self.params.l_paquetes[paquete_2],self.params.l_ofertas[oferta_i]):
                                yield SwapParcels(paquete_1, paquete_2)

    def apply_action(self, action: AzamonOperator) -> StateRepresentation:
        new_state = self.copy()
        if isinstance(action, CambiarOferta):
            p_i = action.p_i
            oferta_j = action.oferta_j
            oferta_k = action.oferta_k
            new_state.assignacions[p_i] = oferta_k
            #print("cambiar rebut")
        elif isinstance(action, SwapParcels):
            p_i = action.p_i
            p_j = action.p_j
            #print("swap rebut")
            new_state.assignacions[p_i],new_state.assignacions[p_j] = new_state.assignacions[p_j],new_state.assignacions[p_i]
        #print("ASSIGNACIÓ:",new_state.assignacions)
        #print("COST:",new_state.cost_calcular())
        iterations.append((self.cost_calcular(),self.assignacions))
        felicidades.append(self.felicidad())
        return new_state

    def felicidad(self):
        f = 0
        for paquete_id, oferta_id in enumerate(self.assignacions):
            paquete = self.params.l_paquetes[paquete_id]
            oferta = self.params.l_ofertas[oferta_id]
            dies_entrega = oferta.dias
            dies_demanat = paquete.prioridad*2 
            #considerem que amb prioridad 1 -> 2 dies, prioridad 2 -> 4 dies
            nova_felicitat = dies_demanat-dies_entrega
            if nova_felicitat < 0: #casos en els q s'entrega també dintre del rang, ja que no es possible que arribin més tard 
                nova_felicitat = 0
            f += nova_felicitat 
        return f
    
    def heuristica1(self):
        return self.cost_calcular()
    def heuristica2(self):
        return self.cost_calcular()-self.params.pond_felicitat*self.felicidad() 


    def cost_calcular(self) -> float:
        cost = 0.0
        for paquete, oferta in enumerate(self.assignacions):
            cost += self.params.l_paquetes[paquete].peso * self.params.l_ofertas[oferta].precio
            if self.params.l_ofertas[oferta].dias in [3, 4]:
                cost += 0.25 * self.params.l_paquetes[paquete].peso
            elif self.params.l_ofertas[oferta].dias == 5:
                cost += 0.5 * self.params.l_paquetes[paquete].peso
        return cost


def crear_solucio_inicial_baratescares(l_paquetes,l_ofertas):
    llista_preus = [y.precio for y in l_ofertas]
    #mitjana preus, per així filtrar i omplir els paquets més barat
    accum = 0
    for i in llista_preus:
        accum += i
    mitjana = accum/len(llista_preus)
    #print(mitjana)
    
    
    oferta_por_paquete = [0] * len(l_paquetes)
    peso_por_oferta = [0.0] * len(l_ofertas)

    i = 0
    ofertas_baratas = []
    ofertas_caras = []
    while i<len(l_ofertas):
        if llista_preus[i]<= mitjana:
            ofertas_baratas.append(i)
        else:
            ofertas_caras.append(i)
        i+=1
    #print("barates:",ofertas_baratas)
    #print("cares:",ofertas_caras)
    barates_i_cares = [ofertas_baratas,ofertas_caras]
    for id_paquete in range(len(l_paquetes)):
        paquete_asignado = False
        oferta_potencial = 0
        while not paquete_asignado:
            for barata_o_cara in barates_i_cares:
                for id_oferta in barata_o_cara:
                    if asignable_estricta(l_paquetes[id_paquete], l_ofertas[id_oferta]):
                        oferta_potencial = id_oferta
                        if l_paquetes[id_paquete].peso + peso_por_oferta[oferta_potencial] \
                        <= l_ofertas[oferta_potencial].pesomax:
                            peso_por_oferta[oferta_potencial] = peso_por_oferta[oferta_potencial] \
                                                         + l_paquetes[id_paquete].peso
                            oferta_por_paquete[id_paquete] = oferta_potencial
                            paquete_asignado = True
                            #print(f"Paq= {id_paquete} Env={oferta_potencial} a oferta barata" )
                            break
                if paquete_asignado:
                    break
            if not paquete_asignado:
                print("no s'ha trobat oferta per al ",id_paquete, l_paquetes[id_paquete].peso)
                break
                 
    print()
    #for id_paquete in range(len(self.params.l_paquetes)):
    #    print(f"Paq= {id_paquete} Env={oferta_por_paquete[id_paquete]}"
    #          f" P={self.params.l_paquetes[id_paquete].prioridad}"
    #          f" D={self.params.l_ofertas[oferta_por_paquete[id_paquete]].dias}")
    #for id_oferta in range(len(self.params.l_ofertas)):
    #    print(f"Env= {id_oferta}"
    #          f" Weight={peso_por_oferta[id_oferta]}"
    #          f" MXweight={self.params.l_ofertas[id_oferta].pesomax}")
    #    if self.params.l_ofertas[id_oferta].pesomax < peso_por_oferta[id_oferta]:
    #        print("Esta situación no se debería dar. ¡Reportadlo!")
    #        raise RuntimeError
    return oferta_por_paquete

def generate_initial_state(params,f=crear_solucio_inicial_baratescares) -> StateRepresentation:
    #comprovar que els paquets no pesin mes de 10
    for paq in params.l_paquetes:
        if paq.peso > 10:
            paq.peso = 10
    oferta_por_paquete = f(params.l_paquetes,params.l_ofertas)
    return StateRepresentation(params,oferta_por_paquete,0,1)



if __name__ == '__main__':
    npaq = int(input("Numero de paquetes: "))
    semilla = int(input("Semilla aleatoria: "))
    paquetes = random_paquetes(npaq, semilla)
    ofertas = random_ofertas(paquetes, 1.2, 1234)
    def execute():
        
        #inspeccionar_paquetes(paquetes)
        #inspeccionar_ofertas(ofertas)
        op_cambiar, op_swap = False, True
        parameters = ProblemParameters(paquetes,ofertas,0,op_cambiar,op_swap)
        estado_inicial = generate_initial_state(parameters)
        n = hill_climbing(AzamonProblem(estado_inicial))
        print("ASSIGNACIO FINAL:",n.assignacions)
        print("COST FINAL:", n.cost_calcular(), "FELICITAT FINAL: ",n.felicidad())
        print("num iteracions: ",n.contador)
        print()
        

    from timeit import timeit
    print("time is " ,timeit(execute,number=1))
    costes = [i[0] for i in iterations]
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(costes)), costes, marker='o', linestyle='-', color='b')
    #plt.plot(range(len(felicidades)), felicidades, marker='s', linestyle='--', color='r', label='Costes 2')
    plt.xlabel('Iteración (Paso)')
    plt.ylabel('Valor de la Coste')
    plt.title('Progreso de Hill Climbing')
    plt.grid(True)
    plt.show()
    

