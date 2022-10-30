# looking to consume energy. max or min a goal, like survival days
# base goals: consume energy to maximize cycles, reproduce

class Survive:
  # input: needed data, dooder, goal
  # output: action and eval?
  # plugin like
  # get data from Information? -> apply policy to data and goal -> execute action or "recommend" action?
  # should policy just recomemd and not do execution? How to train then? policy waits for result? can i async a task that only continues if something happens?
  
  def __init__(self):
    pass
  
  
  # random, rule-based, NNs
  # maybe new dooders get a product of weights from parents.
  # genetic starting weights, learned weights. get product of that and those weights combine with another dooder during repro
  # genetic weights are a sequence of weights for other activities and policies. all can be contained in single array (with partitions)

  
  # maybe this recomemds to always be comsuming. it can be base policy that can be overcome/overpowered
  # weights that led to survive longer,
