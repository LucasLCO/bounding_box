import numpy as np
import numpy.typing as npt
from typing import Optional, List, Union, Sequence, Dict


class BoundingBox:
    box_type = Union[Sequence[Union[float, int]], npt.NDArray[Union[np.float64, np.int64]]]

    def __init__(self, bounding_box:box_type) -> None:
        self.bounding_box = self.separate_max_min(bounding_box)
        self.middle = self.find_middle(self.bounding_box)
        self.dimensions = self.find_dimensions(self.bounding_box)
        self.area = self.dimensions["width"] * self.dimensions["height"]

    def reload_init(self, bounding_box:box_type) -> None:
        self.bounding_box = self.separate_max_min(bounding_box)
        self.middle = self.find_middle(self.bounding_box)
        self.dimensions = self.find_dimensions(self.bounding_box)
        self.area = self.dimensions["width"] * self.dimensions["height"]
        
    @staticmethod
    def separate_max_min(box: box_type)->Dict[str, int]:
        """
            Separate the box by its maxs and mins (in x, y).

            Parameterss
            -----------
                box: dict
                    parking space bounding box (values stored in coord.json).

            Output
            ------
                middle: dict
                    dict obtaining x 
        
        """
        
        separeted_box = {}
        separeted_box["xmin"] = min(box[0], box[2])
        separeted_box["ymin"] = min(box[1], box[3])
        separeted_box["xmax"] = max(box[0], box[2])
        separeted_box["ymax"] = max(box[1], box[3])

        return separeted_box

    @staticmethod
    def find_middle(separeted_box:Dict[str, int]):
        """
            Find the middle of the bounding box.
        
            Parameterss
            -----------
                separeted_box: dict
                    parking space bounding box (values stored in coord.json).

            Output
            ------
                middle: dict
                    dict obtaining x .
            """
        
        middle = {}
        middle["x"] = int((separeted_box["xmax"] + separeted_box["xmin"]) / 2)
        middle["y"] = int((separeted_box["ymax"] + separeted_box["ymin"]) / 2)
        
        return middle

    
    @staticmethod
    def find_dimensions(separeted_box:Dict[str, int]):
        dimensions = {}
        dimensions["width"] = separeted_box["xmax"] - separeted_box["xmin"]
        dimensions["height"] = separeted_box["ymax"] - separeted_box["ymin"]

        return dimensions
    

    def iou(self, bounding_box_2):
            x_left = max(self.bounding_box["xmin"], bounding_box_2["xmin"])
            y_top = max(self.bounding_box["ymin"], bounding_box_2["ymin"])
            x_right = min(self.bounding_box["xmax"], bounding_box_2["xmax"])
            y_bottom = min(self.bounding_box["ymax"], bounding_box_2["ymax"])

            if x_right < x_left or y_bottom < y_top:
                return 0
            
            intersection_area = (x_right - x_left) * (y_bottom - y_top)

            try:
                iou_percentage = intersection_area / float(self.area)
            except:
                iou_percentage = 0

            return iou_percentage


    def change_size(self, n_percetage: Optional[float] = 0.4) -> None:
        """
            reduces the parking bounding to n_percentage of its own size.

            Parameterss
            -----------
                parking_box: list
                    parking space bounding box (values stored in coord.json).

                n_percetage: float
                    percentage in 0-1 scale.

            Output
            ------
                new_car_box: list
                    Car bounding box cuted in half.
            """
        assert n_percetage <= 0, "n_percentage must be bigger than 0."

        new_width = self.width * n_percetage
        new_height = self.height * n_percetage

        new_bouding_box = [
        int(self.middle["x"] - new_width / 2),
        int(self.middle["y"] - new_height / 2),
        int(self.middle["x"] + new_width / 2),
        int(self.middle["y"] + new_height / 2),
    ]
        
        self.reload_init(new_bouding_box)
