from typing import Union, Sequence, Dict, Tuple


def separate_box(bounding_box: Sequence[Union[float, int]]) -> Dict[str, int]:
    """
    Separate the box by its maxs and mins (in x, y).

    Args:
        bounding_box (Sequence of int or float): Object detection algorithm return values in xyxy.

    Returns:
        dict: bounding box xmin, ymin, xmax, ymax values.
    """

    assert (
        bounding_box[0] != bounding_box[2] and bounding_box[1] != bounding_box[3]
    ), "Invalid box."

    separeted_box = {}
    separeted_box["xmin"] = int(min(bounding_box[0], bounding_box[2]))
    separeted_box["ymin"] = int(min(bounding_box[1], bounding_box[3]))
    separeted_box["xmax"] = int(max(bounding_box[0], bounding_box[2]))
    separeted_box["ymax"] = int(max(bounding_box[1], bounding_box[3]))
    separeted_box["class"] = int(bounding_box[4])

    assert set(separeted_box.values()) != {
        0
    }, "Values given must be different than 0. The values might be normalized."

    return separeted_box


def find_middle(separeted_box: Dict[str, int]) -> Dict[str, int]:
    """
    Find the middle of the bounding box.

    Args:
        separeted_box (dict): Dictionary with keys xmin, ymin, xmax, ymax to store bouding box coordinates.

    Returns:
        dict: bounding box middle x and y coordinates values.
    """

    middle = {}
    middle["x"] = int((separeted_box["xmax"] + separeted_box["xmin"]) / 2)
    middle["y"] = int((separeted_box["ymax"] + separeted_box["ymin"]) / 2)

    return middle


def find_dimensions(separeted_box: Dict[str, int]) -> Dict[str, int]:
    """
    Find width and height of the bounding box.

    Args:
        separeted_box (dict): Dictionary with keys xmin, ymin, xmax, ymax to store bouding box coordinates.

    Returns:
        dict: bounding box width and height values in pixels.
    """

    dimensions = {}
    dimensions["width"] = separeted_box["xmax"] - separeted_box["xmin"]
    dimensions["height"] = separeted_box["ymax"] - separeted_box["ymin"]

    return dimensions


def find_walls(separeted_box: Dict[str, int]) -> Dict[str, int]:
    """
    Find walls coordinates of the bounding box.

    Args:
        separeted_box (dict): Dictionary with keys xmin, ymin, xmax, ymax to store bouding box coordinates.

    Returns:
        dict: bounding box top, bottom, left, right walls coordinates in xyxy.
    """

    walls = {}
    walls["top"] = (
        separeted_box["xmin"],
        separeted_box["ymin"],
        separeted_box["xmax"],
        separeted_box["ymin"],
    )
    walls["bottom"] = (
        separeted_box["xmin"],
        separeted_box["ymax"],
        separeted_box["xmax"],
        separeted_box["ymax"],
    )
    walls["left"] = (
        separeted_box["xmin"],
        separeted_box["ymin"],
        separeted_box["xmin"],
        separeted_box["ymax"],
    )
    walls["right"] = (
        separeted_box["xmax"],
        separeted_box["ymin"],
        separeted_box["xmax"],
        separeted_box["ymax"],
    )

    return walls

def is_counterclockwise(
        self, a: Tuple[int, int], b: Tuple[int, int], c: Tuple[int, int]
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


def separate_classes(dict_boxes):
    classes = {cls for cls in set(dict_boxes[::].dict_bouding_box["class"])}