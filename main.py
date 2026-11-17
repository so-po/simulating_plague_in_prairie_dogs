# Run submodels together & possibly load in parameters

from parameters import *
from eventstate import *
from vector_submodel import * 
from host_submodel import *

def main():

    # ==== SET UP COMPARTMENTS: ====

    # host compartments:
    S = 0
    Ef = 0
    Ec = 0
    V = 0
    If = 0
    Ic = 0
    M = 0

    N = S+Ef+Ec+V+If+Ic #TODO: double-check that this doesn't include M

    # vector compartments:
    Fsq = 0
    Fsh = 0
    Feq = 0
    Feh = 0
    Fiq1 = 0
    Fih1 = 0
    Fiq2 = 0
    Fih2 = 0

    loops = 20 # how many times to run the algo 
    t = 0 # time

    # ==== CHOOSE EVENT : ====

    for i in range(0, loops):
        # a0_host, host_event = host_choose_event(params) #TODO
        a0_vector, vector_event = vector_choose_event(Fsq, Fsh, Feq, Feh, Fiq1, Fih1, Fiq2, Fih2, Ic, If, N)

        # BREAK if a_0 = 0 from either of these functions

        # ==== UPDATE POPULATION BASED ON EVENT : ====

        # TODO: stoich[event_names.indexOf(host_event)] 


        # ==== UPDATE TIME ==== 

        # TODO: Draw τ ∼Exp(a0) and set t→t+ τ.

        # time_increment = 
        t = t + time_increment

        # === STORE COMPARTMENT VALUES (for plotting later) ===

        # TODO
      
    # === PLOT ===
    # TODO








