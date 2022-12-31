from sdk.core.collector import Collector


@Collector.register('ActiveDooderCount')
def get_dooder_count(simulation) -> int:
    """Return the number of dooders in the simulation."""
    return simulation.society.active_dooder_count

@Collector.register('TerminatedDooderCount')
def get_dooder_count(simulation) -> int:
    """Return the number of dooders in the simulation."""
    return simulation.society.dooders_died

@Collector.register('CreatedDooderCount')
def get_dooder_count(simulation) -> int:
    """Return the number of dooders in the simulation."""
    return simulation.society.dooders_created
