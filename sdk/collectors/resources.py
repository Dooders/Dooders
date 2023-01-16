from sdk.core.collector import Collector


@Collector.register()
def available_energy(simulation):

    return len(simulation.resources.available_resources)


@Collector.register()
def consumed_energy(simulation):

    return simulation.resources.consumed_energy


@Collector.register()
def allocated_energy(simulation):

    return simulation.resources.allocated_energy