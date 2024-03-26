import unittest
import moon_utils
import datetime

class TestMoonUtils(unittest.TestCase):
    def test_moon_phase(self):
        self.assertAlmostEqual(moon_utils.age(datetime.date(2021, 1, 1)), 17.92, places=2)
        self.assertAlmostEqual(moon_utils.age(datetime.date(2021, 1, 2)), 18.92, places=2)
        self.assertAlmostEqual(moon_utils.age(datetime.date(2021, 1, 3)), 19.92, places=2)

    def test_phase(self):
        my_fixture = datetime.date(2019, 1, 21)
        expected = moon_utils.MoonPhase.FULL_MOON
        # phase de test avec des appels assert
        self.assertEqual(moon_utils.phase(moon_utils.age(my_fixture)), expected, msg=f'My error message on pl.f({my_fixture}) different than {expected}')

if __name__ == '__main__':
    unittest.main(verbosity=2)
