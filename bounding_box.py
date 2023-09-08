from typing import Optional, Union, Sequence, Dict

class BoundingBox:
    def __init__(self, bounding_box:Sequence[Union[float, int]]) -> None:
        self.len = len(bounding_box)
        self.init(bounding_box)

    def init(self, bounding_box:Sequence[Union[float, int]]) -> None:
        self.bounding_box = self.separate_max_min(bounding_box)
        self.list_bounding_box = tuple(self.bounding_box.values())
        self.middle = self.find_middle(self.bounding_box)
        self.list_middle = tuple(self.middle.values())
        self.dimensions = self.find_dimensions(self.bounding_box)
        self.list_dimensions = tuple(self.dimensions.values())
        self.area = self.dimensions["width"] * self.dimensions["height"]
        self.walls = self.find_walls(self.bounding_box)

    def __getitem__(self, index):
        return tuple(self.bounding_box.values())[index]
    
    def __len__(self):
        return self.len

    @staticmethod
    def separate_max_min(box: Sequence[Union[float, int]])->Dict[str, int]:
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
        separeted_box["xmin"] = int(min(box[0], box[2]))
        separeted_box["ymin"] = int(min(box[1], box[3]))
        separeted_box["xmax"] = int(max(box[0], box[2]))
        separeted_box["ymax"] = int(max(box[1], box[3]))

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
    
    @staticmethod
    def find_walls(separeted_box:Dict[str, int]):
        walls = {}
        walls["top"] = (separeted_box["xmin"], separeted_box["ymin"], separeted_box["xmax"], separeted_box["ymin"])
        walls["bottom"] = (separeted_box["xmin"], separeted_box["ymax"], separeted_box["xmax"], separeted_box["ymax"])
        walls["left"] = (separeted_box["xmin"], separeted_box["ymin"], separeted_box["xmin"], separeted_box["ymax"])
        walls["right"] = (separeted_box["xmax"], separeted_box["ymin"], separeted_box["xmax"], separeted_box["ymax"])

        return walls

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

    def change_size(self, n_percetage: Optional[float] = 1, inplace: Optional[bool] = True) -> Union[None, 'BoundingBox']:
        """
            changes the bounding to n_percentage of its own size.

            Parameterss
            -----------
                n_percetage: float
                    percentage in 0-inf scale.

            Output
            ------
                new_car_box: list
                    Car bounding box cuted in half.
            """
        
        assert n_percetage > 0, "n_percentage must be bigger than 0."

        new_width = self.dimensions["width"] * n_percetage
        new_height = self.dimensions["height"] * n_percetage

        new_bouding_box = [
        int(self.middle["x"] - new_width / 2),
        int(self.middle["y"] - new_height / 2),
        int(self.middle["x"] + new_width / 2),
        int(self.middle["y"] + new_height / 2),
    ]

        if not inplace:
            return BoundingBox(new_bouding_box)
        
        self.init(new_bouding_box)
