""" 
Dooder Collector
----------------
This collector is responsible for collecting the stats of all active dooders
"""

from sdk.core.collector import Collector

@Collector.register()
def dooder_stats(simulation) -> dict:
  """ 
  Collect the stats of all active dooders
  
  Parameters
  ----------
  simulation : Simulation
      The simulation to collect from
    
  Returns
  -------
  dict
      A dictionary of dooder stats
  """
  
  dooder_stats = []
  
  for dooder in simulation.society.active_dooders.values():
    dooder_stats.append(dooder.stats)
    
  return dooder_stats
