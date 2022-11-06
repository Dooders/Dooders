# Hunger

* Hunger will be set to 0 when the Dooder is created  
* During a step, if the dooder didn't consume energy, hunger increases by 1  
* If Dooder comsumes energy, hunger resets to 0  
* If hunger was already 0, then hunger is decreased by 1, to a limit  
* This way a Dooder can store some energy.  
* when hunger reaches a determined number, the Dooder dies. or each hunger level, the probability of dying increases  


hunger mean probabilities:  

hunger = 1 --> prob_mean = 5%  
hunger = 2 --> prob_mean = 10%  
hunger = 3 --> prob_mean = 20%  
hunger = 4 --> prob_mean = 50%  
hunger = 5 --> prob_mean = 75%  
hunger > 5 --> prob_mean = 99%  
