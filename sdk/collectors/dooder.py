""" 
Dooder Collector
----------------
This collector is responsible for collecting the stats of all active dooders
"""

from sdk.core.core import Core

@Core.register('collector')
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
  
  for dooder in simulation.arena.active_dooders.values():
    dooder_stats.append(dooder.stats.dict())
    
  return dooder_stats
