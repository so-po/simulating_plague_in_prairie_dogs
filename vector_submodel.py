from parameters import *
import math
import numpy as np
import random


# TODO: 
# - update states to be the correct names

# KEY FOR VECTOR SUBMODEL COMPARTMENTS: 
# - Fsq : susceptible and questing
# - Fsh : susceptible and on-host
# - Feq : infected and questing
# - Feh : infected and questing
# - Fiq1 : early-stage infectious and questing
# - Fih1 : early-stage infectious and on-host
# - Fiq2 : late-stage infectious and questing
# - Fih2 : late-stage infectious and on-host
#
# Number of fleas that can reproduce = # of noninfectious, on-host fleas (Fsh + Feh)


def vector_choose_event(Fsq, Fsh, Feq, Feh, Fiq1, Fih1, Fiq2, Fih2, Ic, If, N):
    # Run one step of the gillepsie algorithm for the vector submodel & return the state that will happen based on the rates of each event
    # Arguments: 
    # - Fsq, Fsh, Feq, Feh, Fiq1, Fih1, Fiq2, Fih2: # of fleas in each compartment
    # - Ic, If: # of infected hosts, by contact and by fleas
    # - N: total # of hosts
    # Returns: A string representing the state that was randomly drawn

    # ==== KEY : ====
    # s = suseptible
    # e = exposed (infected)
    # i1 = infectious, early stage
    # i2 = infectious, late stage

    # q = questing
    # h = on host

    # ==== EVENTS : ==== 
    event_rates = [] # array of arrays, containing: [event rate, name of event]

    # BIRTH
    F_0 = Fsh + Feh #total number of fleas that can reproduce
    event_rates.append([r_f*(N/(1+N+F_0))*F_0, 'Birth'])

    # DEATH (NATURAL & PLAGUE):
    event_rates.append([mu_f*Fsq, 'Susceptible (Q) Death']) # s q natural death
    event_rates.append([mu_f*Fsh, 'Susceptible (H) Death']) # s h natural death
    event_rates.append([mu_f*Feq, 'Infectious (Q) Death']) # e q natural death
    event_rates.append([mu_f*Feh, 'Infectious (H) Death']) # e h natural death

    event_rates.append([mu_f*Fiq1, 'Early Stage (Q) Death']) # i q 1 natural death
    event_rates.append([mu_f*Fih1, 'Early Stage (H) Death']) # i h 1 natural death
    event_rates.append([s*Fiq1, 'Early Stage (Q) P.D.'])    # i q 1 plague death
    event_rates.append([s*Fih1, 'Early Stage (H) P.D.'])    # i h 1 plague death

    event_rates.append([mu_f*Fiq2, 'Late Stage (Q) Death']) # i q 2 natural death
    event_rates.append([mu_f*Fih2, 'Late Stage (H) Death']) # i h 2 natural death
    event_rates.append([s*Fiq2, 'Late Stage (Q) P.D.'])    # i q 2 plague death
    event_rates.append([s*Fih2, 'Late Stage (H) P.D.'])    # i h 2 plague death

    # MOVEMENT ONTO & OFF OF HOSTS AND INFECTION PROGRESSION:
    find_host_rate = (1-(math.e**(-1*alpha*(N/B))))

    event_rates.append([delta*Fsh,'Susceptible Leaves Host']) # s leaves host
    event_rates.append([find_host_rate*Fsq, 'Susceptible Finds Host']) # s finds host
    event_rates.append([gamma*Fsh*((Ic+If)/N), 'Susceptible Infected']) # s gets infected

    event_rates.append([delta*Feh, 'Infectious Leaves Host']) # e leaves host
    event_rates.append([find_host_rate*Feq, 'Infectious Finds Host']) # e finds host

    event_rates.append([tau*Feh, 'End of Latency (H)']) # e h -> i1 h (end of latency, exposed becomes infectious)
    event_rates.append([tau*Feq, 'End of Latency (Q)']) # e q -> i1 q (end of latency, exposed becomes infectious)

    event_rates.append([delta*Fih1,'Early Stage Leaves Host']) # i1 leaves host
    event_rates.append([find_host_rate*Fiq1,'Early Stage, Finds Host']) # i1 finds host

    event_rates.append([epsilon*Fih1, 'Grad. to Late Stage (H)']) # i1 h -> i2 h (graduate to late state infectiousness)
    event_rates.append([epsilon*Fiq1, 'Grad. to Late Stage (Q)']) # i1 v -> i2 v (graduate to late state infectiousness)

    event_rates.append([delta*Fih2, 'Late Stage Leaves Host']) # i2 leaves host
    event_rates.append([find_host_rate*Fih2, 'Late Stage, Finds Host']) # i2 finds host


    # ==== CHOOSE AN EVENT : ==== 

    event_rates = np.array(event_rates, dtype=np.dtype([('rate',np.float64),('event_name',np.str_)]))

    print(event_rates[:, 0][0])
    a0 = np.sum(event_rates[:, 0]) # total of all rates

    if a0 == 0:
        return None

    #weighted random draw:
    chosen_event = np.choice(event_rates[:, 0], 1, event_rates[:, 1]) # TODO: is this weighted random draw equivalent to the gillespie algo's way of choosing things?
    
    return chosen_event


# Test that it compiles:
vector_choose_event(100, 0, 0, 0, 0, 0, 0, 0, 1, 1, 10)