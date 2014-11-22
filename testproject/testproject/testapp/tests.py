from django.test import TestCase


class SimpleTest(TestCase):
    """
    A couple of dummy tests to demonstrate 'manage.py test --pdb'.
    """

    def test_error(self):
        """
        Tests that 1 + 1 always equals 4.
        """
        a = 1
        b = 2
        c = 3
        one_plus_one = four

    def test_failure(self):
        """
        Tests that 1 + 1 always equals 4.
        """
        a = 1
        b = 2
        c = 3
        self.assertEqual(1 + 1, 4)
