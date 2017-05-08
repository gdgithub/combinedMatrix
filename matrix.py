import scipy
import random
import math

class Matrix(scipy.matrix):
    """
        Clase heredada de scipi.matrix la cual permite realizar las tareas tales como:
        1) Generar matrices simetricas
        2) Generar submatrices
        3) Determinar si una matriz es totalmente positiva
        4) Calcular la matriz combinada
        5) Generar una matriz totalmente positiva por medio de factores Bi, D, Ci
        6) Generar reportes acerca de matrices, sus submatrices y determinantes asociados
    """
    @staticmethod
    def create_symmetric_matrix(orden, arbitrary=True, aleatory=False,\
                                interval=[0,1], integerEntry=False,\
                                manualEntry=False):
        """
            Crea una matriz simetrica de orden n de la manera siguiente:
            1) En forma abitraria, utilizando entradas algebraicas. Es la opcion por defecto.
            2) Aleatoria entre dos numeros reales. Se requiere arbitrary=False
            3) Entrada por teclado.
        """
        result = []

        if arbitrary:
            result = [['a{0}{1}'.format(i+1, j+1) \
                if i <= j else 'a{0}{1}'.format(j+1, i+1) \
                for j in range(orden)] for i in range(orden)]
        else:
            if aleatory:
                result = scipy.zeros((orden, orden))

                for i in range(orden):
                    for j in range(i, orden):
                        value = interval[0] + (interval[1] - interval[0])*random.random()
                        result[i][j] = math.ceil(value) if integerEntry else value
                        result[j][i] = result[i][j]
            elif manualEntry:
                result = [[float(raw_input('a{0}{1}: '.format(i+1, j+1)))  \
                    for j in range(orden)] for i in range(orden)]

        return Matrix(result)

    def get_congruent_matrix_with_diagonal_one(self):
        """
            Devuelve una matriz congruente a esta matriz con entradas en la
            diagonal principal iguales a 1
        """
        pass