Optimal Production and Order Control in Multi-Product Systems

This repository contains Python code for simulating and optimizing production and order control policies in a multi-product supply chain. The project models a system using a Markov Decision Process (MDP) to minimize operational costs associated with production, inventory, and order management.

Introduction

This project simulates an assembly-to-order (ATO) production system where a manufacturer receives parts from a supplier and assembles products based on customer orders. The system aims to minimize costs associated with inventory holding, rejected orders, unsatisfied demand, and production. By using an MDP framework, it identifies optimal policies for:

Ordering parts from a supplier.
Accepting or rejecting customer orders.
Scheduling order fulfillment based on the system's current state.

Features

Markov Decision Process (MDP): Models optimal decisions for production and order management.
Value Iteration Algorithm: Efficiently solves the MDP to determine optimal policies.
Simulation: Runs simulations over a given time horizon to evaluate system performance and calculate total costs and profits.
Dynamic Control Policies: Generates control decisions based on system states, buffer capacities, and incoming order rates.
CSV Output: Saves simulation results, including state vectors and control actions, to CSV files for analysis.
Project Structure
graphql
Copy code
.
├── main.py           # Main simulation script
├── example.py        # Example usage of the StateAction class
├── stationaction.py  # Contains the StateAction class for state and control logic
├── state_values.csv  # Outputs state values from value iteration (generated)
└── simulation_results.csv  # Outputs simulation results (generated)
main.py
This is the main script that sets up the parameters for the production system, runs the value iteration, and simulates the system over a specified time period. It saves the results to CSV files.

example.py
This file provides an example of how to use the StateAction class to initialize system parameters and run the value iteration algorithm.

stationaction.py
Contains the StateAction class, which handles all the state transitions, value calculations, and control decisions for the MDP-based system.

Installation
Clone the repository:
bash
Copy code
git clone https://github.com/yourusername/multi-product-production-control.git
Install the required dependencies:
bash
Copy code
pip install -r requirements.txt
Dependencies include:
numpy
pandas
Usage
Modify the system parameters in main.py to fit your production system.
Run the simulation:
bash
Copy code
python main.py
Check the results in the state_values.csv and simulation_results.csv files.
Example Execution
bash
Copy code
python example.py
This will run a small test with predefined parameters and output the results of the value iteration to state_values.csv.

Parameters
The system is governed by several key parameters, which can be adjusted in main.py and example.py:

states: An array representing the capacities of the buffers in the system (e.g., [10, 5, 5] for three buffers).
statenum: The total number of possible states in the system.
invc: Inventory holding cost per unit.
rejoc: Rejection cost for orders that cannot be accepted.
unsatdc: Cost of unsatisfied demand.
mu: Supply rate for incoming parts from the supplier.
lmd: Order arrival rates for different products.
omg: Rates at which orders become due.
theta: Discount factor for future costs.
price: The revenue per fulfilled order for each product.
Simulation Results
The simulation outputs two CSV files:

state_values.csv: Contains state vectors, their corresponding values, and the control decisions from the value iteration process.
simulation_results.csv: Logs each iteration of the simulation, showing the current state, control actions, overall cost, and overall profit.
You can analyze these results to evaluate system performance under different parameter settings.
