import datetime
from decimal import Decimal
from typing import List, NewType, Optional

from pydantic import BaseModel, Field

PointID = NewType("PointID", int)
DooderID = NewType("DooderID", int)

class Point(BaseModel):
    id: PointID
    loc: tuple
    neighbors: Optional[List[PointID]] = None


class Dooder(BaseModel):
    id: DooderID
    residing: Optional[PointID] = None