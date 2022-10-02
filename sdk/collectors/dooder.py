from sdk.core.collector import Collector

@Collector.register('DooderStats')
def get_stats(simulation):
  
  dooder_stats = []
  
  for dooder in simulation.society.active_dooders.values():
    dooder_stats.append(dooder.stats)
    
  return dooder_stats
