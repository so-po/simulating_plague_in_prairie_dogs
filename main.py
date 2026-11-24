import matplotlib
import matplotlib.pylab as plt

from parameters import *
from eventstate import *
from vector_submodel import * 
from host_submodel import *

def run_simulation(max_days = 500):

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

    t = 0 # time in days

    #keep track of values for graphing:
    vector_compartments = []
    host_compartments = []
    times = []

    while t <= max_days:
        N = S + Ef + Ec + V + If + Ic #recompute total hosts
        if (N == 0):
            print("ENDING SIMULATION RUN: Prairie dogs have gone extinct.")
            break

        # ==== CHOOSE EVENT : ====
        
        host_event_rates = get_host_events(S, V, M, Ec, Ef, Ic, If, N, Fiq1, Fiq2, t)   
        vector_event_rates = get_vector_events(Fsq, Fsh, Feq, Feh, Fiq1, Fih1, Fiq2, Fih2, Ic, If, N)

        event_rates = np.concatenate((host_event_rates, vector_event_rates), axis=0)

        a0 = np.sum(event_rates['rate'])

        if a0 == 0:
            print("ENDING SIMULATION RUN: Rates of all events have reached zero.")
            break

        event_probabilities = event_rates['rate']/a0

        try:
            chosen_event = np.random.choice(event_rates['event_name'], 1, p=event_probabilities)
        except:
            print("ERROR: negative/incorrect probabilties")
            # print(event_rates)
            break
        
        # ==== UPDATE TIME BASED ON a0: ====
        
        t += np.random.exponential(1 / a0) # numpy takes the scale = 1/rate

        # ==== UPDATE POPULATION BASED ON EVENT : ====

        if chosen_event in host_event_names:

            host_compartment_updates = host_event_outcomes[host_event_names.index(chosen_event)] # S   V  Ec  Ef  Ic  If   M

            s, v, ec, ef, ic, i_f, m = host_compartment_updates
            S += s
            V += v
            Ec += ec
            Ef += ef
            Ic += ic
            If += i_f
            M += m

            # print("Host: ", S, " ", V, " ", Ec, " ", Ef, " ", Ic, " ", If, " ", M)

        elif chosen_event in vector_event_names:

            vector_compartment_updates = vector_event_outcomes[vector_event_names.index(chosen_event)] #F_SQ F_SH F_EQ F_EH F_IQ1 F_IH1 F_IQ2 F_IH2

            fsq, fsh, feq, feh, fiq1, fih1, fiq2, fih2 = vector_compartment_updates
            Fsq += fsq
            Fsh += fsh
            Feq += feq
            Feh += feh
            Fiq1 += fiq1
            Fih1 += fih1
            Fiq2 += fiq2
            Fih2 += fih2

            #TODO: Bug w/ Fiq2 going below zero, causing negative rates. Need to investigate

            # print("Vector: ", Fsq, " ", Fsh, " ", Feq, " ", Feh, " ", Fiq1, " ", Fih1, " ", Fiq2, " ", Fih2)
        
        else:
            raise Exception(f"ERROR: Event name DNE in vector or host list: {chosen_event}.")

        times.append(t)
        host_compartments.append([S, V, Ec, Ef, Ic, If, M])
        vector_compartments.append([Fsq, Fsh, Feq, Feh, Fiq1, Fih1, Fiq2, Fih2])
        
    return times, host_compartments, vector_compartments

times, host_compartments, vector_compartments = run_simulation()

# === PLOT ===
# TODO

host_compartments = np.array(host_compartments)

plt.plot(times, host_compartments[:, 0], label='S')
plt.plot(times, host_compartments[:, 4], label='If')
plt.plot(times, host_compartments[:, 5], label='Ic')
plt.plot(times, host_compartments[:, 6], label='M')
plt.legend()
plt.show()