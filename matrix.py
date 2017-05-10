import sympy
import random
import math
import itertools as it

class Matrix(sympy.Matrix):
    """
        Clase heredada de sympy.Matrix la cual permite realizar las tareas tales como:
        1) Generar matrices simetricas
        2) Generar submatrices
        3) Determinar si una matriz es totalmente positiva
        4) Calcular la matriz combinada
        5) Generar una matriz totalmente positiva por medio de factores Bi, D, Ci
        6) Generar reportes acerca de matrices, sus submatrices y determinantes asociados
    """
    #matrix = None

    """
    def __init__(self,matrix):
        self.matrix = sympy.Matrix(matrix)
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
            if aleatory or manualEntry:
                result = [[0 for j in range(orden)]\
                            for i in range(orden)]

                for i in range(orden):
                    for j in range(i, orden):
                        if manualEntry:
                            value = float(raw_input('a{0}{1}: '.format(i+1, j+1)))
                        else:
                            value = interval[0] + (interval[1] - interval[0])*random.random()
                        result[i][j] = math.ceil(value) if integerEntry else value
                        result[j][i] = result[i][j]
        return Matrix(result)

    def get_congruent_matrix_with_diagonal_one(self):
        """
            Devuelve una matriz congruente a esta matriz con entradas en la
            diagonal principal iguales a 1
        """
        auxMatrix = self.tolist()
        dim = len(auxMatrix)

        for i in range(dim):
            for c in range(dim):
                auxMatrix[i][c] *= 1/sympy.sqrt(self.row(i)[i])
            for r in range(dim):
                auxMatrix[r][i] *= 1/sympy.sqrt(self.row(i)[i])

        return Matrix(auxMatrix)

    def get_submatrices(self, rows, cols):
        """
            Obtiene las submatrices del orden especificado
        """
        I = list(it.combinations(range(self.rows), rows))
        J = list(it.combinations(range(self.cols), cols))

        indexes = list(it.product(I, J))

        subMatrices = []
        subMatriz_aux = []
        row = []

        for pair in indexes:
            for r in pair[0]:
                for c in pair[1]:
                    row.append(self.row(r)[c])
                subMatriz_aux.append(list(row))
                del row[:]
            subMatrices.append(Matrix(list(subMatriz_aux)))
            del subMatriz_aux[:]
        return subMatrices

    def combined_matrix(self):
        """
            Devuelve la matriz combinada de la matriz dada 
        """
        return Matrix.multiply_elementwise(self, self.inv().T)