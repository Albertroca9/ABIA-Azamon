from typing import List
from abia_azamon import *
class ProblemParameters(object):
    def __init__(self, l_paquetes: List[Paquete], l_ofertas: List[Oferta], pond_felicitat= 0,op_cambiar=1, op_swap=1):
        self.l_paquetes = l_paquetes
        self.l_ofertas = l_ofertas
        self.pond_felicitat = pond_felicitat
        self.op_cambiar = op_cambiar
        self.op_swap = op_swap

    def __repr__(self):
        return f"Params(h_max={self.h_max}, v_h={self.v_h}, p_max={self.p_max}, c_max={self.c_max})"


def crear_asignacion_ordenada(l_paquetes, l_ofertas):
    # Función para crear una asignación de paquetes a ofertas
    # basada en la prioridad de cada paquete y la capacidad de cada oferta.
    print()
    def es_asignable(paquete, oferta):
        # Verifica que la prioridad del paquete coincida con los días de la oferta
        return not ((paquete.prioridad != 0 or oferta.dias != 1)
                    and (paquete.prioridad != 1 or oferta.dias != 2)
                    and (paquete.prioridad != 1 or oferta.dias != 3)
                    and (paquete.prioridad != 2 or oferta.dias != 4)
                    and (paquete.prioridad != 2 or oferta.dias != 5))

    # Lista para guardar la oferta asignada a cada paquete
    oferta_por_paquete = [-1] * len(l_paquetes)
    peso_por_oferta = [0.0] * len(l_ofertas)

    # Recorrer cada paquete y asignar a una oferta viable
    for id_paquete, paquete in enumerate(l_paquetes):
        for id_oferta, oferta in enumerate(l_ofertas):
            # Comprueba si la oferta es asignable al paquete
            if es_asignable(paquete, oferta):
                # Verifica si el peso del paquete cabe en la oferta sin exceder el límite
                if paquete.peso + peso_por_oferta[id_oferta] <= oferta.pesomax:
                    # Asigna el paquete a esta oferta y actualiza el peso acumulado
                    oferta_por_paquete[id_paquete] = id_oferta
                    peso_por_oferta[id_oferta] += paquete.peso
                    #print(f"Paq= {id_paquete} asignado a Env= {id_oferta}")
                    break  # Sale del bucle porque ya se ha asignado el paquete
        else:
            print(f"No se encontró oferta para Paq= {id_paquete} dentro de las restricciones.")
    
    """print()
    for id_paquete in range(len(l_paquetes)):
        print(f"Paq= {id_paquete} Env= {oferta_por_paquete[id_paquete]}"
              f" P= {l_paquetes[id_paquete].prioridad}"
              f" D= {l_ofertas[oferta_por_paquete[id_paquete]].dias if oferta_por_paquete[id_paquete] != -1 else 'N/A'}")
    for id_oferta in range(len(l_ofertas)):
        print(f"Env= {id_oferta}"
              f" Peso= {peso_por_oferta[id_oferta]}"
              f" PesoMax= {l_ofertas[id_oferta].pesomax}")
        if l_ofertas[id_oferta].pesomax < peso_por_oferta[id_oferta]:
            print("Esta situación no se debería dar. ¡Reportadlo!")
            raise RuntimeError("El peso total excede el máximo permitido para esta oferta.")
    """
    return oferta_por_paquete