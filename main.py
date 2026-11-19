# Run submodels together & possibly load in parameters

from parameters import *
from eventstate import *
from vector_submodel import * 
from host_submodel import *

def main():

    # ==== SET UP COMPARTMENTS: ====

    # host compartments:
    S = 1
    Ef = 0
    Ec = 0
    V = 0
    If = 0
    Ic = 0
    M = 0

    N = S+Ef+Ec+V+If+Ic #TODO: double-check that this doesn't include M

    # vector compartments:
    Fsq = 100
    Fsh = 0
    Feq = 100
    Feh = 0
    Fiq1 = 0
    Fih1 = 0
    Fiq2 = 0
    Fih2 = 0

    loops = 20 # how many times to run the algo 
    t = 0 # time

    # ==== CHOOSE EVENT : ====



    for i in range(0, loops):

        if (N == 0):
            print("All hosts are dead. Ending loop")
            break

        a0_host, host_event = host_choose_event(S, V, M, Ec, Ef, Ic, If, N, Fiq1, Fiq2)   
        a0_vector, vector_event = vector_choose_event(Fsq, Fsh, Feq, Feh, Fiq1, Fih1, Fiq2, Fih2, Ic, If, N)

        # TODO: BREAK if a_0 = 0 from either of these functions

        # ==== UPDATE TIME ==== 

        # TODO: Draw τ ∼Exp(a0) and set t→t+ τ.

        # time_increment = 
        #t = t + time_increment

        # ==== UPDATE POPULATION BASED ON EVENT : ====

        host_compartment_updates = host_event_outcomes[host_event_names.index(host_event)] # S   V  Ec  Ef  Ic  If   M
        s, v, ec, ef, ic, i_f, m = host_compartment_updates
        S += s
        V += v
        Ec += ec
        Ef += ef
        Ic += ic
        If += i_f
        M += m
        print("Host: ", S, " ", V, " ", Ec, " ", Ef, " ", Ic, " ", If, " ", M)

        vector_compartment_updates = vector_event_outcomes[vector_event_names.index(vector_event)] #F_SQ F_SH F_EQ F_EH F_IQ1 F_IH1 F_IQ2 F_IH2

        fsq, fsh, feq, feh, fiq1, fih1, fiq2, fih2 = vector_compartment_updates
        Fsq += fsq
        Fsh += fsh
        Feq += feq
        Feh += feh
        Fiq1 += fiq1
        Fih1 += fih1
        Fiq2 += fiq2
        Fih2 += fih2
        print("Vector: ", Fsq, " ", Fsh, " ", Feq, " ", Feh, " ", Fiq1, " ", Fih1, " ", Fiq2, " ", Fih2)


        # === STORE COMPARTMENT VALUES (for plotting later) ===

        # TODO
      
    # === PLOT ===
    # TODO

main()
