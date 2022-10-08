# SDK Structure
  
## Base

This folder contains the base-classes for the functionality of the library.  

## Collectors

All collectors are located in this folder. A collector is a class that is responsible for collecting data from a specific scope. Like from the Simulation, from a individual Dooder, etc.  

## Conditions

A condition is a function that returns a True or False value. This value is used to determine if a specific state has been reached (like Death). For example, if a Dooder is hungry, it needs to consume energy before it starves to death.  

## Core

Core classes for the plug-in design for Collectors, Strategies, and Conditions. This folder manages to core capabilities of the library.  

## Models

Contains functional representation of a system, like a Dooder, Society, Environment, etc..  
A model is the structural and conceptual representation of a system.  

## Modules

Contains the modules used in the various model, specifically with the Dooder agent model. An example of a future module is the Cognition model for a Dooder to make decisions.  

## Strategies

A strategy is a technique to provide an output. Usually a value or list of values. That output is used to determine an action or an input for another function.  
Some examples of strategies are the seed genetics of a simulation, the initial population of a simulation, the initial energy of a dooder, etc.  

## Utils

Contains utility classes and functions for the library.  
