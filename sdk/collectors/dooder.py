from sdk.core.collector import Collector

#! maybe special handling to explode if dict

@Collector.register('Stat')
def get_stats(simulation) -> dict:
  
  dooder_stats = []
  
  for dooder in simulation.society.active_dooders.values():
    dooder_stats.append(dooder.stats)
    
  return dooder_stats
