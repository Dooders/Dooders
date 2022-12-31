from sdk.core.collector import Collector


@Collector.register('ActiveDooderCount')
def get_dooder_count(simulation) -> int:
    """Return the number of dooders in the simulation."""
    return simulation.society.active_dooder_count
