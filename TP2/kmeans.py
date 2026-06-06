import numpy as np

def kmeans(D, k, epsilon = 1e-4, max_iter = 300):
    """
    Implementação do algoritmo de k-Means

    Parâmetros:
    D: dataset
    k: número de clusters
    epsilon: critério de parada
    max_iter: número máximo de iterações
    """
    
    n_samples, n_features = D.shape

    # Pega uma amostra de tamanho k dos dados para serem os centroides iniciais
    random_start = np.random.choice(n_samples, k, replace=False)
    centroids = D[random_start]

    t = 0
    while t < max_iter:
        t += 1

        # Calcula a distância de cada ponto para cada centroide e escolhe o mais próximo
        distances = np.linalg.norm(D[:, np.newaxis] - centroids, axis=2)**2
        clusters = np.argmin(distances, axis=1)

        # Atualização dos centroides
        new_centroids = np.zeros((k, n_features))
        for i in range(k):
            points_in_cluster = D[clusters==i]

            if len(points_in_cluster > 0):
                new_centroids[i] = np.mean(points_in_cluster, axis=0)
            else:
                new_centroids[i] = centroids[i]
            
        shift = np.sum(np.linalg.norm(new_centroids - centroids, axis=1)**2)

        centroids = new_centroids

        if shift <= epsilon:
            break
    
    return centroids, clusters