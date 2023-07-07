import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def death_age_by_cycle(dooder_df: pd.DataFrame) -> go.Figure:
    """ 
    Creates a histogram of the age of death by cycle.

    Parameters
    ----------
    dooder_df : pd.DataFrame
        The DataFrame containing the information about the dooders.

    Returns
    -------
    figure : go.Figure
        The histogram of the age of death by cycle.
    """

    ages = list(dooder_df['age'])

    # Create a histogram trace
    trace = go.Histogram(x=ages)

    # Create a layout
    layout = go.Layout(
        title='Histogram of Dooder by termination cycle',
        title_font=dict(family='Roboto-Bold'),
        xaxis=dict(
            title='Cycle Number',
            title_font=dict(family='Roboto-Bold'),
            tickfont=dict(family='Roboto-Bold')
        ),
        yaxis=dict(
            title='Counts',
            title_font=dict(family='Roboto-Bold'),
            tickformat=',d',
            tickfont=dict(family='Roboto-Bold')
        )
    )

    # Create a Figure object
    figure = go.Figure(data=[trace], layout=layout)

    return figure


def starting_success_probability(dooder_df: pd.DataFrame) -> go.Figure:
    """ 
    Creates a histogram of the success probability of the dooders.

    Parameters
    ----------
    dooder_df : pd.DataFrame
        The DataFrame containing the information about the dooders.

    Returns
    -------
    figure : go.Figure
        The histogram of the success probability of the dooders.
    """

    fig = px.histogram(
        dooder_df, x="starting_success_probability", color='experiment_result')

    # Update title
    fig.update_layout(title="Histogram of Starting Success Probability")

    # Update x-axis label
    fig.update_xaxes(title="Starting Success Probability")

    # Update y-axis label
    fig.update_yaxes(title="Dooder Count")

    return fig
