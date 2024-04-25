from mobility.utils.moon_utils import MoonPhase, age, phase
import unittest


import unittest
from mobility.utils.moon_utils import MoonPhase  # Import the MoonPhase enum from your module
class TestMoonPhaseEnum(unittest.TestCase):
    def test_enum_values(self):
        """Test that the MoonPhase enum values are correctly defined."""
        # Check if each enum member's value matches its position in the enum
        self.assertEqual(MoonPhase.NEW_MOON.value, 0)
        self.assertEqual(MoonPhase.WAXING_CRESCENT.value, 1)
        self.assertEqual(MoonPhase.FIRST_QUARTER.value, 2)
        self.assertEqual(MoonPhase.WAXING_GIBBOUS.value, 3)
        self.assertEqual(MoonPhase.FULL_MOON.value, 4)
        self.assertEqual(MoonPhase.WANING_GIBBOUS.value, 5)
        self.assertEqual(MoonPhase.LAST_QUARTER.value, 6)
        self.assertEqual(MoonPhase.WANING_CRESCENT.value, 7)

    def test_enum_names(self):
        """Test that the MoonPhase enum names match the expected names."""
        # Check if each enum member's name matches the expected name
        self.assertEqual(MoonPhase.NEW_MOON.name, "NEW_MOON")
        self.assertEqual(MoonPhase.WAXING_CRESCENT.name, "WAXING_CRESCENT")
        self.assertEqual(MoonPhase.FIRST_QUARTER.name, "FIRST_QUARTER")
        self.assertEqual(MoonPhase.WAXING_GIBBOUS.name, "WAXING_GIBBOUS")
        self.assertEqual(MoonPhase.FULL_MOON.name, "FULL_MOON")
        self.assertEqual(MoonPhase.WANING_GIBBOUS.name, "WANING_GIBBOUS")
        self.assertEqual(MoonPhase.LAST_QUARTER.name, "LAST_QUARTER")
        self.assertEqual(MoonPhase.WANING_CRESCENT.name, "WANING_CRESCENT")

if __name__ == '__main__':
    unittest.main()


import unittest
import datetime
from decimal import Decimal
from mobility.utils.moon_utils import age  # Assuming your function is imported from your_module

class TestMoonAge(unittest.TestCase):
    def test_moon_age(self):
        """Test the calculation of the age of the moon."""
        # Define a target date for testing
        target_date = datetime.date(2024, 4, 24)  # Example date
        # Calculate the expected moon age manually
        # The starting date (11 August 1999) is taken as a reference point
        # We know the moon cycle is approximately 29.53059 days
        # So, we calculate the days since 11 August 1999 and take modulo 29.53059
        expected_age = (target_date - datetime.date(1999, 8, 11)).days % 29.53059
        # Call the function with the target date
        moon_age = age(target_date)
        # Assert that the calculated moon age matches the expected age
        self.assertAlmostEqual(moon_age, Decimal(expected_age), places=6)

if __name__ == '__main__':
    unittest.main()
















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


