def cost_function_linear_version1(session_details, petrol_price, wear_and_tear_factor = 0.2, driver_discount=0.05):
    # By GMC, Translated by Sandeep.

    passengers = session_details['participants_list']
    driver = session_details['driver']
    passenger_count = len(passengers) #To determine the no:of passengers

    total_distance = driver_dist = session_details['distance']

    for user in session_details['passenger_dropoff_details']:
        itemvalue = list(user.values())[0]
        total_distance += itemvalue['distance']

    mileage = session_details['mileage']
    fuel_cost = (driver_dist/mileage)*petrol_price #Fuel cost
    
    total_cost = fuel_cost + (wear_and_tear_factor*fuel_cost) #Fuel + Wear and Tear
    
    driver_cost = ((1-(driver_discount)) * driver_dist/total_distance)*total_cost 
    
    dr_discnt = driver_discount * driver_cost / passenger_count
  
    session_details['cost_split'] = []
    for user in session_details['passenger_dropoff_details']:
        itemkey = list(user.keys())[0]
        itemvalue = list(user.values())[0]
        user_cost = {itemkey: (itemvalue['distance']/total_distance)*total_cost + dr_discnt }
        session_details['cost_split'].append(user_cost)
  
    session_details['cost_split'].append({driver: driver_cost})   # Add Driver to cost_split.
    
    cost_function_variables = {}
    cost_function_variables['total_cost'] = total_cost
    cost_function_variables['petrol_price'] = petrol_price
    cost_function_variables['mileage'] = mileage
    cost_function_variables['driver_discount'] = driver_discount
    cost_function_variables['wear_and_tear_factor'] = wear_and_tear_factor
    session_details['cost_function_variables'] = cost_function_variables

    return session_details
        
