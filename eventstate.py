import numpy as np
host = np.array([

    # S   V  Ec  Ef  Ic  If   M
    [+1,  0,  0,  0,  0,  0,  0],   # Birth
    [-1,  0,  0,  0,  0,  0,  0],   # Susceptible Death
    [ 0,  0, -1,  0,  0,  0,  0],   # Infectious (Contact) Death
    [ 0,  0,  0, -1,  0,  0,  0],   # Infectious (Flea) Death
    [ 0, -1,  0,  0,  0,  0,  0],   # Vaccinated Death
    [ 0,  0,  0,  0,  0,  0, -1],   # Reservoir Decay
    [-1,  0, +1,  0,  0,  0,  0],   # Susceptible Inf. (Contact)
    [-1,  0, +1,  0,  0,  0,  0],   # Susceptible Inf. (Reservoir)
    [-1,  0,  0, +1,  0,  0,  0],   # Susceptible Inf. (Flea)
    [+1, -1,  0,  0,  0,  0,  0],   # Loss of Immunity
    [ 0,  0, -1,  0, +1,  0,  0],   # End of latency (Contact)
    [ 0,  0,  0, -1,  0, +1,  0],   # End of latency (Flea)
    [ 0,  0,  0,  0, -1,  0, +1],   # Plague Death (Contact)
    [ 0,  0,  0,  0,  0, -1, +1],   # Plague Death (Flea)
])
host_event_names = ["Birth", "Susceptible Death", "Infectious (Contact) Death", 
               "Infectious (Flea) Death","Vaccinated Death","Reservoir Decay",
                "Susceptible Inf. (Contact)","Susceptible Inf. (Reservoir)",
                "Susceptible Inf. (Flea)", "Loss of Immunity","End of latency (Contact)",
                "End of latency (Flea)", "Plague Death (Contact)", "Plague Death (Flea)"]


vector = np.array([

    #F_SQ F_SH F_EQ F_EH F_IQ1 F_IH1 F_IQ2 F_IH2
    [ 1,   0,   0,   0,    0,    0,   0,    0], #Birth
    [-1,   0,   0,   0,    0,    0,   0,    0], #Susceptible (Q) Death
    [ 0,   -1,  0,   0,    0,    0,   0,    0], #Susceptible (H) Death
    [ 0,   0,  -1,   0,    0,    0,   0,    0], #Infectious (Q) Death
    [ 0,   0,   0,  -1,    0,    0,   0,    0], #Infectious (H) Death
    [ 0,   0,   0,   0,   -1,    0,   0,    0], #Early Stage (Q) Death
    [ 0,   0,   0,   0,    0,   -1,   0,    0], #Early Stage (H) Death
    [ 0,   0,   0,   0,   -1,    0,   0,    0], #Early Stage (Q) P.D.
    [ 0,   0,   0,   0,    0,   -1,   0,    0], #Early Stage (H) P.D.
    [ 0,   0,   0,   0,    0,    0,  -1,    0], #Late Stage (Q) Death
    [ 0,   0,   0,   0,    0,    0,   0,   -1], #Late Stage (H) Death
    [ 0,   0,   0,   0,    0,    0,  -1,    0], #Late Stage (Q) P.D.
    [ 0,   0,   0,   0,    0,    0,   0,   -1], #Late Stage (H) P.D.
    [+1,  -1,   0,   0,    0,    0,   0,    0], #Susceptible Leaves Host
    [-1,  +1,   0,   0,    0,    0,   0,    0], #Susceptible Finds Host
    [ 0,  -1,   0,  +1,    0,    0,   0,    0], #Susceptible Infected
    [ 0,   0,  +1,  -1,    0,    0,   0,    0], #Infectious Leaves Host
    [ 0,   0,  -1,  +1,    0,    0,   0,    0], #Infectious Finds Host
    [ 0,   0,   0,  -1,    0,   +1,   0,    0], #End of Latency (H)
    [ 0,   0,  -1,   0,   +1,    0,   0,    0], #End of Latency (Q)
    [ 0,   0,   0,   0,   +1,   -1,   0,    0], #Early Stage Leaves Host
    [ 0,   0,   0,   0,   -1,   +1,   0,    0], #Early Stage, Finds Host
    [ 0,   0,   0,   0,    0,   -1,   0,   +1], #Grad. to Late Stage (H)
    [ 0,   0,   0,   0,   -1,    0,  +1,    0], #Grad. to Late Stage (Q)
    [ 0,   0,   0,   0,    0,    0,  +1,   -1], #Late Stage Leaves Host
    [ 0,   0,   0,   0,    0,    0,  -1,   +1], #Late Stage, Finds Host
])

vector_event_names = [
    "Birth",
    "Susceptible (Q) Death",
    "Susceptible (H) Death",
    "Infectious (Q) Death",
    "Infectious (H) Death",
    "Early Stage (Q) Death",
    "Early Stage (H) Death",
    "Early Stage (Q) P.D.",
    "Early Stage (H) P.D.",
    "Late Stage (Q) Death",
    "Late Stage (H) Death",
    "Late Stage (Q) P.D.",
    "Late Stage (H) P.D.",
    "Susceptible Leaves Host",
    "Susceptible Finds Host",
    "Susceptible Infected",
    "Infectious Leaves Host",
    "Infectious Finds Host",
    "End of Latency (H)",
    "End of Latency (Q)",
    "Early Stage Leaves Host",
    "Early Stage, Finds Host",
    "Grad. to Late Stage (H)",
    "Grad. to Late Stage (Q)",
    "Late Stage Leaves Host",
    "Late Stage, Finds Host",
]