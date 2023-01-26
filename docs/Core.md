# Core Components

The core components of the library serve as the foundation for its capabilities. They are designed to be easily and quickly integrated, and follow specific guidelines to provide a solid base for further development.

Currently the core components include: [Actions](#Actions), [Steps](#Steps), [Policies](#Policies), [Strategies](#Strategies), [Conditions](#Conditions), and [Collectors](#Collectors).


## Core
The Core class manages the registration of new functions within the existing components.

**Requirements:**

- Every component needs to be available before a simulation starts
- Straightforward usage with decorator based registration
- Consistent and universal schema to store component functions

## Actions
The primary way an object interacts with the simulation. 

***For Example:*** 
A Dooder **moves** from one location to another. The action in this case is [move](https://github.com/csmangum/Dooders/blob/main/sdk/actions/move.py)

## Steps


## Policies


## Strategies


## Conditions


## Collectors

