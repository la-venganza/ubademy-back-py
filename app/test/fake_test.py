import unittest


def fake_incrementer(x):
    return x + 1


def test_fake_incremente_answer():
    assert fake_incrementer(3) == 4


class MyTestCase(unittest.TestCase):

    def test_something_equal(self):
        self.assertEqual(True, True)

    def test_something_not_equal(self):
        self.assertNotEqual(True, False)


if __name__ == '__main__':
    unittest.main()
