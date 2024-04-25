from mobility.utils.moon_utils import MoonPhase, age, phase
import unittest

class TestMoonPhases(unittest.TestCase):
   def test_phase(self):
       # Test with various known moon ages
       # Note that the intervals and exact phases may vary slightly depending on the calculations
       # Here we are just checking if the returned phases fall within the expected intervals
       # We manually calculate the expected moon phase values based on the day values
       # provided by the age() function

        self.assertEqual(phase(0), MoonPhase.NEW_MOON)
        self.assertEqual(phase(1.84566), MoonPhase.WAXING_CRESCENT)
        self.assertEqual(phase(6), MoonPhase.FIRST_QUARTER)
        self.assertEqual(phase(11), MoonPhase.WAXING_GIBBOUS)
        self.assertEqual(phase(15), MoonPhase.FULL_MOON)
        self.assertEqual(phase(19), MoonPhase.WANING_GIBBOUS)
        self.assertEqual(phase(22), MoonPhase.LAST_QUARTER)
        self.assertEqual(phase(26), MoonPhase.WANING_CRESCENT)
        self.assertEqual(phase(29), MoonPhase.NEW_MOON)


if __name__ == '__main__':
    unittest.main()


