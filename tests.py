# only needed to run the tests
import pathlib
import shutil
import unittest
import os
from os.path import isdir, isfile
from PIL import Image


class TestCommandLine(unittest.TestCase):
    """
    - file is crated in path
    - google docs is opened
    - files different formats work (img is generated)
    - resolution of file
    """
    folder_output = '123_folder_output_tests'

    csv_file = './test_data/sales_data.csv'
    ods_file = './test_data/sales_data.ods'
    xlsx_file = './test_data/sales_data.xlsx'
    google_docs = "https://drive.google.com/file/d/1y1MzCLpFioVAHnGNZDKG5L4O62PtCqZX/view?usp=sharing"

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
        cmd = 'env3.8/bin/python3.8 mycommand.py {params}'.format(params=params)
        os.system(cmd)

    def setUp(self):
        pathlib.Path(self.folder_output).mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.folder_output)

    """
    Output
    """

    def test_output_folder_default(self):
        cmd = '{input} --output-folder {out}/output/tests'.format(
            input=self.csv_file,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isdir('{out}/output/tests'.format(out=self.folder_output)))
        self.assertTrue(isfile('{out}/output/tests/output.png'.format(out=self.folder_output)))

    def test_filename_default(self):
        cmd = '{input} --output-filename {out}/output/tests/out.png'.format(
            input=self.csv_file,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isdir('{out}/output/tests'.format(out=self.folder_output)))
        self.assertTrue(isfile('{out}/output/tests/out.png'.format(out=self.folder_output)))

    def test_filename_overrides_output_folder(self):
        cmd = '{input} --output-folder {out}/tests2 --output-filename {out}/output/tests/out.png'.format(
            input=self.csv_file,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isdir('{out}/output/tests'.format(out=self.folder_output)))
        self.assertTrue(isfile('{out}/output/tests/out.png'.format(out=self.folder_output)))
        self.assertFalse(isdir('{out}/tests2'.format(out=self.folder_output)))

    def test_output_png(self):
        cmd = '{input} --output-filename {out}/output/tests/out.png'.format(
            input=self.csv_file,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isfile('{out}/output/tests/out.png'.format(out=self.folder_output)))

    def test_output_jpg(self):
        cmd = '{input} --output-filename {out}/output/tests/out.jpg'.format(
            input=self.csv_file,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isfile('{out}/output/tests/out.jpg'.format(out=self.folder_output)))

    def test_output_svg(self):
        cmd = '{input} --output-filename {out}/output/tests/out.svg'.format(
            input=self.csv_file,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isfile('{out}/output/tests/out.svg'.format(out=self.folder_output)))

    """
    Sizes
    """

    """
    Graph types
    """

    """
    Input formats
    """


if __name__ == '__main__':
    unittest.main()
