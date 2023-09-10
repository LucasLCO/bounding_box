# bounding_box

A Python package designed to simplify bounding box operations for object detection. It provides functions to calculate box centers, dimensions, and intersections, reducing the complexity of these tasks in your code. With Bounding_Box, you can streamline your object detection workflow, making it more efficient and straightforward.

## Installation
```
pip install easy-bounding-box
```

## Example

```python
from easy_bounding_box import BoundingBox
import numpy as np
import cv2

img = np.zeros((750,1000,3))

bounding_box = BoundingBox([547.31, 41.473, 940.4, 712.92])
bounding_box_2 = BoundingBox((500, 20, 700, 350))

bounding_box_3 = bounding_box_2.change_size(0.4, False)

line = (100, 250, 530, 250)

img = cv2.line(img, line[:2], line[2:], (255,255,0), 2)

img = cv2.rectangle(img, bounding_box[:2], bounding_box[2:], (255,0,0), 2)

img = cv2.rectangle(img, bounding_box_2[:2], bounding_box_2[2:], (0,255,0), 2)

img = cv2.rectangle(img, bounding_box_3[:2], bounding_box_3[2:], (0,0,255), 2)

print("Bounding box 2 is intercepting blue line: ", bounding_box_2.box_intercept_line(line))
print("bounding box is intercepting bounding_box_2: ", bounding_box.box_intercept_box(bounding_box_2.bounding_box))
print("How much of bounding_box_2 is in bounding_box: ", bounding_box_2.iou(bounding_box.bounding_box))
print("Bounding box 3 values: ", bounding_box_3.bounding_box)
print("Bounding box 3 listed values: ", bounding_box_3.list_bounding_box)
print("Bounding box 3 middle: ", bounding_box_3.middle)
print("Bounding box 3 listed middle: ", bounding_box_3.list_middle)
print("Bounding box 3 dimensions: ", bounding_box_3.dimensions)
print("Bounding box 3 listed dimensions: ", bounding_box_3.list_dimensions)
print("Bounding box 3 area: ", bounding_box_3.area)
print("Bounding box 3 walls coordinates: ", bounding_box_3.walls)

cv2.imshow("image", img)
  
cv2.waitKey(0)

cv2.destroyAllWindows()
```