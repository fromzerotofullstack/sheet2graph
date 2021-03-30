import sys
from typing import Any, Optional, List

import pandas as pd
import plotly
import plotly.express as px
import pathlib
import argparse
from typeguard import typechecked
from openpyxl.utils.cell import get_column_letter, coordinate_from_string
import numpy as np


@typechecked
def select_data(df: pd.DataFrame, x=Optional[str], y=Optional[str]) -> pd.DataFrame:
    @typechecked
    def get_vals_from_selector(sel: str = 'a3,a4,a5') -> List[str]:
        vals = []

        # case insensitive
        sel = sel.upper()

        # range values
        if ':' in sel:
            cells = sel.split(':')
            # A3 to ('A', 3)
            letter1, num1 = coordinate_from_string(cells[0])
            letter2, num2 = coordinate_from_string(cells[1])

            if len(cells) != 2:
                print("Bad syntax in range selector")
                exit()

            if letter1 != letter2:
                print("Only ranges with the same letter are supported")
                exit()

            # we do not want an infinite loop if syntax is wrong
            max_count = 10000
            tmp = ''
            c = num1
            while c <= num2 and c < max_count:
                tmp += letter1 + str(c) + ','
                c += 1

            if tmp.endswith(','):
                tmp = tmp[:-1]
            sel = tmp

        # comma-separated values
        if ',' in sel:
            cells = sel.split(',')
            for el in cells:
                # A3 to ('A', 3)
                letter, num = coordinate_from_string(el)
                cell_val = df[letter].iloc[num - 1]
                # xlsx can be number instead of string
                vals.append(str(cell_val))

        return vals

    df.dropna(how='all', inplace=True)

    if (x and not y) or (y and not x):
        print("""You need to provide both -x and -y flags to select data
        Examples:
            -x A2:A6 -y b2:b6
            -x a2,a3,a4,a5,a6 -y B2,B3,B4,B5,B6
        """)
        exit()

    if x and ':' not in x and ',' not in x:
        print("""Bad syntax for -x parameter
        Examples:
            -x A2:A6 -y b2:b6
            -x a2,a3,a4,a5,a6 -y B2,B3,B4,B5,B6
        """)
        exit()
    if y and ':' not in y and ',' not in y:
        print("""Bad syntax for -y parameter
        Examples:
            -x A2:A6 -y b2:b6
            -x a2,a3,a4,a5,a6 -y B2,B3,B4,B5,B6
        """)
        exit()

    """
    index like in excel
    letters for columns
    1 based integers for rows
    """

    # df = df.iloc[2:].copy()
    # df.columns = ['Salesman', 'Week1', 'Week2', 'Week3', 'Week4']
    # df['Week1'] = df['Week1'].astype(int)

    columns = df.columns.to_list()
    letter_columns = []
    for el in columns:
        letter_columns.append(get_column_letter(el + 1))

    df.columns = letter_columns
    df.index = np.arange(1, len(df) + 1)

    """
    select our data for x and y
    """
    if x and y:
        x_vals = get_vals_from_selector(x)
        y_vals = get_vals_from_selector(y)
        data = {
            'x': x_vals,
            'y': y_vals,
        }
        """
        We try to convert to numeric
        if it is not possible it will raise an exception
        and we repeat without numeric conversion
        """
        try:
            new_df = pd.DataFrame(data)
            new_df['y'] = pd.to_numeric(new_df['y'])
        except Exception as e:
            new_df = pd.DataFrame(data)

        return new_df

    return df


@typechecked
def plot(df: pd.DataFrame, graph_type: str = 'bar', xlabel='x', ylabel='y') -> Any:
    if not xlabel:
        xlabel = 'x'
    if not ylabel:
        ylabel = 'y'

    if graph_type == 'bar':
        fig = px.bar(df, x='x', y='y', labels={
            "x": xlabel,
            "y": ylabel,
        })
    elif graph_type == 'line':
        fig = px.line(df, x='x', y='y', labels={
            "x": xlabel,
            "y": ylabel,
        })
    elif graph_type == 'scatter':
        fig = px.scatter(df, x='x', y='y', labels={
            "x": xlabel,
            "y": ylabel,
        })
    else:
        print("graph type not supported")
        exit()
    return fig


