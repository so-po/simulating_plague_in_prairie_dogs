import matplotlib
import matplotlib.pylab as plt

from parameters import *
from eventstate import *
from vector_submodel import * 
from host_submodel import *

def run_simulation():

    # ==== SET UP COMPARTMENTS: ====

    # host compartments:
    S = 1000
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

    loops = 1000 # how many times to run the algo 
    t = 0 # time

    #keep track of values for graphing:
    vector_compartments = []
    host_compartments = []
    times = []

    for i in range(0, loops):

        if (N == 0):
            print("All hosts are dead. Ending loop")
            break

        # ==== CHOOSE EVENT : ====

        a0_host, host_event = host_choose_event(S, V, M, Ec, Ef, Ic, If, N, Fiq1, Fiq2)   
        a0_vector, vector_event = vector_choose_event(Fsq, Fsh, Feq, Feh, Fiq1, Fih1, Fiq2, Fih2, Ic, If, N)

        # TODO: BREAK if a_0 = 0 from either of these functions

        if a0_host == 0 or a0_vector == 0:
            break 

        # ==== UPDATE TIME ==== 

        # TODO: Draw τ ∼Exp(a0) and set t→t+ τ.
        
        a0 = a0_host + a0_vector
        placeholder_var = np.random.exponential(1 / a0)  # numpy takes the scale = 1/rate
        t += placeholder_var
        times.append(t)

        # ==== UPDATE POPULATION BASED ON EVENT : ====

        try:
            host_compartment_updates = host_event_outcomes[host_event_names.index(host_event)] # S   V  Ec  Ef  Ic  If   M
        except:
            raise Exception(f"ERROR: Host event DNE: {host_event}.")
        s, v, ec, ef, ic, i_f, m = host_compartment_updates
        S += s
        V += v
        Ec += ec
        Ef += ef
        Ic += ic
        If += i_f
        M += m
        #print("Host: ", S, " ", V, " ", Ec, " ", Ef, " ", Ic, " ", If, " ", M)
        host_compartments.append([S, V, Ec, Ef, Ic, If, M])


        try:
            vector_compartment_updates = vector_event_outcomes[vector_event_names.index(vector_event)] #F_SQ F_SH F_EQ F_EH F_IQ1 F_IH1 F_IQ2 F_IH2
        except:
            raise Exception(f"ERROR: Vector event DNE: {vector_event}.")
        fsq, fsh, feq, feh, fiq1, fih1, fiq2, fih2 = vector_compartment_updates
        Fsq += fsq
        Fsh += fsh
        Feq += feq
        Feh += feh
        Fiq1 += fiq1
        Fih1 += fih1
        Fiq2 += fiq2
        Fih2 += fih2
        #print("Vector: ", Fsq, " ", Fsh, " ", Feq, " ", Feh, " ", Fiq1, " ", Fih1, " ", Fiq2, " ", Fih2)
        vector_compartments.append([Fsq, Fsh, Feq, Feh, Fiq1, Fih1, Fiq2, Fih2])

    return times, host_compartments, vector_compartments

times, host_compartments, vector_compartments = run_simulation()

# === PLOT ===
# TODO

host_compartments = np.array(host_compartments)

plt.plot(times, host_compartments[:, 0], label='S')
plt.plot(times, host_compartments[:, 4], label='If')
plt.plot(times, host_compartments[:, 5], label='Ic')
plt.legend()
plt.show()