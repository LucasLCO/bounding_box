from typing import Optional, Union, Sequence, Dict, Tuple

class BoundingBox:
    def __init__(self, bounding_box:Sequence[Union[float, int]]) -> None:
        """ Class to simplify bounding boxes usage.
        
        It does calculations such as, finding middle, dimensions, intersections to save time and code when working with object detection algorithms.

        Attributes:
            bounding_box (dict): Dictionary with keys xmin, ymin, xmax, ymax to store bouding box coordinates.
            list_bounding_box (tuple): Tuple contating xmin, ymin, xmax, ymax respectively.
            middle (dict): Dictionary with keys x and y store bouding box middle coordinates.
            list_middle (tuple): Tuple contating middle x and y respectively.
            dimensions (dict): Dictionary with keys width and height to store bouding dimensions size. 
            list_dimensions (tuple): Tuple contating widht and height respectively.
            area (int): bounding box area in pixels.
            walls (dict): Dictionary with keys top, bottom, left, right to store box walls coordinates in a tuple (x1, y1, x2, y2).

        Methods:
            separate_max_min(box):
                Separate a given xyxy box in xmin, ymin, xmax, ymax values in a dict
             
            find_middle(separeted_box):
                Find the middle a box given the separated box and stores it in a dict.

            find_dimensions(separeted_box):
                Find width and height of a box given the separated box and stores it in a dict.

            find_walls(separeted_box):
                Find the walls coordinates in x1, y1, x2, y2 given the separated box and stores it in a dict.

            iou(bounding_box_2):
                Calculates how much of itslef is in bounding_box_2.
            
            change_size(n_percetage, inplace):
                Changes the bounding to n_percentage of its own size and if change it intern values or create anthor object with the new values given inplace.

            box_intercept_line(line):
                Check if any of box wall is hitting in a given line.

            box_intercept_box(bounding_box_2):
                Check if box intercept another given bounding_box_2.
            
                
        Example:
            ```python
            box = BoundingBox((200, 200, 400, 400))
            box.walls
            ```
        """

        self._len = len(bounding_box)
        self.__init(bounding_box)

    def __init(self, bounding_box:Sequence[Union[float, int]]) -> None:
        self.bounding_box = self.separate_max_min(bounding_box)
        self.list_bounding_box = tuple(self.bounding_box.values())
        self.middle = self.find_middle(self.bounding_box)
        self.list_middle = tuple(self.middle.values())
        self.dimensions = self.find_dimensions(self.bounding_box)
        self.list_dimensions = tuple(self.dimensions.values())
        self.area = self.dimensions["width"] * self.dimensions["height"]
        self.walls = self.find_walls(self.bounding_box)

    def __getitem__(self, index):
        return self.list_bounding_box[index]

    def __len__(self):
        return self._len

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

    def iou(self, bounding_box_2:Dict[str, int]) -> float:
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

        new_bounding_box = [
        int(self.middle["x"] - new_width / 2),
        int(self.middle["y"] - new_height / 2),
        int(self.middle["x"] + new_width / 2),
        int(self.middle["y"] + new_height / 2),
    ]

        if not inplace:
            return BoundingBox(new_bounding_box)
        
        self.__init(new_bounding_box)

    @staticmethod
    def __is_counterclockwise(a: Tuple[int, int], b: Tuple[int, int], c: Tuple[int, int]) -> bool:
        """
        Determines if three points are in a counterclockwise orientation.

        Args:
            a (Tuple[float, float]): Coordinates of point A (x, y).
            b (Tuple[float, float]): Coordinates of point B (x, y).
            c (Tuple[float, float]): Coordinates of point C (x, y).

        Returns:
            bool: True if the points are in a counterclockwise orientation, False otherwise.
        """

        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

    def __do_segments_intersect(self, start_ab: Tuple[int, int], end_ab: Tuple[int, int], start_cd: Tuple[int, int], end_cd: Tuple[int, int]) -> bool:
        """
        Checks if two line segments AB and CD intersect.

        Args:
            start_ab (Tuple[float, float]): Coordinates of the start point of segment AB (x, y).
            end_ab (Tuple[float, float]): Coordinates of the end point of segment AB (x, y).
            start_cd (Tuple[float, float]): Coordinates of the start point of segment CD (x, y).
            end_cd (Tuple[float, float]): Coordinates of the end point of segment CD (x, y).

        Returns:
            bool: True if the line segments AB and CD intersect, False otherwise.
        """

        return self.__is_counterclockwise(start_ab, start_cd, end_cd) != self.__is_counterclockwise(end_ab, start_cd, end_cd) and self.__is_counterclockwise(start_ab, end_ab, start_cd) != self.__is_counterclockwise(start_ab, end_ab, end_cd)
    
    def box_intercept_line(self, line:Tuple[int, int, int, int]) -> bool:
        for wall in self.walls:
            intercept = self.__do_segments_intersect(self.walls[wall][:2], self.walls[wall][2:], line[:2], line[2:])
            if intercept:
                
                return True
        return False
    
    def box_intercept_box(self, bounding_box_2:Dict[str, int]) -> bool:
        if (self.bounding_box["xmin"] > bounding_box_2["xmax"] or self.bounding_box["xmax"] < bounding_box_2["xmin"] or
            self.bounding_box["ymin"] > bounding_box_2["ymax"] or self.bounding_box["ymax"] < bounding_box_2["ymin"]):

            return False
        return True
