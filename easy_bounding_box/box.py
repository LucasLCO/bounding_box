from typing import Optional, Union, Sequence, Dict, Tuple, List
from .utils.box_utils import separate_max_min, find_middle, find_dimensions, find_walls

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
        self._init(bounding_box)

    def _init(self, bounding_box: Sequence[Union[float, int]]) -> None:
        """
        Used to update values of the bounding box without another instance.

        Args:
            bouding_box (Sequence of int or float): Object detection algorithm return values in xyxy.

        Returns:
            None.
        """

        self.bounding_box = separate_max_min(bounding_box)
        self.list_bounding_box = tuple(self.bounding_box.values())
        self.middle = find_middle(self.bounding_box)
        self.list_middle = tuple(self.middle.values())
        self.dimensions = find_dimensions(self.bounding_box)
        self.list_dimensions = tuple(self.dimensions.values())
        self.area = self.dimensions["width"] * self.dimensions["height"]
        self.walls = find_walls(self.bounding_box)

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

    def iou(self, bounding_box_2: Dict[str, int]) -> float:
        """
        Calculates how much of itslef is in bounding_box_2.

        Args:
            bounding_box_2 (dict): Dictionary with keys xmin, ymin, xmax, ymax to store bouding box coordinates.

        Returns:
            float: Percentage value of iou.
        """

        x_left = max(self.bounding_box["xmin"], bounding_box_2["xmin"])
        y_top = max(self.bounding_box["ymin"], bounding_box_2["ymin"])
        x_right = min(self.bounding_box["xmax"], bounding_box_2["xmax"])
        y_bottom = min(self.bounding_box["ymax"], bounding_box_2["ymax"])

        if x_right < x_left or y_bottom < y_top:
            return 0

        intersection_area = (x_right - x_left) * (y_bottom - y_top)

        iou_percentage = intersection_area / float(self.area)

        return iou_percentage

    def change_size(
        self, n_percetage: Optional[float] = 1, inplace: Optional[bool] = True
    ) -> Union[None, "BoundingBox"]:
        """
        Change the bounding to n_percentage of its own size.

        Args:
            n_percetage (float): Percentage to be calculated.
            inplace (bool): If it is going to change this instace values or create another instance.

        Returns:
            None if inplace otherwise new instance of BoundingBox with changed values.
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

        self._init(new_bounding_box)

    @staticmethod
    def _is_counterclockwise(
        a: Tuple[int, int], b: Tuple[int, int], c: Tuple[int, int]
    ) -> bool:
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

    def _do_segments_intersect(
        self,
        start_ab: Tuple[int, int],
        end_ab: Tuple[int, int],
        start_cd: Tuple[int, int],
        end_cd: Tuple[int, int],
    ) -> bool:
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

        return self._is_counterclockwise(
            start_ab, start_cd, end_cd
        ) != self._is_counterclockwise(
            end_ab, start_cd, end_cd
        ) and self._is_counterclockwise(
            start_ab, end_ab, start_cd
        ) != self._is_counterclockwise(
            start_ab, end_ab, end_cd
        )

    def box_intercept_line(self, line: Tuple[int, int, int, int]) -> bool:
        """
        Check if any of box wall is hitting in a given line.

        Args:
            line (tuple): line to check intersection

        Returns:
            bool: True if the box and line intersect, False otherwise.
        """

        for wall in self.walls:
            intercept = self._do_segments_intersect(
                self.walls[wall][:2], self.walls[wall][2:], line[:2], line[2:]
            )
            if intercept:
                return True
        return False

    def box_intercept_box(self, bounding_box_2: Dict[str, int]) -> bool:
        """
        Check if box intercept another given bounding_box_2.

        Args:
            bounding_box_2 (dict): Dictionary with keys xmin, ymin, xmax, ymax to store bouding box coordinates.

        Returns:
            bool: True if the box and bounding_box_2 intersect, False otherwise.
        """

        if (
            self.bounding_box["xmin"] > bounding_box_2["xmax"]
            or self.bounding_box["xmax"] < bounding_box_2["xmin"]
            or self.bounding_box["ymin"] > bounding_box_2["ymax"]
            or self.bounding_box["ymax"] < bounding_box_2["ymin"]
        ):
            return False
        return True
