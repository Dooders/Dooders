from sdk.core.collector import Collector


@Collector.register('AvailableEnergy')
def get_stats(simulation):

    return len(simulation.resources.available_resources)


@Collector.register('ConsumedEnergy')
def get_stats(simulation):

    return simulation.resources.consumed_energy


@Collector.register('AllocatedEnergy')
def get_stats(simulation):

    return simulation.resources.allocated_energy


@Collector.register('DissipatedEnergy')
def get_stats(simulation):

    return simulation.resources.dissipated_energy
