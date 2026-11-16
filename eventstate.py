
stoich = np.array([

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
event_names = ["Birth", "Susceptible Death", "Infectious (Contact) Death", 
               "Infectious (Flea) Death","Vaccinated Death","Reservoir Decay",
                "Susceptible Inf. (Contact)","Susceptible Inf. (Reservoir)",
                "Susceptible Inf. (Flea)", "Loss of Immunity","End of latency (Contact)",
                "End of latency (Flea)", "Plague Death (Contact)", "Plague Death (Flea)"]
