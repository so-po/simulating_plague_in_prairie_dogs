
host_event_outcomes = {
    # S   V  Ec  Ef  Ic  If   M
    "Host Birth": [+1,  0,  0,  0,  0,  0,  0],   # Birth
    "Susceptible Death": [-1,  0,  0,  0,  0,  0,  0],   # Susceptible Death
    "Infectious (Contact) Death": [ 0,  0, -1,  0,  0,  0,  0],   # Infectious (Contact) Death
    "Infectious (Flea) Death": [ 0,  0,  0, -1,  0,  0,  0],   # Infectious (Flea) Death
    "Vaccinated Death": [ 0, -1,  0,  0,  0,  0,  0],   # Vaccinated Death
    "Reservoir Decay": [ 0,  0,  0,  0,  0,  0, -1],   # Reservoir Decay
    "Susceptible Inf. (Contact)": [-1,  0, +1,  0,  0,  0,  0],   # Susceptible Inf. (Contact)
    "Susceptible Inf. (Reservoir)": [-1,  0, +1,  0,  0,  0,  0],   # Susceptible Inf. (Reservoir)
    "Susceptible Inf. (Flea)": [-1,  0,  0, +1,  0,  0,  0],   # Susceptible Inf. (Flea)
    "Loss of Immunity": [+1, -1,  0,  0,  0,  0,  0],   # Loss of Immunity
    "End of latency (Contact)": [ 0,  0, -1,  0, +1,  0,  0],   # End of latency (Contact)
    "End of latency (Flea)": [ 0,  0,  0, -1,  0, +1,  0],   # End of latency (Flea)
    "Plague Death (Contact)": [ 0,  0,  0,  0, -1,  0, +1],   # Plague Death (Contact)
    "Plague Death (Flea)": [ 0,  0,  0,  0,  0, -1, +1]   # Plague Death (Flea)
}

vector_event_outcomes = {
    #F_SQ F_SH F_EQ F_EH F_IQ1 F_IH1 F_IQ2 F_IH2
    "Flea Birth": [ 1,   0,   0,   0,    0,    0,   0,    0], #Flea Birth
    "Susceptible (Q) Death": [-1,   0,   0,   0,    0,    0,   0,    0], #Susceptible (Q) Death
    "Susceptible (H) Death": [ 0,   -1,  0,   0,    0,    0,   0,    0], #Susceptible (H) Death
    "Infectious (Q) Death": [ 0,   0,  -1,   0,    0,    0,   0,    0], #Infectious (Q) Death
    "Infectious (H) Death": [ 0,   0,   0,  -1,    0,    0,   0,    0], #Infectious (H) Death
    "Early Stage (Q) Death": [ 0,   0,   0,   0,   -1,    0,   0,    0], #Early Stage (Q) Death
    "Early Stage (H) Death": [ 0,   0,   0,   0,    0,   -1,   0,    0], #Early Stage (H) Death
    "Early Stage (Q) P.D.": [ 0,   0,   0,   0,   -1,    0,   0,    0], #Early Stage (Q) P.D.
    "Early Stage (H) P.D.": [ 0,   0,   0,   0,    0,   -1,   0,    0], #Early Stage (H) P.D.
    "Late Stage (Q) Death": [ 0,   0,   0,   0,    0,    0,  -1,    0], #Late Stage (Q) Death
    "Late Stage (H) Death": [ 0,   0,   0,   0,    0,    0,   0,   -1], #Late Stage (H) Death
    "Late Stage (Q) P.D.": [ 0,   0,   0,   0,    0,    0,  -1,    0], #Late Stage (Q) P.D.
    "Late Stage (H) P.D.": [ 0,   0,   0,   0,    0,    0,   0,   -1], #Late Stage (H) P.D.
    "Susceptible Leaves Host": [+1,  -1,   0,   0,    0,    0,   0,    0], #Susceptible Leaves Host
    "Susceptible Finds Host": [-1,  +1,   0,   0,    0,    0,   0,    0], #Susceptible Finds Host
    "Susceptible Infected": [ 0,  -1,   0,  +1,    0,    0,   0,    0], #Susceptible Infected
    "Infectious Leaves Host": [ 0,   0,  +1,  -1,    0,    0,   0,    0], #Infectious Leaves Host
    "Infectious Finds Host": [ 0,   0,  -1,  +1,    0,    0,   0,    0], #Infectious Finds Host
    "End of Latency (H)": [ 0,   0,   0,  -1,    0,   +1,   0,    0], #End of Latency (H)
    "End of Latency (Q)": [ 0,   0,  -1,   0,   +1,    0,   0,    0], #End of Latency (Q)
    "Early Stage Leaves Host": [ 0,   0,   0,   0,   +1,   -1,   0,    0], #Early Stage Leaves Host
    "Early Stage, Finds Host": [ 0,   0,   0,   0,   -1,   +1,   0,    0], #Early Stage, Finds Host
    "Grad. to Late Stage (H)": [ 0,   0,   0,   0,    0,   -1,   0,   +1], #Grad. to Late Stage (H)
    "Grad. to Late Stage (Q)": [ 0,   0,   0,   0,   -1,    0,  +1,    0], #Grad. to Late Stage (Q)
    "Late Stage Leaves Host": [ 0,   0,   0,   0,    0,    0,  +1,   -1], #Late Stage Leaves Host
    "Late Stage, Finds Host": [ 0,   0,   0,   0,    0,    0,  -1,   +1], #Late Stage, Finds Host
}