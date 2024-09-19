import numpy as np
import pandas as pd

from stationaction import StateAction

def simulation(states, statenum, invc, rejoc, unsatdc, mu, lmd, omg, theta, initialstate, price):
    # Initialize the StateAction object
    state_action = StateAction(states, statenum, invc, rejoc, unsatdc, mu, lmd, omg, theta)
    # Perform the value iteration
    max_iterations = 10000
    tolerance = 1e-6
    for i in range(max_iterations):
        delta = state_action.one_iteration()
        if delta < tolerance:
            print(f"Converged after {i + 1} iterations with delta: {delta}")
            break
    # Collect the state vectors and values
    data0 = []
    for s in range(statenum):
        state_vector = state_action.number_to_state(s)
        value = state_action.value[s]
        controlact = state_action.control_decision(state_vector)
        data0.append({
            'State': state_vector.tolist(),  # Convert numpy array to list for better readability in CSV
            'Value': value,
            'Control': controlact
        })

    # Convert to DataFrame
    df = pd.DataFrame(data0)

    # Save to CSV
    df.to_csv('state_values.csv', index=False)

    # Collect data for CSV output
    data = []

    # simulation part
    simulationtime = 100
    overallcost = 0
    overallprofit = 0
    currentstate = initialstate.copy()  # Copy initial state to avoid modifying the original

    #random events variables
    awt = np.exp(-1/mu) #the average lead time for the production order to come

    # Simulation loop
    for i in range(simulationtime):
        control = state_action.control_decision(currentstate)
        for j in range(len(price)):
            event_occurs = np.random.rand() < lmd[j]
            #print(1, j, event_occurs)
            if event_occurs: # when an order comes
                if control[j + 1] == 0 and currentstate[j + 1] < states[j + 1]:  # accept an incoming order for each category
                    currentstate[j + 1] += 1
                else:  # reject an incoming order
                    overallcost += rejoc[j]

            event_occurs = np.random.rand() < np.exp(-1/(omg[j]*currentstate[j+1]))
            #print(2, j, event_occurs)
            if event_occurs: # if an order becomes due
                if control[len(states) + j - 1] == 1:
                    if currentstate[0] > 0 and currentstate[j + 1] > 0:  # satisfy the order
                        currentstate[0] -= 1
                        currentstate[j + 1] -= 1
                        overallprofit += price[j]
                    else:  # do not satisfy the order
                        overallcost += unsatdc[j]
                else:
                    overallcost += unsatdc[j]

        event_occurs = np.random.rand() < awt
        #print(3, event_occurs)
        if event_occurs:
            currentstate[0] = control[0]  # state change of b_0 after control
        overallcost += currentstate[0] * invc

        # Collect data for the current state, including 'control'
        data.append({
            'Iteration': i + 1,
            'State': currentstate.copy(),
            'Control': control.tolist(),  # Store control as a list
            'OverallCost': overallcost,
            'OverallProfit': overallprofit
        })

    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Save DataFrame to CSV
    df.to_csv('simulation_results.csv', index=False)

    #print(f"The overall cost is {overallcost}")
    #print(f"The overall profit is {overallprofit}")

    return overallcost, overallprofit


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Define system parameters
    states = np.array([10, 5, 5])  # Example buffer capacities for 3 buffers (B_0, B_1, B_2)
    statenum = 11 * 6 * 6  # Number of possible states in the system

    # Define costs and rates
    invc = 5  # Inventory holding cost (h')
    rejoc = np.array([20, 30])  # Rejection cost per product (c^r)
    unsatdc = np.array([30, 40])  # Unsatisfied order cost (c^d)
    mu = 0.3  # Supply rate (μ)
    lmd = np.array([0.5, 0.4])  # Order arrival rates (λ_i)
    omg = np.array([0.2, 0.3])  # Order due rates (ω_i)
    theta = 0.05  # Discount factor (θ)
    price = np.array([100, 120])
    initialstate = np.array([1, 1, 1])
    result1, result2 = simulation(states, statenum, invc, rejoc, unsatdc, mu, lmd, omg, theta, initialstate, price)

    print(result1, result2)