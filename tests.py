import unittest


class TestCommandLine(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_first(self):
        self.assertEqual('test', 'test')

    def test_second(self):
        self.assertNotEqual('test2', 'testasdasdasd')


if __name__ == '__main__':
    unittest.main()
