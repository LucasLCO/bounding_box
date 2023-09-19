from typing import List
from box import BoundingBox


class BoundingBoxes:
    def __init__(self, boxes) -> None:
        self.boxes = map(lambda x : BoundingBox(x), boxes)
        
        