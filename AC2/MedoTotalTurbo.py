
from MedoTotal import *

class MedoTotalTurbo(MedoTotal):

    def __init__(self, texto_input=mundoStandard):
        super().__init__(texto_input)

    def falha_antecipada(self, state):
        if state.medo < state.tempo:
            if state.pastilhas == set():
                return True

            #TODO

        return False