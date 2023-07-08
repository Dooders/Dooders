import pandas as pd
import plotly.graph_objects as go

from dooders.data.experiment_results import min_max_avg_per_cycle


def accuracy_range_by_cycle(inference_df: pd.DataFrame) -> go.Figure:
    """ 

    Parameters
    ----------
    inference_df : pd.DataFrame
        The inference dataframe
    """

    cycle_tuples = min_max_avg_per_cycle(inference_df)

    min_values = [x[0] for x in cycle_tuples]
    max_values = [x[1] for x in cycle_tuples]
    avg_values = [x[2] for x in cycle_tuples]

    # Creating the x-axis values
    x_values = list(range(len(cycle_tuples)))

    # Creating the figure and adding traces
    fig = go.Figure()

    # Adding the area chart for min and max values
    fig.add_trace(go.Scatter(
        x=x_values + x_values[::-1],  # Create a closed area
        y=min_values + max_values[::-1],
        fill='toself',
        mode='none',
        fillcolor='rgba(0, 176, 246, 0.2)',
        name='Min-Max Range'
    ))

    # Adding the line chart for average values
    fig.add_trace(go.Scatter(
        x=x_values,
        y=avg_values,
        mode='lines',
        name='Average'
    ))

    # Updating layout
    fig.update_layout(
        title='Average Accuracy With Ranges',
        xaxis_title='Cycle Number',
        yaxis_title='Average Accuracy'
    )

    return fig
