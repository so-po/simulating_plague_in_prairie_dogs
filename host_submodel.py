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


def get_host_events(S, V, M, Ec, Ef, Ic, If, N, Fiq1, Fiq2, day):
    # Run one step of the gillespie algorithm for the host submodel & return the state that will happen based on the rates of each event
    # Arguments: 
    # - S, V, M, Ec, Ef, Ic, If: # of prairie dogs in each host compartments
    # - Fiq1, Fiq2, : # of fleas in each vector compartment
    # - N: total # of hosts
    # - day: the time step in days since the simulation started (alters the birth rate)
    # Returns: A numpy array containing all events and their rates (w/ columns 'rate' and 'event_name')

    # ==== EVENTS : ==== 
    event_rates = [] # array of tuples, containing: (event rate, name of event)

    # CIRCLE BACK TO BIRTH
  
    if (day%365) >= 359: # the birth phase happens for 6 days at the end of every year (ignoring leap years)
        event_rates.append((r_tilde*(1-(N/K))*(S+V)*S, 'Host Birth'))
        #TODO: if during the birth phase the number of newborn pups exceeds 3.08 pups per female (sex ratio is about 1:2 males to females (Hoogland, 2013)) then r tilde is set to zero.
    event_rates.append((mu*S, 'Susceptible Death')) 
    event_rates.append((mu*Ec, 'Infectious (Contact) Death')) 
    event_rates.append((mu*Ef, 'Infectious (Flea) Death')) 
    event_rates.append((mu*V, 'Vaccinated Death')) 

    event_rates.append((mu*zeta, 'Reservoir Decay')) 

    event_rates.append((beta_c*((Ic+If)/N)*S, 'Susceptible Inf. (Contact)'))    
    event_rates.append((beta_r*(M/B)*S, 'Susceptible Inf. (Reservoir)'))    
    event_rates.append(((beta_f1*Fiq1+ beta_f2*Fiq2)*(1-math.e**(-alpha*(N/B)))*S, 'Susceptible Inf. (Flea)')) 

    event_rates.append((lmbda*V, 'Loss of Immunity')) 
    event_rates.append((sigma*Ec, 'End of latency (Contact)'))    
    event_rates.append((sigma*Ef, 'End of latency (Flea)'))    

    event_rates.append((alpha*Ic,'Plague Death (Contact)')) 
    event_rates.append((alpha*If, 'Plague Death (Flea)')) 
    
    event_rates = np.array(event_rates, dtype=np.dtype([('rate',np.float64),('event_name','U30')])) #format array
    return event_rates