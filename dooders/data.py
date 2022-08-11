from pydantic import BaseModel


class DirectionCountDict(BaseModel):
    N: int = 0
    NE: int = 0
    E: int = 0
    SE: int = 0
    S: int = 0
    SW: int = 0
    W: int = 0
    NW: int = 0


class ExperimentResults(BaseModel):
    """
    Results of the simulation.
    The main output of the simulation sent via websocket.
    """
    StepNumber: int
    AgentCount: int
    DirectionCount: DirectionCountDict


def direction_counts(model) -> DirectionCountDict:
    """
    Count the number of times each direction is chosen.
    The count is accumulated across all agents.
    Function executes at the end of each step.

    Purpose:
        Keep track of the distribution of directions.

    Args:
        model: Simulation model.

    Returns:
        A dictionary mapping direction to count.
    """
    from collections import Counter
    direction_list = model.datacollector.get_agent_vars_dataframe()[
        'Direction'].tolist()
    direction_counts = Counter(direction_list)
    final_direction_counts = DirectionCountDict(**direction_counts)

    return final_direction_counts


def results(model) -> ExperimentResults:
    """
    Rollup the results of the simulation.
    Function executes at the end of each step.

    Args:
        model: Simulation model.

    Returns:
        A dictionary of results.
    """
    results = {
        'StepNumber': model.schedule.steps,
        'AgentCount': model.schedule.get_agent_count(),
        'DirectionCount': direction_counts(model)}
    return results