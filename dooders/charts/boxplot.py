import pandas as pd
import plotly.express as px


def starting_success_probability(dooder_df: pd.DataFrame) -> px.box:
    """ 
    Creates a boxplot of the starting success probability by experiment result.

    Parameters
    ----------
    dooder_df : pd.DataFrame
        The DataFrame containing the information about the dooders.

    Returns
    -------
    fig : px.box
        The boxplot of the starting success probability by experiment result.
    """

    category_order = ['FailedEarly', 'Failed', 'Passed']

    fig = px.box(dooder_df, y='starting_success_probability',
                 x='experiment_result', color='experiment_result')

    # Update title
    fig.update_layout(
        title="Starting Success Probability by Experiment Result")

    # Update x-axis label
    fig.update_xaxes(title="")

    # Update y-axis label
    fig.update_yaxes(title="Starting Success Probability")

    # Remove legend
    fig.update_layout(showlegend=False)

    return fig
