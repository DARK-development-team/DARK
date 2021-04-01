from django.test import TestCase

class SimpleTest(TestCase):

    def test_assert_ok(self):
        self.assertEqual(1, 1)

    def test_assert_wrong(self):
        self.assertEqual(0, 1)

# Create your tests here.
