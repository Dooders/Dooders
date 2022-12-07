# Development Diary

A space to log what I've been working in and thinking. That will help look back and remember why I made certain decisions or chose to take a specific path.

Sorted by the most recent entry

---

## 2022-12-05 Building out the Dooder step process

I'm first going to create a custom dictionary class to handle the internal models. That way I can easily access the weights and biases of every model

Then I'm going to update the movement policy to be goal-based. The goal will be inferred by the Dooder's state.

## 2022-12-04: Managing multiple learning models

Right now I'm working out the best design to manage multiple learning models. Currently a Dooder only has a model to determine where to move (saved as a class attribute called internal_models). I'll be adding many more models going further so I need a consistent design.

A simple dictionary may be enough, but I want to think through it a bit more before taking that route.

I'm also thinking about better ways to "collect" data during a simulation. Something that can be easily changed to collect the specific data I want. I'll be adding a lot of data-points to the simulation and I want to be able to easily change what data is collected.
