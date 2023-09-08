# bounding_box

A Python package designed to simplify bounding box operations for object detection. It provides functions to calculate box centers, dimensions, and intersections, reducing the complexity of these tasks in your code. With Bounding_Box, you can streamline your object detection workflow, making it more efficient and straightforward.

## Example

```
from bounding_box import BoundingBox
import numpy as np
import cv2

img = np.zeros((1000,1000,3))

bounding_box = BoundingBox([747.31, 41.473, 1140.4, 712.92])
bounding_box_2 = BoundingBox((700, 20, 900, 350))

img = cv2.rectangle(img, bounding_box[:2], bounding_box[2:], (255,0,0), 2)

img = cv2.rectangle(img, bounding_box_2[:2], bounding_box_2[2:], (0,255,0), 2)

print("bounding_box is interceptingbounding_box_2: ", bounding_box.box_intercept_box(bounding_box_2.bounding_box))

print("How much of bounding_box_2 is in bounding_box: ", bounding_box_2.iou(bounding_box.bounding_box))

cv2.imshow("image", img)
  
cv2.waitKey(0)
  
cv2.destroyAllWindows()

```