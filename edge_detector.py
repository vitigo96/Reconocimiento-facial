import numpy as np
import pandas as pd
import sys


def find_steady_states_transients(dataframe, columns, noise_level,
                                  state_threshold, n=4):

    """
    Parameters
    ----------
    dataframe: dataframe with electrical variables used for disaggregation
    columns: headers of the dataframe (not including the time index)
    stateThreshold: maximum difference between highest and lowest
        value in steady state.
    noise_level: the level used to define significant
        appliances, transitions below this level will be ignored.
            
    Returns
    -------
    steady_states, transients : pd.DataFrame
    """
       
    steady_states_list = []
    transients_list = []
       
    power_dataframe = dataframe[columns].dropna()
    if power_dataframe.empty: 
        pass

    x, y = find_steady_states(
        power_dataframe, columns=columns, n=n, state_threshold=state_threshold, noise_level=noise_level)
    steady_states_list.append(x)
    transients_list.append(y)
    
    return [pd.concat(steady_states_list), pd.concat(transients_list)]


def find_steady_states(dataframe, columns, n_point = False, n=4, state_threshold=60,
                       noise_level=70):
    
    """Finds steady states given a DataFrame of power.
    The algorithm can take several columns but uses the active power (index 0) to detect the events
    
    Parameters
    ----------
    dataframe: dataframe with electrical variables used for disaggregation
    columns: headers of the dataframe (not including the time index)
    stateThreshold: maximum difference between highest and lowest
        value in steady state.
    noise_level: the level used to define significant
        appliances, transitions below this level will be ignored.
    n_point: for the real_time_disag algorithm. When this is True, function returns the transients and 
    steady_states dataframes but only the ones that appear in the nth position of the dataframe (which 
    has a short length, in order for the real_time_disag algorithm to work faster)

    Returns
    -------
    steady_states, transitions
    """
    num_measurements = len(dataframe.columns) 
    estimated_steady_power = np.array([0] * num_measurements)
    last_steady_power = np.array([0] * num_measurements)
    previous_measurement = np.array([0] * num_measurements)

    # These flags store state of power
    instantaneous_change = False  # power changing this second
    ongoing_change = False  # power change in progress over multiple seconds

    index_transitions = []  # Indices to use in returned Dataframe
    index_steady_states = []
    transitions = []  # holds information on transitions
    steady_states = []  # steadyStates to store in returned Dataframe
    N = 0  # N stores the number of samples in state
    time = dataframe.iloc[0].name  # first state starts at beginning
    
    # Iterate over the rows performing algorithm
    # print ("Finding Edges, please wait ...", end="\n")
    sys.stdout.flush()
    
    for row in dataframe[columns].itertuples():
        #Step 1
        this_measurement = row[1:len(columns)+1] 
        state_change = np.fabs(
            np.subtract(this_measurement[0], previous_measurement[0])) #Index 0 corresponds to active power

        #Step 2: Check if there is a change this last measurement
        if np.sum(state_change > state_threshold):
            instantaneous_change = True
        else:
            instantaneous_change = False
            
        # Step 3: Identify if transition is just starting, if so, process it
        if instantaneous_change and (not ongoing_change):
            # Calculate transition size
            last_transition = np.subtract(estimated_steady_power, last_steady_power)
            # Sum Boolean array to verify if transition is above noise level
            if np.sum(np.fabs(last_transition) > noise_level):
                # 3A, C: if so add the index of the transition start and the

                # Avoid outputting first transition from zero
                index_transitions.append(time)
                transitions.append(last_transition)
                index_steady_states.append(time)
                # last states steady power
                steady_states.append(estimated_steady_power)

            # 3B
            last_steady_power = estimated_steady_power
            # 3C
            time = row[0]
            
        # Step 4: if a new steady state is starting, zero counter
        if instantaneous_change:
            N = 0

        # Step 5: update our estimate for steady state's energy
        estimated_steady_power = np.divide(
            np.add(np.multiply(N, estimated_steady_power),
                   this_measurement), (N + 1))

        # Step 6: increment counter
        N += 1

        # Step 7: Update ongoing_change value
        ongoing_change = instantaneous_change

        # Step 8
        previous_measurement = this_measurement

    # Appending last edge
    last_transition = np.subtract(estimated_steady_power, last_steady_power)
    if np.sum(np.fabs(last_transition) > noise_level):
        index_transitions.append(time)
        transitions.append(last_transition)
        index_steady_states.append(time)
        steady_states.append(estimated_steady_power)
    
    if not steady_states:
        pass
    #Remove first edge if dataframe starts above noise level 
    elif np.sum(steady_states[0] > noise_level) and index_transitions[0] == index_steady_states[0] == dataframe[columns[0:1]].iloc[0].name:
        transitions = transitions[1:]
        index_transitions = index_transitions[1:]
        steady_states = steady_states[0:]
        index_steady_states = index_steady_states[0:]

    # print("Edge detection complete.")
    #print("Creating transition frame ...")
    sys.stdout.flush()
  
    if len(index_transitions) == 0:
        # No events
        return pd.DataFrame(), pd.DataFrame()
    else:
        transitions = pd.DataFrame(data=transitions, index=index_transitions,
                                   columns=columns)
        #print("Transition frame created.")
        #print("Creating states frame ...")
        sys.stdout.flush()
        steady_states = pd.DataFrame(data=steady_states, index=index_steady_states,
                                     columns=columns)
        # print("States frame created.")
        # print("Finished.")
    
    if n_point == True:
        #return transition and steady state only if it is detected at the position n of the dataframe
        steady_states = steady_states[steady_states.index == dataframe.iloc[n].name]
        transitions = transitions[transitions.index == dataframe.iloc[n].name]

    return steady_states, transitions