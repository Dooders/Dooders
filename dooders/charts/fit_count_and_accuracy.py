from typing import List, Union

import plotly.graph_objects as go


def fit_count_and_accuracy(fit_dooder_count: List,
                           avg_accuracies: List,
                           save_path: Union[str, None] = None) -> None:
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
    save_path : str, optional
        The path to save the chart to (default is None). If None, the chart
        is displayed only. If not None, the chart is saved to the path.
    """

    # Create a list of generations
    generations = list(range(1, len(fit_dooder_count)+1))

    # Create a line chart
    fig = go.Figure()

    # Add a bar chart for the second set of values
    fig.add_trace(go.Bar(x=generations, y=avg_accuracies,
                  yaxis='y2', name='Average Accuracy', opacity=0.4))

    fig.add_trace(go.Scatter(x=generations, y=fit_dooder_count,
                  mode='lines+markers', name='Fit Dooders'))

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
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    if save_path is not None:
        fig.write_image(f'{save_path}fit_count_and_accuracy.png',
                        format='png',
                        scale=2,
                        engine='orca')

    fig.show()
