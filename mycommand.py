import pandas as pd
import plotly
import plotly.express as px

if __name__ == '__main__':
    df = pd.read_csv('sales_data.csv', header=None)
    df.dropna(how='all', inplace=True)
    df = df.iloc[2:]
    df.columns = ['Salesman', 'Week1', 'Week2', 'Week3', 'Week4']
    df['Week1'] = df['Week1'].astype(int)

    fig = px.bar(df, x='Salesman', y='Week1')
    plotly.io.write_image(fig, "output.png")
