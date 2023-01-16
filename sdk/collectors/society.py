from sdk.core.collector import Collector


@Collector.register()
def active_dooder_count(simulation) -> int:
    """Return the number of dooders in the simulation."""
    return simulation.society.active_dooder_count

@Collector.register()
def terminated_dooder_count(simulation) -> int:
    """Return the number of dooders in the simulation."""
    return simulation.society.dooders_died

@Collector.register()
def created_dooder_count(simulation) -> int:
    """Return the number of dooders in the simulation."""
    return simulation.society.dooders_created
