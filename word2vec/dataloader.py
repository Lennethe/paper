import numpy as np
from keras.datasets import mnist
import gensim 

def load_v(n_sample):
    (_, _), (X_test, y_test) = mnist.load_data()
    X = np.zeros((n_sample * 10, X_test.shape[1], X_test.shape[2]))
    y = np.zeros(n_sample*10)
    for num in range(10):
        dest_indices = np.arange(num*n_sample, (num+1)*n_sample)
        source_indices = np.where(y_test == num)[0][:n_sample]
        X[dest_indices, :, :] = X_test[source_indices, :, :]
        y[dest_indices] = y_test[source_indices]
    return X, y


def load_visualize_data(dic):
    X = np.zeros((len(dic),300))
    model = gensim.models.Word2Vec.load('ja.bin')
    for num in range(len(dic)):
        X[num] = model[dic[num]]
    return X