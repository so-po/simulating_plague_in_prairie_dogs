from cProfile import Profile
from pstats import SortKey, Stats

import matplotlib
import matplotlib.pylab as plt
import math

from parameters import *
from eventstate import *

def run_simulation(max_days = 100):

    # ==== SET UP COMPARTMENTS: ====

    # host compartments:
    S = 200
    Ef = 0
    Ec = 0
    V = 0
    If = 0
    Ic = 0
    M = 0

    N = S+Ef+Ec+V+If+Ic

    # vector compartments:
    Fsq = 2500 
    Fsh = 1000
    Feq = 0
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

        F_0 = Fsh + Feh #total number of fleas that can reproduce
        find_host_rate = (1-(math.e**(-1*alpha*(N/B))))

        #TODO: rename these to have seperate names for host & fleas
        
        event_rates = [ # array of tuples, containing: (event rate, name of event)
            # HOST EVENTS
            (mu*S, 'Susceptible Death'),
            (mu*Ec, 'Infectious (Contact) Death'),
            (mu*Ef, 'Infectious (Flea) Death'),
            (mu*V, 'Vaccinated Death'),
            (zeta*M, 'Reservoir Decay'),
            (beta_c*((Ic+If)/N)*S, 'Susceptible Inf. (Contact)'),
            (beta_r*(M/B)*S, 'Susceptible Inf. (Reservoir)'),
            ((beta_f1*Fiq1+ beta_f2*Fiq2)*find_host_rate*S, 'Susceptible Inf. (Flea)'),
            (lmbda*V, 'Loss of Immunity'),
            (sigma*Ec, 'End of latency (Contact)'),
            (sigma*Ef, 'End of latency (Flea)'),
            (alpha*Ic,'Plague Death (Contact)'),
            (alpha*If, 'Plague Death (Flea)'),

            # VECTOR EVENTS
            
            # BIRTH
            (r_f*(N/(1+N+F_0))*F_0, 'Flea Birth'),

            # DEATH (NATURAL & PLAGUE):
            (mu_f*Fsq, 'Susceptible (Q) Death'),
            (mu_f*Fsh, 'Susceptible (H) Death'), 
            (mu_f*Feq, 'Infectious (Q) Death'), 
            (mu_f*Feh, 'Infectious (H) Death'), 

            (mu_f*Fiq1, 'Early Stage (Q) Death'), 
            (mu_f*Fih1, 'Early Stage (H) Death'),
            (s*Fiq1, 'Early Stage (Q) P.D.'),
            (s*Fih1, 'Early Stage (H) P.D.'),

            (mu_f*Fiq2, 'Late Stage (Q) Death'),
            (mu_f*Fih2, 'Late Stage (H) Death'),
            (s*Fiq2, 'Late Stage (Q) P.D.'),
            (s*Fih2, 'Late Stage (H) P.D.'),
            (delta*Fsh,'Susceptible Leaves Host'),
            (find_host_rate*Fsq, 'Susceptible Finds Host'),
            (gamma*Fsh*((Ic+If)/N), 'Susceptible Infected'),

            (delta*Feh, 'Infectious Leaves Host'),
            (find_host_rate*Feq, 'Infectious Finds Host'),

            (tau*Feh, 'End of Latency (H)'),
            (tau*Feq, 'End of Latency (Q)'),

            (delta*Fih1,'Early Stage Leaves Host'),
            (find_host_rate*Fiq1,'Early Stage, Finds Host'),

            (epsilon*Fih1, 'Grad. to Late Stage (H)'),
            (epsilon*Fiq1, 'Grad. to Late Stage (Q)'),

            (delta*Fih2, 'Late Stage Leaves Host'),
            (find_host_rate*Fiq2, 'Late Stage, Finds Host')
        ]

        
        if (t%365) >= 359: # the birth phase happens for 6 days at the end of every year (ignoring leap years)
            event_rates.append((r_tilde*(1-(N/K))*(S+V)*S, 'Host Birth'))
            #TODO: if during the birth phase the number of newborn pups exceeds 3.08 pups per female (sex ratio is about 1:2 males to females (Hoogland, 2013)) then r tilde is set to zero.

        event_rates = np.array(event_rates, dtype=np.dtype([('rate',np.float64),('event_name','U30')]))

        a0 = np.sum(event_rates['rate'])

        if a0 == 0:
            print("ENDING SIMULATION RUN: Rates of all events have reached zero.")
            break

        event_probabilities = event_rates['rate']/a0

        try:
            chosen_event = np.random.choice(event_rates['event_name'], 1, p=event_probabilities)
        except:
            print("ERROR: negative/incorrect probabilties")
            print(event_rates)
            print("Vector: ", Fsq, " ", Fsh, " ", Feq, " ", Feh, " ", Fiq1, " ", Fih1, " ", Fiq2, " ", Fih2)
            print("Host: ", S, " ", V, " ", Ec, " ", Ef, " ", Ic, " ", If, " ", M)

            break
        
        # ==== UPDATE TIME BASED ON a0: ====
        
        t += np.random.exponential(1 / a0) # numpy takes the scale = 1/rate

        if (t >= 365*h and Ic == 0): # introduce first infection after h years
            Ic = 1

        # ==== UPDATE POPULATION BASED ON EVENT : ====

        if chosen_event in host_event_names:

            host_compartment_updates = host_event_outcomes[host_event_names.index(chosen_event)] # S   V  Ec  Ef  Ic  If   M

            ss, vv, ec, ef, ic, i_f, m = host_compartment_updates
            S += ss
            V += vv
            Ec += ec
            Ef += ef
            Ic += ic
            If += i_f
            M += m
            
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
        
        else:
            raise Exception(f"ERROR: Event name DNE in vector or host list: {chosen_event}.")

        times.append(t)
        host_compartments.append([S, V, Ec, Ef, Ic, If, M])
        vector_compartments.append([Fsq, Fsh, Feq, Feh, Fiq1, Fih1, Fiq2, Fih2])
        
    return times, host_compartments, vector_compartments

# === PLOT ===
# TODO


# pr = Profile()
# pr.enable()

times, host_compartments, vector_compartments = run_simulation(365*11)

# pr.disable()
# pr.print_stats(sort='time')

host_compartments = np.array(host_compartments)

plt.plot(times, host_compartments[:, 0], label='S')
plt.plot(times, host_compartments[:, 4], label='If')
plt.plot(times, host_compartments[:, 5], label='Ic')
plt.plot(times, host_compartments[:, 6], label='M')
plt.xlabel('time (days)')
plt.ylabel('# of prairie dogs')
plt.legend()
plt.show()