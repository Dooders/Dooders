

class Location:
  
  contents = {}
  
  def __init__(self, coordinate):
    self.coordinate = coordinate
    self.x = self.coordinate[0]
    self.y = self.coordinate[1]
    
    
   def __str__(self):
      return self.coordinate
