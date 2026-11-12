
# ==== PARAMS THAT WE ADJUST: === 

# Ranges: (Stored as [min value, max value])
lmbda_range = [0, 1/270] #rate of immunity loss
v_range = [0, 0.99] #effective proportion of population vaccinated
d_range = [0.033, 0.092] #rate of insecticidal dusting
eta_range = [0, 0.99] #general culling proportion
h_range = [0, 5] #years of vaccination before disease arrival

# Values: (We need to set these)
lmbda = None
v = None
d = None
eta = None
h = None

# === CONSTANTS: === 

K = 200 #carrying capacity
r_tilde = 1.1605 #intrinsic rate of increase
mu = 1/(365*5) #natural mortality rate
beta_f1 = 14.625 #blocked vector early-stage transmission rate
beta_f2 = 0.09 #blocked vector late-stage transmission rate
beta_c = 0.073 #airborne transmission rate
beta_r = 0.0483 #reservoir transmission rate
B = 20 #number of burrows host enters
sigma = 0.21 #exposed period
alpha_f = 0.5 #blocked vector mortality rate
alpha_c = 0.5 #contact vector mortality rate 
zeta = 0.006 #reservoir decay rate
delta = 0.05 #rate of leaving hosts
alpha = 0.004 #searching efficiency of questing fleas
mu_f = 0.07 #natural mortality rate
r_f = 1.5 #conversion efficiency 
gamma = 0.28 #transmission rate: hosts to vector
tau = 0.009 #exposed_period
epsilon = 0.5 #graduation rate from early to late-stage
s = 0.33 #disease-induced mortality rate
