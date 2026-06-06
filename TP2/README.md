# Trabalho Prático II: Aprendizado de Máquina
## Introdução à Inteligência Artificial — UFMG

Esta pasta contém o código-fonte e as instruções para a execução do Trabalho Prático II. O objetivo deste trabalho é estudar técnicas de aprendizado supervisionado e não-supervisionado através da implementação e análise dos algoritmos **KNN** e **K-Means** do zero, bem como comparar seus resultados com as implementações da biblioteca `scikit-learn`.

---

## Estrutura do Projeto

O projeto está organizado da seguinte forma:
* `main.py`: Script principal unificado que gerencia o fluxo de execução, leitura dos datasets, invocação dos métodos desenvolvidos, cálculo de métricas e exibição das tabelas comparativas com o `scikit-learn`.
* `knn.py`: Script desenvolvido pelo grupo que implementa o algoritmo KNN usando apenas a biblioteca `numpy`.
* `kmeans.py`: Script desenvolvido pelo grupo que implementa o algoritmo K-Means usando apenas a biblioteca `numpy`.
* `requirements.txt`: Arquivo contendo as dependências de terceiros necessárias para carregar os dados e rodar os testes comparativos.
* `nba_treino.csv`: Dataset com 80% das observações usado para treinar o KNN e compor o K-Means.
* `nba_teste.csv`: Dataset com 20% das observações usado para testar o KNN e compor o K-Means.

---

## Pré-requisitos e Instalação

1. Certifique-se de ter o **Python 3.8+** instalado em seu sistema.
2. Certifique-se de estar no mesmo diretório que o arquivo `main.py` e que os arquivos `nba_treino.csv` e `nba_teste.csv`  estão dentro do diretório `data/`.

Para instalar as dependências necessárias para o projeto (Pandas, Numpy e Scikit-Learn), execute o comando abaixo no terminal:

```bash
pip install -r requirements.txt
```

> Qualquer outro comando de instalação de bibliotecas python deve funcionar
---

## Como Executar o Programa

Após garantir que as dependências estão devidamente instaladas e os arquivos CSV estão na mesma pasta, você pode iniciar o fluxo de experimentos rodando o seguinte comando:

```bash
python3 main.py
```

> Qualquer outro comando de execução de um arquivo python deve funcionar

### O que o programa faz ao ser executado:
1. **Parte 1 (Supervisionado - KNN):** Executa a implementação do grupo do KNN e a do `scikit-learn` para os valores de $k = \{2, 10, 50, 13\}$. Para cada um, calcula e imprime no terminal uma tabela formatada da Matriz de Confusão, seguida do comparativo de Acurácia, Precisão, Recall e F1-Score entre os dois modelos.
2. **Parte 2 (Não-Supervisionado - K-Means):** Agrupa o dataset unificado utilizando o K-Means do grupo e o do `scikit-learn` para $k = \{2, 3\}$. Exibe uma tabela vertical dos centróides obtidos para cada atributo e mostra a distribuição das classes reais de resposta (`TARGET_5Yrs`) dentro de cada grupo gerado.