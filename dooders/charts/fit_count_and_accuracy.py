from typing import List

import plotly.graph_objects as go


def fit_count_and_accuracy(fit_dooder_count: List, avg_accuracies: List) -> None:
    """
    Creates a dual-axis line chart comparing the count of fit Dooders 
    and the average accuracy of the Dooders in the gene pool after each 
    generation.
    
    Parameters
    ----------
    fit_dooder_count : list
        A list of the count of fit Dooders after each generation.
    avg_accuracies : list
        A list of the average accuracy of the Dooders in the gene pool after
        each generation.
    """

    # Create a list of generations
    generations = list(range(1, len(fit_dooder_count)+1))

    # Create a line chart
    fig = go.Figure()

    # Add a bar chart for the second set of values
    fig.add_trace(go.Bar(x=generations, y=avg_accuracies,
                  yaxis='y2', name='Bar Chart', opacity=0.4))

    fig.add_trace(go.Scatter(x=generations, y=fit_dooder_count,
                  mode='lines+markers', name='Line Chart'))

    # Update layout for secondary y-axis
    fig.update_layout(
        yaxis=dict(
            title='Fit Dooders'
        ),
        yaxis2=dict(
            title='Average Accuracy',
            overlaying='y',
            side='right',
            range=[0, 100],
            showgrid=False
        ),
        title='Fit Count and Average Accuracy',
        xaxis_title='Generation',
        showlegend=False,
    )

    fig.show()
