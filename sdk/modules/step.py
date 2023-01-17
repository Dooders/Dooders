# decide what step flow you want for each model
# allow for custom step flows
# step flow class sets up the requirements for a specific step flow
# encompasses the logic for a single step of the model
# will need to have things like, reaction and action phases
# every model can have a step method that can be custom

# one idea for a step flow:
# 1. Establish desire based on goals & current state
# 2. Predict next step to get the desire fulfilled
# 3. Keep predicting until desire is met
# 4. Go back to #1

# decorator to register step flows, stored in steps directory

#! are these different or the same? Step vs StepFlow
#! how do I make sure a new step logic meets some requirements?
#! step logic vs step flow vs step plan vs step process vs step method
#! also need a way to state which model a specific step flow is for

#! step plan could be the specific step flows to use for each model 
#! (from the greater step pool)

# a step is a point in the simulation to execute logic for a specific object 
# or model during its tern

from abc import ABC


class Step(ABC):
    """ 
    
    """
    pass

class StepFlow(ABC):
    pass