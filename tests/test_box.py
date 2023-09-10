import unittest
import sys
sys.path.append("./")
from easy_bounding_box.box import BoundingBox

class TestBoundingBox(unittest.TestCase):
    def test_iou(self):
        bounding_box = BoundingBox((500, 20, 700, 350))
        bounding_box_2 = BoundingBox([547.31, 41.473, 940.4, 712.92])
        self.assertGreaterEqual(bounding_box.iou(bounding_box_2.bounding_box), 0)
        self.assertLessEqual(bounding_box.iou(bounding_box_2.bounding_box), 1)
        self.assertGreaterEqual(bounding_box_2.iou(bounding_box.bounding_box), 0)
        self.assertLessEqual(bounding_box_2.iou(bounding_box.bounding_box), 1)

if __name__ == "__main__":
    unittest.main()
