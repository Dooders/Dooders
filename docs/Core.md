# Core Components

The core components provide the foundational capabilities of the library. These components are designed to be added to easily and quickly, and follow specific designs to allow for a base to build off of.

Currently the core components include: [Actions](#Actions), [Steps](#Steps), [Policies](#Policies), [Strategies](#Strategies), [Conditions](#Conditions), and [Collectors](#Collectors).

These components are managed by a Core class that handles registration of new functions inside the existing components

**Component Requirements:**

- Components dictionary needs to be available before a simulation starts
- Easy extension with new component classes and functions
- Easy usage of components in the code
- Consistent and universal schema

## Actions
The primary way an object interacts with the simulation. 
***For Example:*** A Dooder **moves** from one location to another. The action in this case is [Move](https://github.com/csmangum/Dooders/blob/main/sdk/actions/move.py)

## Steps


## Policies


## Strategies


## Conditions


## Collectors

