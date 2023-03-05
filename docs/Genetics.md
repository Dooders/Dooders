# Genetics

***This page is a work-in-progress*** 

The initial seed population is generated based on the selected genetic attributes and the strategies to populate the attributes. The [Genetics](Genetics.md) model serves as a way to establish starting values that can be mutable or immutable.  

For example, the starting energy value is determined at Dooder creation as the `energy_supply` attribute and changes cycle to cycle. Permanent values might be something like Metabolism which defines the rate a Dooder will starve with no new energy.  

A Dooder's behavior is an expression of both its genetics and environment. Some attributes can change over time, like the energy supply, while others can be immutable, like the metabolism.
