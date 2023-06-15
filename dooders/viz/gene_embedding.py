import plotly.express as px


embedding_map = {0: 'EmbeddingA', 1: 'EmbeddingB', 2: 'EmbeddingC'}


def gene_embedding(gene_embeddings_df, color_by='cycle', show_cbar=False) -> px.scatter:
    """ 
    Create a scatter plot of the gene embeddings.
    
    Parameters
    ----------
    gene_embeddings_df : pd.DataFrame
        A DataFrame containing the gene embeddings.
    color_by : str
        The column name to color the points by.
    show_cbar : bool
        Whether to show the colorbar.

    Returns
    -------
    fig : px.scatter
        The scatter plot.
    """
    # Create the scatter plot
    fig = px.scatter(gene_embeddings_df,
                     x="X",
                     y="Y",
                     color=color_by,
                     color_continuous_scale="Viridis")

    # Remove axis titles
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)

    # Remove tick labels
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    # Remove the color legend
    fig.update_layout(coloraxis_showscale=False)

    if show_cbar:
        fig.update_layout(coloraxis_colorbar=dict(
            title=color_by))

    return fig


# 1D, 2D, and 3D gene viz
#! should I scale the values? or are thet already
