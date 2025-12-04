class AzamonOperator(object):
    pass


class CambiarOferta(AzamonOperator):
    def __init__(self, p_i: int, oferta_j: int, oferta_k: int):
        self.p_i = p_i
        self.oferta_j = oferta_j
        self.oferta_k = oferta_k

    def __repr__(self) -> str:
        return f"Change package {self.p_i} from oferta {self.c_j} to oferta {self.c_k}"


class SwapParcels(AzamonOperator):
    def __init__(self, p_i: int, p_j: int):
        self.p_i = p_i
        self.p_j = p_j

    def __repr__(self) -> str:
        return f"Swap parcels {self.p_i} and {self.p_j}"
