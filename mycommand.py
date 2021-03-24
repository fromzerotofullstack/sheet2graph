import sys
from typing import Any

import pandas as pd
import plotly
import plotly.express as px
import pathlib
import argparse
from typeguard import typechecked


@typechecked
def select_data(df: pd.DataFrame) -> pd.DataFrame:
    df.dropna(how='all', inplace=True)
    df = df.iloc[2:].copy()
    df.columns = ['Salesman', 'Week1', 'Week2', 'Week3', 'Week4']
    df['Week1'] = df['Week1'].astype(int)
    return df


@typechecked
def plot(df: pd.DataFrame, graph_type: str = 'bar') -> Any:
    if graph_type == 'bar':
        fig = px.bar(df, x='Salesman', y='Week1')
    elif graph_type == 'line':
        fig = px.line(df, x='Salesman', y='Week1')
    elif graph_type == 'scatter':
        fig = px.scatter(df, x='Salesman', y='Week1')
    else:
        print("graph type not supported")
        exit()
    return fig


def main(num_args:int, input_file=None, output_filename=None, output_format='', output_folder='', output_size='700x500',
         graph_type='bar', print_version=False, version: str = '0.0'):

    # no arguments prints version and help
    if num_args == 0 or print_version:
        print("mycommand {v}".format(v=version))
        print("    run 'mycommand --help' for all the options")
        return

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

    df = select_data(df)
    fig = plot(df, graph_type=graph_type)

    plotly.io.write_image(fig, output_path, format=output_format, width=width, height=height)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""
    Graph spreadsheet data easily
    Takes a spreadsheet file as input and outputs an image file (bitmap, vector) with graphs of the data contained in the file.
    Accepted input files are csv and xlsx file extensions
    """)
    parser.add_argument('input_file', nargs='?', default=None, help='input file (csv, xlsx)')
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
            input_file=args.input_file,
            output_filename=args.output_filename,
            output_format=args.output_format,
            output_folder=args.output_folder,
            output_size=args.size,
            graph_type=args.graph_type,
            print_version=args.print_version,
            version='0.1',
        )
