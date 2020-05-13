import numpy as np

vect = np.array([1,2,3,4,5])

def vanderbro(vector):
    vander_bro_matr = np.zeros(vector.shape[0] * vector.shape[0])
    vander_bro_matr = vander_bro_matr.reshape(vector.shape[0], vector.shape[0])
    for i in range(vector.shape[0]):
        vander_bro_matr[i:i+1,:] = pow(vector, i)
    return  vander_bro_matr

print(vanderbro(vect))

'''Определитель моей матрицы равен определителю np.vander(vect) и определителю, представленному в Википедии: 288'''
