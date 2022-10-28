import unittest
import a_star

class Test_A_Star(unittest.TestCase):

    # Test 41x41.txt map.
    # This is verify that the base requirement is met.
    def test_41x41(self):
        self.assertTrue(a_star.main("41x41", False, False))

    # Test 61x31.txt map.
    # This is verify that the base requirement is met.
    def test_61x31(self):
        self.assertTrue(a_star.main("61x31", False, False))

    # Test 81x81.txt map.
    # This is verify that the base requirement is met.
    def test_81x81(self):
        self.assertTrue(a_star.main("81x81", False, False))

    # Randomise the start and end location on the X-Axis 100 times
    # in the 41x41.txt map.
    # This is the verify the implementation of the A* Algorithm.
    def test_StressRandomise41x41(self):
        for _ in range(100):
            self.assertTrue(a_star.main("41x41", False, True))

    # Randomise the start and end location on the X-Axis 100 times
    # in the 61x31.txt map.
    # This is the verify the implementation of the A* Algorithm.
    def test_StressRandomise61x31(self):
        for _ in range(100):
            self.assertTrue(a_star.main("61x31", False, True))

    # Randomise the start and end location on the X-Axis 100 times
    # in the 81x81.txt map.
    # This is the verify the implementation of the A* Algorithm.
    def test_StressRandomise81x81(self):
        for _ in range(100):
            self.assertTrue(a_star.main("81x81", False, True))

if __name__ == "__main__":
    unittest.main()