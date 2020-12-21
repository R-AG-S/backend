def cost_funcn(memberdetails,mileage,petrol_price):
    
    denominator = 0 #To calculate the ratio
    
    pax = 0 #To determine the no:of passengers
    
    driver_dist = 0 #To determine distance travelled by the driver
    
    wear_and_tear_factor = 0.2 # 20% extra for wear and tear
    
    for user in memberdetails:
        
        denominator += user['distance']
        
        if isdriver(user): #REPLACE WITH FUNCTION TO DETERMINE DRIVER
            
            driver_dist = user['distance']
            
        else:
            pax += 1
            
            
    
    fuel_cost = (driver_dist/mileage)*petrol_price #Fuel cost
    
    total_cost = fuel_cost + (wear_and_tear_factor*fuel_cost) #Fuel + Wear and Tear
    
    dr_discnt = 0 #Driver Discount (calculated below)
        
        
        
    
    for user in memberdetails:
        
        user['cost'] = (user['distance']/denominator)*total_cost
        
        
        if isdriver(user):
            
            dr_discnt = 0.05 * user['cost'] #5% discount for driver
            
            user['cost'] -= dr_discnt
            
    
    dr_discnt = dr_discnt/pax #Splitting driver discount among passengers
    
    
    for user in memberdetails:
        
        if isdriver(user) == false:
            
            user['cost'] += dr_discnt
        