def main(num_args: int, x=None, y=None, xlabel='x', ylabel='y', input_file=None, output_filename=None, output_format='',
         output_folder='',
         output_size='700x500',
         graph_type='bar', print_version=False, version: str = '0.0', print_only=False):
    # no arguments prints version and help
    if num_args == 0 or print_version:
        print("mycommand {v}".format(v=version))
        print("    run 'mycommand --help' for all the options")
        return

    # when we pass only input file we print data
    if num_args == 1 and input_file:
        print_only = True

    if not print_only:
        if output_filename:
            p = pathlib.Path(output_filename)
            output_folder = str(p.parent)
            pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)
            output_path = "{folder}/{f}".format(folder=output_folder, f=p.name)
            # .png, .svg, etc.
            output_format = p.suffix[1:]
        else:
            pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)
            output_path = "{folder}/output.{ext}".format(folder=output_folder, ext=output_format)

        if 'x' not in output_size:
            print("Wrong size format. It needs to be $WIDTHx$HEIGHT format. For example '700x500'")
            exit()

        tmp = output_size.split('x')
        width, height = tmp[0], tmp[1]

    df = pd.DataFrame()
    if input_file:
        is_google_docs = input_file.startswith('http') and 'drive.google.com' in input_file
        if is_google_docs:
            doc_id = input_file.split('/')[-2]
            input_file = 'https://drive.google.com/uc?export=download&id={doc_id}'.format(
                doc_id=doc_id
            )

        # csv, xlsx
        input_ext = pathlib.Path(input_file).suffix[1:]
        if input_ext == 'csv':
            df = pd.read_csv(input_file, header=None)
        else:
            try:
                df = pd.read_excel(input_file, header=None)
            except Exception as e:
                print("error opening file {f}".format(f=input))
                print(e)
                exit()

    df = select_data(df, x=x, y=y)
    if print_only:
        print(df)
        return

    fig = plot(df, graph_type=graph_type, xlabel=xlabel, ylabel=ylabel)

    plotly.io.write_image(fig, output_path, format=output_format, width=width, height=height)


def entry():
    parser = argparse.ArgumentParser(description="""
    Graph spreadsheet data easily
    Takes a spreadsheet file as input and outputs an image file (bitmap, vector) with graphs of the data contained in the file.
    Accepted input files are csv and xlsx file extensions
    """)
    parser.add_argument('input_file', nargs='?', default=None, help='input file (csv, xlsx)')
    parser.add_argument('-x', nargs='?', default=None,
                        help="An expression to select the x axis. Ex. '-x A2:A6' or '-x a2,a3,a4,a5'. The range works like in a spreadsheeet, with columns being letters, and row numbers starting at 1. Case-insensitive")
    parser.add_argument('-y', nargs='?', default=None,
                        help="An expression to select the y axis. Ex. '-x b2:b6' or '-x B2,B3,B4,B5'. The range works like in a spreadsheeet, with columns being letters, and row numbers starting at 1. Case-insensitive")

    parser.add_argument('-xlabel', nargs='?', default='x',
                        help="The label for the x axis. By default 'x'")
    parser.add_argument('-ylabel', nargs='?', default='y',
                        help="The label for the y axis. By default 'y'")

    parser.add_argument('--graph-type', '-gt', nargs='?', dest='graph_type', default="bar",
                        help='[bar|line|scatter]: default is bar')
    parser.add_argument(
        '--output-folder', '-of', nargs='?', dest='output_folder', default="output",
        help="output_folder (ending without slash): default is 'output'. Can be serveral folders. ex. 'sales/graphs'"
    )
    parser.add_argument(
        '--output-filename', '-ofi', nargs='?', dest='output_filename', default=None,
        help="output_filename: default is 'output/output.png'. Overrides --output-folder,--output-format if present"
    )
    parser.add_argument(
        '--output-format', '-ofo', nargs='?', dest='output_format', default='png',
        help="[png|jpg|svg]: default is png"
    )
    parser.add_argument(
        '--size', '-s', nargs='?', dest='size', default='700x500',
        help="size: widthxheight. Default '700x500'"
    )
    parser.add_argument(
        '--print-only', '-p', nargs='?', dest='print_only', default=False, const=True,
        help="Prints the selected data, without generating any file output"
    )
    parser.add_argument(
        '--run-tests', nargs='?', dest='run_tests', default=False, const=True,
        help="Runs all the tests (might take a while). Overloads any other option"
    )
    parser.add_argument(
        '--version', '-v', nargs='?', dest='print_version', default=False, const=True,
        help="Show version information"
    )
    args = parser.parse_args()

    if args.run_tests:
        import unittest
        from tests import TestCommandLine

        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestCommandLine)
        unittest.TextTestRunner().run(suite)
    else:
        # includes name of the script
        num_args = len((sys.argv)) - 1
        main(
            num_args=num_args,
            x=args.x,
            y=args.y,
            xlabel=args.xlabel,
            ylabel=args.ylabel,
            input_file=args.input_file,
            output_filename=args.output_filename,
            output_format=args.output_format,
            output_folder=args.output_folder,
            output_size=args.size,
            graph_type=args.graph_type,
            print_version=args.print_version,
            print_only=args.print_only,
            version='0.1',
        )


if __name__ == '__main__':
    entry()
