from sklearn.decomposition import PCA
from dooders.sdk.core.core import Core


@Core.register('strategy')
def pca_transform(weights) -> list:
    """ 
    """
    layer_pca = PCA(n_components=3)
    layer_pca.fit(weights)
    
    return layer_pca.singular_values_