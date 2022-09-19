# Time

## Highlights

* Time model is responsible for executing and scheduling the cycle steps.
* Currently designed to distribute a schedule for each Object type (I.e., Dooder, Energy)
* User can state which object type to run. If no object type is provided, Time will run through each available object type randomly.
* Base class is important to require certain functionality built-in

Future iteration will have more advanced scheduling and executing

Like:

* Sorted by a metric (desc or asc)
* Distributed across a list of categories
* Ability to ignore an object based on logic

## Terminology

* Model - A system that is responsible for a specific task
* Cycle - Time period where all object actions happen (step by step)
* Step - A single action phase for any given object
* Object - Anything with “physical” placement or movement
* Dooder - Agent object
* Energy - Refers to both an energy object
* Energy Collection - a Dooders ability to make an action
