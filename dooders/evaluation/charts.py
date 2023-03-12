import pandas as pd
import plotly.express as px


def plot_df(df: pd.DataFrame) -> None:
    """ 
    Plots a line chart of the provided dataframe. 

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to plot.
    """
    for column in df.columns:
        line_plot(df, column)


def line_plot(df: pd.DataFrame, column_name: str) -> None:
    """ 
    Plots a line chart of the provided column.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to plot.
    column : str
        The column to plot.
    """
    title = column_name.replace('_', ' ').title()
    fig = px.line(df, x=df.index, y=column_name, title=title)
    fig.update_traces(line=dict(width=4))
    fig.update_layout(xaxis_title='Cycle Number',
                      yaxis_title='Dooder Count')
    fig.show()


def plot_pct_difference(df, column_name):
    """
    Plot the % difference from the previous cycle for each cycle in the given dataframe
    for the given column name.

    Parameters:
    df (pandas.DataFrame): the dataframe to plot
    column_name (str): the name of the column to plot

    Returns:
    None
    """
    # Calculate the % difference from the previous cycle for each cycle
    pct_diff = df[column_name].pct_change() * 100
    title = column_name.replace('_', ' ').title()

    # Plot the % difference from the previous cycle for each cycle
    fig = px.line(pct_diff, x=pct_diff.index, y=column_name, title=title)
    fig.add_hline(y=0)
    # Add axis labels and a title
    fig.update_layout(xaxis_title='Cycle #',
                      yaxis_title='Percent Change',
                      yaxis_range=[-100, 100])
    fig.show()


#! yaml based chart settings.
#! chart_type, chart_title, x_axis_title, y_axis_title, x_axis_column, y_axis_column
