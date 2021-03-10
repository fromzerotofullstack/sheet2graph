import pandas as pd
import plotly
import plotly.express as px
import pathlib
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""
    Graph spreadsheet data easily
    Takes a spreadsheet file (csv, xls) as input and outputs an image file (bitmap, vector) with gaphs of the data contained in the file
    """)
    parser.add_argument('input_file', nargs='+', help='input file (csv,xls)')
    parser.add_argument('--graph-type', '-gt', nargs='?', dest='graph_type', default="bar", help='[bar|line]: default is bar')
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
    output_filename = args.output_filename

    if output_filename:
        p = pathlib.Path(output_filename)
        output_folder = str(p.parent)
        pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)
        output_path = "{folder}/{f}".format(folder=output_folder, f=p.name)
        # .png, .svg, etc.
        output_format = p.suffix[1:]
    else:
        output_folder = args.output_folder
        pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)
        output_format = args.output_format
        output_path = "{folder}/output.{ext}".format(folder=output_folder, ext=output_format)

    tmp = args.size.split('x')
    width, height = tmp[0], tmp[1]


    df = pd.read_csv(input_file, header=None)
    df.dropna(how='all', inplace=True)
    df = df.iloc[2:]
    df.columns = ['Salesman', 'Week1', 'Week2', 'Week3', 'Week4']
    df['Week1'] = df['Week1'].astype(int)

    if args.graph_type == 'bar':
        fig = px.bar(df, x='Salesman', y='Week1')
    elif args.graph_type == 'line':
        fig = px.line(df, x='Salesman', y='Week1')
    else:
        raise Exception("graph type not supported")

    plotly.io.write_image(fig, output_path, format=output_format, width=width, height=height)
