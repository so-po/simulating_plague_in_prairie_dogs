from parameters import *
import math
import numpy as np
import random


# ==== KEY FOR VECTOR SUBMODEL COMPARTMENTS: ====
#   - S : susceptible
#   - V : vaccinated
#   - M : Reservoir 
#   - Ec : latency (Contact)
#   - Ef : latency (Flea)
#   - Ic : Plague (Contact)
#   - If : Plague (Flea)
# N : total pop of prarie dogs



def host_choose_event(S, V, M, Ec, Ef, Ic, If, N , Fiq1, Fiq2,a):
    # Run one step of the gillepsie algorithm for the vector submodel & return the state that will happen based on the rates of each event
    # Arguments: 
    # - Fiq1, Fiq2, : # of fleas in each compartment
    # - Ic, If: # of infected hosts, by contact and by fleas
    # - N: total # of hosts
    # Returns: A string representing the state that was randomly drawn

    # ==== EVENTS : ==== 
    event_rates = [] # array of tuples, containing: (event rate, name of event)

  
    # DEATH (NATURAL & PLAGUE):
    # CIRCEL BACK TO BIRTH
    event_rates.append((mu*S, 'Susceptible Death')) 
    event_rates.append((mu*Ec, 'Infectious (Contact) Death')) 
    event_rates.append((mu*Ef, 'Infectious (Flea) Death ')) 

    event_rates.append((mu*V, 'Vaccinated Death')) 
    event_rates.append((mu*zeta, 'Reservoir Decay')) 
    event_rates.append((beta_c*((Ic+If)/N)*S, 'Susceptible Inf. (Contact)'))    
    event_rates.append((beta_r*(M/B)*S, 'Susceptible Inf. (Reservoir)'))    

    event_rates.append(((beta_f1*Fiq1+ beta_f2*Fiq2)*(1-math.e**(-a*(N/B)))*S, 'Susceptible Inf. (Flea)')) 
    event_rates.append((lmbda*v, 'Loss of Immunity')) 
    event_rates.append((sigma*Ec, 'End of latency (Contact)'))    
    event_rates.append((sigma*Ef, 'End of latency (Flea)'))    

    event_rates.append((alpha*Ic,'Plague Death (Contact)')) 
    event_rates.append((alpha*If, 'Plague Death (Flea)')) 
    


    # ==== CHOOSE AN EVENT : ==== 

    event_rates = np.array(event_rates, dtype=np.dtype([('rate',np.float64),('event_name','U30')])) #format array

    # check that events can happen:
    a0 = np.sum(event_rates['rate']) # total of all rates
    if a0 == 0:
        return None

    #do a weighted random draw:
    event_probabilities = event_rates['rate']/a0
    chosen_event = np.random.choice(event_rates['event_name'], 1, p=event_probabilities) # TODO: is this weighted random draw equivalent to the gillespie algo's way of choosing things?
    
    return chosen_event[0]


## Test that it compiles:
# print(vector_choose_event(100, 200, 0, 0, 0, 0, 0, 0, 10, 1, 50))