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


def main(input_file='', output_filename=None, output_format='', output_folder='', output_size='700x500',
         graph_type='bar'):
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

    tmp = output_size.split('x')
    width, height = tmp[0], tmp[1]

    # csv, xlsx
    accepted_excel_formats = ['xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt']
    input_ext = pathlib.Path(input_file).suffix[1:]
    if input_ext == 'csv':
        df = pd.read_csv(input_file, header=None)
    elif input_ext in accepted_excel_formats:
        df = pd.read_excel(input_file, header=None)
    else:
        print("Spreadhseet file format not supported. Please use one fo the supported formats ({extensions})".format(
        extensions=",".join(accepted_excel_formats)))
        exit()

    df = select_data(df)
    fig = plot(df, graph_type=graph_type)

    plotly.io.write_image(fig, output_path, format=output_format, width=width, height=height)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""
    Graph spreadsheet data easily
    Takes a spreadsheet file as input and outputs an image file (bitmap, vector) with gaphs of the data contained in the file.
    Accept input files are xls, xlsx, xlsm, xlsb, odf, ods and odt file extensions
    """)
    parser.add_argument('input_file', nargs='+', help='input file (csv,xls, xlsx)')
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
    args = parser.parse_args()

    input_file = args.input_file[0]
    main(
        input_file=input_file,
        output_filename=args.output_filename,
        output_format=args.output_format,
        output_folder=args.output_folder,
        output_size=args.size,
        graph_type=args.graph_type,
    )
