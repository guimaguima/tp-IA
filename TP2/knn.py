import numpy as np

class KNN:
    def __init__(self, k):
        self.k = k
    
    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train

    def predict(self, X_test):
        predictions = [self._predict_single(x) for x in X_test]
        return np.array(predictions)
    
    def _predict_single(self, x):
        # Calcula a distância do ponto a todos os outros
        distances = [np.sqrt(np.sum((x - x_train)**2)) for x_train in self.X_train]

        # Pega os k mais próximos e suas labels
        k_index = np.argsort(distances)[:self.k]
        k_nearest_labels = [self.y_train[i] for i in k_index]

        # Conta a quantidade de labels de cada classe e retorna a mais presente
        unique_class, counts = np.unique(k_nearest_labels, return_counts=True)
        most_common_index = np.argmax(counts)
        most_common = unique_class[most_common_index]

        return most_common