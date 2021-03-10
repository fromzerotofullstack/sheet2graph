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
    parser.add_argument('--graph-type', nargs='?', dest='graph_type', default="bar", help='[bar|line]: default is bar')
    args = parser.parse_args()

    input_file = args.input_file[0]

    output_folder = 'output'
    pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)

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

    output_path = "{folder}/output.png".format(folder=output_folder)
    plotly.io.write_image(fig, output_path)
