# only needed to run the tests
import pathlib
import shutil
import unittest
import os
from PIL import Image


class TestCommandLine(unittest.TestCase):
    """
    - file is crated in path
    - google docs is opened
    - files different formats work (img is generated)
    - resolution of file
    """
    folder_output = '123_folder_output_tests'

    @staticmethod
    def file_exists(fp):
        return os.path.isfile(fp)

    @staticmethod
    def get_image_resolution(fp):
        im = Image.open(fp)
        width, height = im.size
        return width, height

    @staticmethod
    def run_cmd(params=''):
        """
        helper to run our command
        """
        cmd = 'env3.8/bin/python3.8 mycommand.py {params}'.format(params)
        os.system(cmd)

    def setUp(self):
        pathlib.Path(self.folder_output).mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.folder_output)

    def test_first(self):
        self.assertEqual('test', 'test')

    def test_second(self):
        self.assertNotEqual('test2', 'testasdasdasd')


if __name__ == '__main__':
    unittest.main()
