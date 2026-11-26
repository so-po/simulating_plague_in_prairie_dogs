from cProfile import Profile
from pstats import SortKey, Stats

import matplotlib
import matplotlib.pylab as plt
import math
import numpy as np

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

    new_pups_born = 0
    females_before_birth_phase = 0
    disease_introduced = False
    birth_phase_started = False

    while t <= max_days:
        N = S + Ef + Ec + V + If + Ic #recompute total hosts
        if (N == 0):
            print("ENDING SIMULATION RUN: Prairie dogs have gone extinct.")
            break


        # ==== CHOOSE EVENT : ====

        F_0 = Fsh + Feh #total number of fleas that can reproduce
        find_host_rate = (1-(math.e**(-1*a*(N/B))))

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
            if not birth_phase_started:
                #initialize birth variables: 
                # (birth is capped at 3.08 newborn pups per female):
                females_before_birth_phase = (S+V) * (2/3) #+V accounts for vacc females too. ratio of males to females is 1:2
                new_pups_born = 0
                birth_phase_started = True
            
            if females_before_birth_phase == 0 or (new_pups_born/females_before_birth_phase < max_new_pups_per_female):
                event_rates.append((r_tilde*max(0, 1-(N/K))*(S+V), 'Host Birth')) # max to prevent it from going below negative                  

        elif birth_phase_started: # exit birth phase
            birth_phase_started = False

            # susceptible prairie dogs get vaccinated:
            num_vaccinated = np.random.binomial(S, VE)
            V += num_vaccinated
            S -= num_vaccinated

            
        event_rates = np.array(event_rates, dtype=np.dtype([('rate',np.float64),('event_name','U30')]))

        a0 = np.sum(event_rates['rate'])

        if a0 == 0:
            print("ENDING SIMULATION RUN: Rates of all events have reached zero.")
            break

        event_probabilities = event_rates['rate']/a0

        chosen_event = ""
        try:
            chosen_event = np.random.choice(event_rates['event_name'], 1, p=event_probabilities)[0]
        except:
            print("ERROR: negative/incorrect probabilties")
            print(event_rates)
            print("Vector: ", Fsq, " ", Fsh, " ", Feq, " ", Feh, " ", Fiq1, " ", Fih1, " ", Fiq2, " ", Fih2)
            print("Host: ", S, " ", V, " ", Ec, " ", Ef, " ", Ic, " ", If, " ", M)

            break
        
        # ==== UPDATE TIME BASED ON a0: ====
        
        t += np.random.exponential(1 / a0) # numpy takes the scale = 1/rate

        if not disease_introduced and t >= 365*disease_arrival_year: #adding flag for disease introduction
            Ic += 1
            disease_introduced = True
        
        # ==== UPDATE POPULATION BASED ON EVENT : ====

        if chosen_event in host_event_outcomes.keys():

            host_compartment_updates = host_event_outcomes[chosen_event] # S   V  Ec  Ef  Ic  If   M

            ss, vv, ec, ef, ic, i_f, m = host_compartment_updates
            S += ss
            V += vv
            Ec += ec
            Ef += ef
            Ic += ic
            If += i_f
            M += m

            if chosen_event == "Host Birth": 
                new_pups_born += 1
            
        elif chosen_event in vector_event_outcomes.keys():

            vector_compartment_updates = vector_event_outcomes[chosen_event] #F_SQ F_SH F_EQ F_EH F_IQ1 F_IH1 F_IQ2 F_IH2

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

        N = S + Ef + Ec + V + If + Ic #recompute after update
        times.append(t)
        host_compartments.append([S, V, Ec, Ef, Ic, If, M, N])
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

# # PLOT OF HOST POPULATION:
# plt.title('host population')
# plt.plot(times, host_compartments[:, 7])
# plt.xlabel('time (days)')
# plt.ylabel('# of prairie dogs alive')
# plt.show()


# PLOT OF COMPARTMENTS: 
plt.title('host population per compartment')
plt.plot(times, host_compartments[:, 0], label='S')
plt.plot(times, host_compartments[:, 4], label='Ic')
plt.plot(times, host_compartments[:, 5], label='If')
plt.plot(times, host_compartments[:, 6], label='M')
# plt.plot(times, host_compartments[:, 1], label='V')
plt.xlabel('time (days)')
plt.ylabel('# of prairie dogs (per compartment)')
plt.legend()
plt.show()