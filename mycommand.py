import pandas as pd
import plotly
import plotly.express as px
import pathlib

if __name__ == '__main__':
    output_folder = 'output'
    pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)

    df = pd.read_csv('sales_data.csv', header=None)
    df.dropna(how='all', inplace=True)
    df = df.iloc[2:]
    df.columns = ['Salesman', 'Week1', 'Week2', 'Week3', 'Week4']
    df['Week1'] = df['Week1'].astype(int)

    fig = px.bar(df, x='Salesman', y='Week1')

    output_path = "{folder}/output.png".format(folder=output_folder)
    plotly.io.write_image(fig, output_path)
