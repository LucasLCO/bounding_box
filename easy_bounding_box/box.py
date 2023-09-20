from typing import Optional, Union, Sequence, Dict, Tuple, List
from .utils.box_utils import separate_box, find_middle, find_dimensions, find_walls, do_segments_intersect


class BoundingBox:
    """
    Class to simplify bounding boxes usage.

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

    def __init__(self, bounding_box: Sequence[Union[float, int]]) -> None:
        """
        Initializes a BoundingBox instance.

        Args:
            bouding_box (Sequence of int or float): object detection algorithm return values in xyxy.

        Returns:
            None.
        """

        self._len = len(bounding_box)
        self._update(bounding_box)
        self.class_ = bounding_box[4]

    def _update(self, bounding_box: Sequence[Union[float, int]]) -> None:
        """
        Used to update values of the bounding box without another instance.

        Args:
            bouding_box (Sequence of int or float): Object detection algorithm return values in xyxy.

        Returns:
            None.
        """

        self.dict_bounding_box = separate_box(bounding_box)
        self.list_bounding_box = tuple(self.dict_bounding_box.values())
        self.dict_middle = find_middle(self.dict_bounding_box)
        self.list_middle = tuple(self.dict_middle.values())
        self.dict_dimensions = find_dimensions(self.dict_bounding_box)
        self.list_dimensions = tuple(self.dict_dimensions.values())
        self.area = self.dict_dimensions["width"] * self.dict_dimensions["height"]
        self.walls = find_walls(self.dict_bounding_box)

        assert self.area > 0, "Area must be grater than 0"

    def __getitem__(self, index) -> Union[List[int], int]:
        """
        Returns bounding box xyxy value at position index.

        Args:
            index (int): Desired position.

        Returns:
            list of int or int: Value(s) at desired position.
        """

        return self.list_bounding_box[index]

    def __len__(self) -> int:
        """
        Returns bounding box length.

        Args:
            None.

        Returns:
            int: bounding box length.
        """

        return self._len
    
    def __str__(self) -> str:
        return f""""
        {self.dict_bounding_box}
        {self.dict_middle}
        {self.dict_dimensions}
        {self.walls}
        """

    def iou(self, bounding_box_2: "BoundingBox") -> float:
        """
        Calculates how much of itslef is in bounding_box_2.

        Args:
            bounding_box_2 (dict): Dictionary with keys xmin, ymin, xmax, ymax to store bouding box coordinates.

        Returns:
            float: Percentage value of iou.
        """

        x_left = max(self.dict_bounding_box["xmin"], bounding_box_2.dict_bounding_box["xmin"])
        y_top = max(self.dict_bounding_box["ymin"], bounding_box_2.dict_bounding_box["ymin"])
        x_right = min(self.dict_bounding_box["xmax"], bounding_box_2.dict_bounding_box["xmax"])
        y_bottom = min(self.dict_bounding_box["ymax"], bounding_box_2.dict_bounding_box["ymax"])

        if x_right < x_left or y_bottom < y_top:
            return 0

        intersection_area = (x_right - x_left) * (y_bottom - y_top)

        iou_percentage = intersection_area / float(self.area)

        return iou_percentage

    def change_size(
        self, n_percetage: Optional[float] = 1, inplace: Optional[bool] = True
    ) -> Union[None, "BoundingBox"]:
        """
        Change the bounding box size to n_percentage of its own size.

        Args:
            n_percetage (float): Percentage to be calculated.
            inplace (bool): If it is going to change this instace values or create another instance.

        Returns:
            None if inplace otherwise new instance of BoundingBox with changed values.
        """

        assert n_percetage > 0, "n_percentage must be bigger than 0."

        new_width = self.dict_dimensions["width"] * n_percetage
        new_height = self.dict_dimensions["height"] * n_percetage

        new_bounding_box = [
            int(self.dict_middle["x"] - new_width / 2),
            int(self.dict_middle["y"] - new_height / 2),
            int(self.dict_middle["x"] + new_width / 2),
            int(self.dict_middle["y"] + new_height / 2),
            int(self.class_)
        ]

        if not inplace:
            return BoundingBox(new_bounding_box)

        self._update(new_bounding_box)


    def box_intercept_line(self, line: Tuple[int, int, int, int]) -> bool:
        """
        Check if any of box wall is hitting in a given line.

        Args:
            line (tuple): line to check intersection

        Returns:
            bool: True if the box and line intersect, False otherwise.
        """

        for wall in self.walls:
            intercept = do_segments_intersect(
                self.walls[wall][:2], self.walls[wall][2:], line[:2], line[2:]
            )
            if intercept:
                return True
        return False

    def box_intercept_box(self, bounding_box_2: "BoundingBox") -> bool:
        """
        Check if box intercept another given bounding_box_2.

        Args:
            bounding_box_2 (dict): Dictionary with keys xmin, ymin, xmax, ymax to store bouding box coordinates.

        Returns:
            bool: True if the box and bounding_box_2 intersect, False otherwise.
        """

        if (
            self.dict_bounding_box["xmin"] > bounding_box_2.dict_bounding_box["xmax"]
            or self.dict_bounding_box["xmax"] < bounding_box_2.dict_bounding_box["xmin"]
            or self.dict_bounding_box["ymin"] > bounding_box_2.dict_bounding_box["ymax"]
            or self.dict_bounding_box["ymax"] < bounding_box_2.dict_bounding_box["ymin"]
        ):
            return False
        return True

    def precise_change_size(
        self,
        percentages: Optional[Tuple[float, float, float, float]] = (1, 1, 1, 1),
        inplace: Optional[bool] = True,
    ) -> Union[None, "BoundingBox"]:
        """
        Change the bounding box xmin, ymin, xmax, ymax to the percentile on percentages based on its dimensions.

        Args:
            percentages (tuple): Percentages to be calculated.
            inplace (bool): If it is going to change this instace values or create another instance.

        Returns:
            None if inplace otherwise new instance of BoundingBox with changed values.
        """
        
        x_min = percentages[0] * 2 - 1 
        y_min = percentages[1] * 2 - 1
        x_max = percentages[2] * 2 - 1
        y_max = percentages[3] * 2 - 1

        new_bounding_box = [
            int(self.dict_middle["x"] - (self.dict_dimensions["width"] / 2 *  x_min)),
            int(self.dict_middle["y"] - (self.dict_dimensions["height"] / 2 * y_min)),
            int(self.dict_middle["x"] + (self.dict_dimensions["width"] / 2 *  x_max)),
            int(self.dict_middle["y"] + (self.dict_dimensions["height"] / 2 * y_max)),
            int(self.class_)
        ]
        if not inplace:
            return BoundingBox(new_bounding_box)

        self._update(new_bounding_box)
