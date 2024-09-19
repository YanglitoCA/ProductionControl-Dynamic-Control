import numpy as np
import pandas as pd

from stationaction import StateAction  # The full implementation of the StateAction class goes here...

# Example usage to initialize and run the value iteration
# Define system parameters
states = np.array([10, 3, 2])  # Example buffer capacities for 3 buffers (B_0, B_1, B_2)
statenum = 11 * 4 * 3  # Number of possible states in the system

# Define costs and rates
invc = 1  # Inventory holding cost (h')
rejoc = np.array([10, 20])  # Rejection cost per product (c^r)
unsatdc = np.array([30, 40])  # Unsatisfied order cost (c^d)
mu = 0.1  # Supply rate (μ)
lmd = np.array([0.03, 0.1])  # Order arrival rates (λ_i)
omg = np.array([0.1, 0.3])  # Order due rates (ω_i)
theta = 0.05  # Discount factor (θ)

# Initialize the StateAction object
state_action = StateAction(states, statenum, invc, rejoc, unsatdc, mu, lmd, omg, theta)

# Perform the value iteration
max_iterations = 100
tolerance = 1e-6
for i in range(max_iterations):
    delta = state_action.one_iteration()
    if delta < tolerance:
        print(f"Converged after {i + 1} iterations with delta: {delta}")
        break

# Collect the state vectors and values
data = []
for s in range(statenum):
    state_vector = state_action.number_to_state(s)
    value = state_action.value[s]
    controlact = state_action.control_decision(state_vector)
    data.append({
        'State': state_vector.tolist(),  # Convert numpy array to list for better readability in CSV
        'Value': value,
        'Control': controlact
    })

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('state_values.csv', index=False)

print("State vectors and values have been saved to 'state_values.csv'.")
