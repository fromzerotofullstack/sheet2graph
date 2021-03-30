# only needed to run the tests
import pathlib
import shutil
import unittest
import os
from os.path import isdir, isfile
from PIL import Image
import subprocess


class TestCommandLine(unittest.TestCase):
    """
    - file is crated in path
    - google docs is opened
    - files different formats work (img is generated)
    - resolution of file
    """
    folder_output = '123_folder_output_tests'

    csv_file = './test_data/sales_data.csv'
    # Missing optional dependency 'odfpy'.  Use pip or conda to install odfpy.
    # ods_file = './test_data/sales_data.ods'
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
        cmd = 'env3.8/bin/python3.8 sheet2graph.py {params}'.format(params=params)
        os.system(cmd)

    @staticmethod
    def run_cmd_with_output(params=''):
        """
        helper to run our command
        """
        cmd = 'env3.8/bin/python3.8 sheet2graph.py {params}'.format(params=params)
        output = subprocess.check_output(cmd, shell=True)
        return output

    def setUp(self):
        pathlib.Path(self.folder_output).mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.folder_output)

    """
    Defaults
    """

    def test_default(self):
        out = self.run_cmd_with_output('')
        self.assertTrue(b'mycommand 0.1' in out)
        self.assertTrue(b'--help' in out)

    def test_version(self):
        out = self.run_cmd_with_output('--version')
        self.assertTrue(b'mycommand 0.1' in out)
        self.assertTrue(b'--help' in out)

    def test_only_input(self):
        cmd = '{input}'.format(
            input=self.csv_file,
        )
        out = self.run_cmd_with_output(cmd)
        files_created = os.listdir(self.folder_output)
        no_files_created = files_created == []
        self.assertTrue(no_files_created)
        self.assertTrue(all(el in out for el in [b'A', b'B', b'C', b'D', b'1', b'2', b'3', b'4']))

    """
    Selecting data
    """

    def test_select_data_both_params_or_none_x(self):
        cmd = '{input} -x "a2:a6" --print-only'.format(
            input=self.csv_file,
        )
        out = self.run_cmd_with_output(cmd)
        self.assertTrue(b'You need to provide both -x and -y flags' in out)

    def test_select_data_both_params_or_none_y(self):
        cmd = '{input} -y "a2:a6" --print-only'.format(
            input=self.csv_file,
        )
        out = self.run_cmd_with_output(cmd)
        self.assertTrue(b'You need to provide both -x and -y flags' in out)

    def test_select_data_bad_syntax_x(self):
        cmd = '{input} -x "a2a6" -y "b2:b6" --print-only'.format(
            input=self.csv_file,
        )
        out = self.run_cmd_with_output(cmd)
        self.assertTrue(b'Bad syntax for -x parameter' in out)

    def test_select_data_bad_syntax_y(self):
        cmd = '{input} -x "a2:a6" -y "b2b6" --print-only'.format(
            input=self.csv_file,
        )
        out = self.run_cmd_with_output(cmd)
        self.assertTrue(b'Bad syntax for -y parameter' in out)

    def test_select_data_commas_lowercase(self):
        cmd = '{input} -x "a3,a4,a5,a6" -y "b3,b4,b5,b6" --print-only'.format(
            input=self.csv_file,
        )
        out = self.run_cmd_with_output(cmd)
        no_headers = all(el not in out for el in [b'Week1', b'Week2', b'Salesman'])
        self.assertTrue(no_headers)
        self.assertTrue(b'20' in out)
        self.assertTrue(b'Ricky Roma' in out)

    def test_select_data_commas_uppercase(self):
        cmd = '{input} -x "A3,A4,A5,A6" -y "B3,B4,B5,B6" --print-only'.format(
            input=self.csv_file,
        )
        out = self.run_cmd_with_output(cmd)
        no_headers = all(el not in out for el in [b'Week1', b'Week2', b'Salesman'])
        self.assertTrue(no_headers)
        self.assertTrue(b'20' in out)
        self.assertTrue(b'Ricky Roma' in out)

    def test_select_data_range_lowercase(self):
        cmd = '{input} -x "a3:a6" -y "b3:b6" --print-only'.format(
            input=self.csv_file,
        )
        out = self.run_cmd_with_output(cmd)
        no_headers = all(el not in out for el in [b'Week1', b'Week2', b'Salesman'])
        self.assertTrue(no_headers)
        self.assertTrue(b'20' in out)
        self.assertTrue(b'Ricky Roma' in out)

    def test_select_data_range_uppercase(self):
        cmd = '{input} -x "A3:A6" -y "B3:B6" --print-only'.format(
            input=self.csv_file,
        )
        out = self.run_cmd_with_output(cmd)
        no_headers = all(el not in out for el in [b'Week1', b'Week2', b'Salesman'])
        self.assertTrue(no_headers)
        self.assertTrue(b'20' in out)
        self.assertTrue(b'Ricky Roma' in out)

    """
    Output
    """

    def test_output_folder_default(self):
        cmd = '{input} -x "a3:a6" -y "b3:b6" --output-folder {out}/output/tests'.format(
            input=self.csv_file,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isdir('{out}/output/tests'.format(out=self.folder_output)))
        self.assertTrue(isfile('{out}/output/tests/output.png'.format(out=self.folder_output)))

    def test_filename_default(self):
        cmd = '{input} -x "a3:a6" -y "b3:b6" --output-filename {out}/output/tests/out.png'.format(
            input=self.csv_file,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isdir('{out}/output/tests'.format(out=self.folder_output)))
        self.assertTrue(isfile('{out}/output/tests/out.png'.format(out=self.folder_output)))

    def test_filename_overrides_output_folder(self):
        cmd = '{input} -x "a3:a6" -y "b3:b6" --output-folder {out}/tests2 --output-filename {out}/output/tests/out.png'.format(
            input=self.csv_file,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isdir('{out}/output/tests'.format(out=self.folder_output)))
        self.assertTrue(isfile('{out}/output/tests/out.png'.format(out=self.folder_output)))
        self.assertFalse(isdir('{out}/tests2'.format(out=self.folder_output)))

    def test_output_png(self):
        cmd = '{input} -x "a3:a6" -y "b3:b6" --output-filename {out}/output/tests/out.png'.format(
            input=self.csv_file,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isfile('{out}/output/tests/out.png'.format(out=self.folder_output)))

    def test_output_jpg(self):
        cmd = '{input} -x "a3:a6" -y "b3:b6" --output-filename {out}/output/tests/out.jpg'.format(
            input=self.csv_file,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isfile('{out}/output/tests/out.jpg'.format(out=self.folder_output)))

    def test_output_svg(self):
        cmd = '{input} -x "a3:a6" -y "b3:b6" --output-filename {out}/output/tests/out.svg'.format(
            input=self.csv_file,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isfile('{out}/output/tests/out.svg'.format(out=self.folder_output)))

    """
    Sizes
    """

    def test_size_default_png(self):
        cmd = '{input} -x "a3:a6" -y "b3:b6" --output-filename {out}/output/tests/out.png'.format(
            input=self.csv_file,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isfile('{out}/output/tests/out.png'.format(out=self.folder_output)))
        w, h = self.get_image_resolution('{out}/output/tests/out.png'.format(out=self.folder_output))
        self.assertTrue(w == 700 and h == 500)

    def test_size_png(self):
        cmd = '{input} -x "a3:a6" -y "b3:b6" --output-filename {out}/output/tests/out.png --size "1400x1000"'.format(
            input=self.csv_file,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isfile('{out}/output/tests/out.png'.format(out=self.folder_output)))
        w, h = self.get_image_resolution('{out}/output/tests/out.png'.format(out=self.folder_output))
        self.assertTrue(w == 1400 and h == 1000)

    def test_size_jpg(self):
        cmd = '{input} -x "a3:a6" -y "b3:b6" --output-filename {out}/output/tests/out.jpg --size "400x300"'.format(
            input=self.csv_file,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isfile('{out}/output/tests/out.jpg'.format(out=self.folder_output)))
        w, h = self.get_image_resolution('{out}/output/tests/out.jpg'.format(out=self.folder_output))
        self.assertTrue(w == 400 and h == 300)

    """
    Graph types
    """

    def test_graph_type_bar(self):
        cmd = '{input} -x "a3:a6" -y "b3:b6" --graph-type=bar --output-filename {out}/output/tests/out.png'.format(
            input=self.csv_file,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isfile('{out}/output/tests/out.png'.format(out=self.folder_output)))

    def test_graph_type_line(self):
        cmd = '{input} -x "a3:a6" -y "b3:b6" --graph-type=line --output-filename {out}/output/tests/out.png'.format(
            input=self.csv_file,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isfile('{out}/output/tests/out.png'.format(out=self.folder_output)))

    def test_graph_type_scatter(self):
        cmd = '{input} -x "a3:a6" -y "b3:b6" --graph-type=scatter --output-filename {out}/output/tests/out.png'.format(
            input=self.csv_file,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isfile('{out}/output/tests/out.png'.format(out=self.folder_output)))

    """
    Input formats
    """

    def test_input_csv(self):
        cmd = '{input} -x "a3:a6" -y "b3:b6" --output-filename {out}/output/tests/out.png'.format(
            input=self.csv_file,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isfile('{out}/output/tests/out.png'.format(out=self.folder_output)))

    def test_input_xlsx(self):
        cmd = '{input} -x "a3:a6" -y "b3:b6" --output-filename {out}/output/tests/out.png'.format(
            input=self.xlsx_file,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isfile('{out}/output/tests/out.png'.format(out=self.folder_output)))

    def test_input_google_docs(self):
        cmd = '{input} -x "a3:a6" -y "b3:b6" --output-filename {out}/output/tests/out.png'.format(
            input=self.google_docs,
            out=self.folder_output,
        )
        self.run_cmd(cmd)
        self.assertTrue(isfile('{out}/output/tests/out.png'.format(out=self.folder_output)))


if __name__ == '__main__':
    unittest.main()
