import numpy as np
import pandas as pd

from kmeans import kmeans
from knn import KNN

from sklearn.neighbors import KNeighborsClassifier as KNN_sk
from sklearn.cluster import KMeans as KMeans_sk

def confusion_matrix(y_true, y_pred):
    TP = np.sum((y_true == 1) & (y_pred == 1))
    FP = np.sum((y_true == 0) & (y_pred == 1))
    TN = np.sum((y_true == 0) & (y_pred == 0))
    FN = np.sum((y_true == 1) & (y_pred == 0))

    return np.array([[TN, FP], [FN, TP]])

def calc_metrics(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    TN, FP = cm[0]
    FN, TP = cm[1]

    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1 = 2 * (precision * recall) / (precision + recall)

    return cm, accuracy, precision, recall, f1

def main():
    print("=== Trabalho Prático II: Aprendizado de Máquina ===\nFeito por Gabriel Guimarães e João Pedro Smolinski\n")

    try:
        df_train = pd.read_csv("data/nba_treino.csv")
        df_test = pd.read_csv("data/nba_teste.csv")
    except FileNotFoundError:
        print("Erro: Arquivos CSV não encontados.")
        return
    
    X_train = df_train.drop(columns=['TARGET_5Yrs']).values
    y_train = df_train['TARGET_5Yrs'].values

    X_test = df_test.drop(columns=['TARGET_5Yrs']).values
    y_test = df_test['TARGET_5Yrs'].values

    print("--- 1. Experimentos com KNN ---")
    knn_k_values = [2, 10, 50, 13]

    for k in knn_k_values:
        print(f"\nAvaliando KNN para k = {k}...")

        knn_model = KNN(k=k)
        knn_model.fit(X_train, y_train)

        y_pred = knn_model.predict(X_test)

        knn_sk = KNN_sk(n_neighbors=k)
        knn_sk.fit(X_train, y_train)
        y_pred_sk = knn_sk.predict(X_test)

        cm, acc, prec, rec, f1 = calc_metrics(y_test, y_pred)

        TN, FP = cm[0, 0], cm[0, 1]
        FN, TP = cm[1, 0], cm[1, 1]

        cm_sk, acc_sk, prec_sk, rec_sk, f1_sk = calc_metrics(y_test, y_pred_sk)

        TN_sk, FP_sk = cm_sk[0, 0], cm_sk[0, 1]
        FN_sk, TP_sk = cm_sk[1, 0], cm_sk[1, 1]

        print("\nMatriz de Confusão (KNN do grupo):")
        print("             | Predito 0 | Predito 1 |")
        print("-------------+-----------+-----------+")
        print(f"  Real 0     | {TN:^9} | {FP:^9} | (TN / FP)")
        print("-------------+-----------+-----------+")
        print(f"  Real 1     | {FN:^9} | {TP:^9} | (FN / TP)")
        print("-------------+-----------+-----------+")

        print(f"Acurácia: {acc:.4f} | Precisão: {prec:.4f} | Recall: {rec:.4f} | F1: {f1:.4f}")

        print("---------------------------------------")
        print("\nMatriz de Confusão (KNN do Scikit-Learn):")
        print("             | Predito 0 | Predito 1 |")
        print("-------------+-----------+-----------+")
        print(f"  Real 0     | {TN_sk:^9} | {FP_sk:^9} | (TN / FP)")
        print("-------------+-----------+-----------+")
        print(f"  Real 1     | {FN_sk:^9} | {TP_sk:^9} | (FN / TP)")
        print("-------------+-----------+-----------+")

        print(f"Acurácia: {acc_sk:.4f} | Precisão: {prec_sk:.4f} | Recall: {rec_sk:.4f} | F1: {f1_sk:.4f}")

        mutual = (y_pred == y_pred_sk).sum()
        print(f">> As predições bateram {(100 * mutual / len(y_pred)):.2f}% com o Scikit-Learn")

    print("\n=====================================\n")

    print("--- 2. Experimentos com K-Means ---")

    df_all = pd.concat([df_train, df_test], ignore_index=True)

    feature_columns = df_all.drop(columns=['TARGET_5Yrs']).columns
    X_all = df_all.drop(columns=['TARGET_5Yrs']).values
    y_all = df_all['TARGET_5Yrs'].values

    kmeans_k_values = [2, 3]
    for k in kmeans_k_values:
        print(f"\nRodando K-Means para k = {k}...")

        centroids, groups = kmeans(X_all, k)

        kmeans_sk = KMeans_sk(n_clusters=k, random_state=42, n_init='auto')
        kmeans_sk.fit(X_all)
        centroids_sk = kmeans_sk.cluster_centers_
        groups_sk = kmeans_sk.labels_

        df_centroids = pd.DataFrame(
            centroids, 
            columns=feature_columns, 
            index=[f'Cluster {i}' for i in range(k)]
        )

        df_centroids_sk = pd.DataFrame(
            centroids_sk, 
            columns=feature_columns, 
            index=[f'Cluster {i}' for i in range(k)]
        )

        print("\n[Centróides Obtidos - KMeans do grupo]")
        print(df_centroids.T.round(2).to_string())

        print("\n[Centróides Obtidos - KMeans do Scikit-Learn]")
        print(df_centroids_sk.T.round(2).to_string())
        print("-" * 60)

        print("\nRelação dos grupos com a variável 'TARGET_5Yrs' (KMeans do grupo):")
        for i in range(k):
            cluster_labels = y_all[groups==i]
            qnt_class_0 = np.sum(cluster_labels == 0)
            qnt_class_1 = np.sum(cluster_labels == 1)
            total = len(cluster_labels)

            if total > 0:
                print(f"Cluster {i}: Total de jogadores = {total} -> {qnt_class_0} da classe 0 | {qnt_class_1} da classe 1")
            else:
                print(f"Cluster {i}: Vazio")

        print("\nRelação dos grupos com a variável 'TARGET_5Yrs' (KMeans do Scikit-Learn):")
        for i in range(k):
            cluster_labels_sk = y_all[groups_sk==i]
            qnt_class_0_sk = np.sum(cluster_labels_sk == 0)
            qnt_class_1_sk = np.sum(cluster_labels_sk == 1)
            total_sk = len(cluster_labels_sk)

            if total_sk > 0:
                print(f"Cluster {i}: Total de jogadores = {total_sk} -> {qnt_class_0_sk} da classe 0 | {qnt_class_1_sk} da classe 1")
            else:
                print(f"Cluster {i}: Vazio")

if __name__ == "__main__":
    main()