import unittest
import sys
sys.path.append("./")
from easy_bounding_box.utils.box_utils import separate_max_min

class TestBox(unittest.TestCase):
    def test_separate_max_min(self):
        self.assertEqual(separate_max_min([0, 1, 2, 3]), {"xmin":0, "ymin":1, "xmax":2, "ymax":3})
        self.assertEqual(separate_max_min([12, 23, 0, 4]), {"xmin":0, "ymin":4, "xmax":12, "ymax":23})
        self.assertEqual(separate_max_min((-12, -23, 0, 4)), {"xmin":-12, "ymin":-23, "xmax":0, "ymax":4})

if __name__ == "__main__":
    unittest.main()