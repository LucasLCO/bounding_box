import numpy as np
import numpy.typing as npt
from typing import Optional, List, Union, Sequence, Dict


class BoundingBox:
    box_type = Union[Sequence[Union[float, int]], npt.NDArray[Union[np.float64, np.int64]]]

    def __init__(self, bounding_box:box_type) -> None:
        self.bounding_box = bounding_box 


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

def iou(box1, box2):
        x_left = max(box1[0], box2[0])
        y_top = max(box1[1], box2[1])
        x_right = min(box1[2], box2[2])
        y_bottom = min(box1[3], box2[3])

        if x_right < x_left or y_bottom < y_top:
            return 0

        intersection_area = (x_right - x_left) * (y_bottom - y_top)

        box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
        try:
            iou_percentage = intersection_area / float(box1_area)
        except:
            iou_percentage = 0

        return iou_percentage

def treat_car_bounding_box(car_box: box_type) -> list:
        """
        Cut the half of the bounding box.

        Parameterss
        -----------
            car_box: Sequence of floats
                Car bounding box (yolo output).

        Output
        ------
            new_car_box: list
                Car bounding box cuted in half.
        """
        separeted_box = separate_max_min(car_box)
        mid = find_middle(separeted_box)

        new_car_box = [separeted_box["xmin"], int(mid[1]), separeted_box["xmax"], separeted_box["ymax"]]
        return new_car_box

def treat_parking_bounding_box(parking_box: box_type,
                                n_percetage: Optional[float] = 0.4) -> List[int]:
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

    separeted_box = separate_max_min(parking_box)
    width = separeted_box["xmax"] - separeted_box["xmin"]
    height = separeted_box["ymax"] - separeted_box["ymin"]

    new_width = width * n_percetage
    new_height = height * n_percetage

    middle = find_middle(separeted_box)

    new_parking_box = [
        int(middle["x"] - new_width / 2),
        int(middle["y"] - new_height / 2),
        int(middle["x"] + new_width / 2),
        int(middle["y"] + new_height / 2),
    ]

    return new_parking_box
