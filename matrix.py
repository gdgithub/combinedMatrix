"""
Libreria Matrix la cual contiene la clase Matrix. Esta permite interactuar con
las matrices de Sympy y extiende sus metodos.abs

Autor: Ivan Gil Cruz
"""
import sympy
import random
import math
import itertools as it
import copy
import reports


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
    def create_symmetric_matrix(orden, arbitrary=True, fiedlerMatrix=False, aleatory=False,
                                interval=[0, 1], integerEntry=False,
                                manualEntry=False):
        """
            Crea una matriz simetrica de orden n de la manera siguiente:
            1) En forma abitraria, utilizando entradas algebraicas. Es la opcion por defecto.
            2) Aleatoria entre dos numeros reales. Se requiere arbitrary=False
            3) Entrada por teclado.
        """
        result = []

        if arbitrary:
            if not fiedlerMatrix:
                result = [['a{0}{1}'.format(i + 1, j + 1)
                           if i <= j else 'a{0}{1}'.format(j + 1, i + 1)
                           for j in range(orden)] for i in range(orden)]
            else:
                num = orden * (orden - 1) / 2
                result = Matrix.create_symmetric_matrix(orden).tolist()
                i = 0
                for r in range(orden):
                    result[r][r] = 1
                    for c in range(r + 1, orden):
                        result[r][c] = sympy.Symbol('x{0}'.format(num - i))
                        result[c][r] = result[r][c]
                        i += 1
        else:
            if aleatory or manualEntry:
                result = [[0 for j in range(orden)]
                          for i in range(orden)]

                for i in range(orden):
                    for j in range(i, orden):
                        if manualEntry:
                            value = float(
                                raw_input('a{0}{1}: '.format(i + 1, j + 1)))
                        else:
                            value = interval[
                                0] + (interval[1] - interval[0]) * random.random()
                        result[i][j] = math.ceil(
                            value) if integerEntry else value
                        result[j][i] = result[i][j]
        return Matrix(result)

    @staticmethod
    def create_diagonal_matrix(orden, manualEntry=False,
                                interval=[0, 1], integerEntry=False, identity=True):
        """
            Devuelve una matriz diagonal. Por defecto retorna la identidad.
            Admite un argumento manualEntry para entrada manual y aleatory de 
            manera aleatoria. Ademas, si se especifica el rango se obtienen
            numeros aleatorios comprendidos en ese rango. El argumento integerEntry 
            establece entradas enteras en la matriz.
        """
        aux = Matrix.create_symmetric_matrix(orden).tolist()

        for i in range(orden):
            for j in range(orden):
                if i == j:
                    if identity:
                        value = 1
                    elif manualEntry:
                        value = float(raw_input('D --> a{0}{1}: '.format(i + 1, j + 1)))
                    else:
                        value = interval[0] + (interval[1] - interval[0]) * random.random()
                    aux[i][j] = math.ceil(value) if integerEntry else float(value)
                else:
                    aux[i][j] = 0
        return Matrix(aux)

    def get_congruent_matrix_with_diagonal_one(self):
        """
            Devuelve una matriz congruente a esta matriz con entradas en la
            diagonal principal iguales a 1
        """
        auxMatrix = self.tolist()
        dim = len(auxMatrix)

        for i in range(dim):
            for c in range(dim):
                auxMatrix[i][c] *= 1 / sympy.sqrt(self.row(i)[i])
            for r in range(dim):
                auxMatrix[r][i] *= 1 / sympy.sqrt(self.row(i)[i])

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

    def get_submatrices_summary(self, orden, latex=False):
        """
            Obtiene un arreglo de diccionarios formados por
            un matriz cuadrada y un determinante. 
        """
        submatrices = self.get_submatrices(orden, orden)
        if latex:
            return [{'submatrix': sympy.latex(m), 'det': sympy.latex(m.det())} for m in submatrices]
        else:
            return [{'submatrix': m, 'det': m.det()} for m in submatrices]

    def get_all_submatrices_summary(self, symmetric=False, report=False):
        """
            Devuelve todas las submatrices de una matriz cuadrada
            junto a sus determinantes
        """
        orden = self.rows
        result = {'matrix': self, 'allsubmatrices': [{'orden': x, 
                    'submatrices': Matrix.different_element_in_array_of_dict(self.get_submatrices_summary(x), 'det') 
                                    if symmetric else 
                                        self.get_submatrices_summary(x)} 
                                    for x in range(1, orden+1)]}
        if report:
            dictMatrixInfo = {'matrix': sympy.latex(self), 'allsubmatrices': [{'orden': x, 
                    'submatrices': Matrix.different_element_in_array_of_dict(self.get_submatrices_summary(x, latex=True), 'det') 
                                    if symmetric else 
                                        self.get_submatrices_summary(x, latex=True)} 
                                    for x in range(1, orden+1)]}
            reports.sub_matrices(orden, dictMatrixInfo)

        return result 

    @staticmethod
    def different_element_in_array_of_dict(array, key):
        """
            Dada una lista de diccionarios y una clave especifica.abs
            Se retorna una lista de diccionarios que no repite la clave
            dada.
        """
        keyAux = []
        result = []
        for d in array:
            if d[key] not in keyAux:
                keyAux.append(d[key])
                result.append(d)
        return result

    def combined_matrix(self):
        """
            Devuelve la matriz combinada de la matriz dada 
        """
        return Matrix.multiply_elementwise(self, self.inv().T)

    def is_totally_positive_matrix(self):
        """
            Devuelve si la matriz es totalmente positiva
        """
        return False not in [False not in [y.det() > 0
                                           for y in self.get_submatrices(x, x)]
                             for x in range(1, self.rows + 1)]

    @staticmethod
    def get_matrices_with_different_det(arrayMatrices):
        """
            Devuelve, dada una lista de matrices, aquellas sin
            repetir el determinante
        """
        auxMatrix = []
        auxDet = []

        for m in arrayMatrices:
            if m.det() not in auxDet:
                auxDet.append(m.det())
                auxMatrix.append(m)
        return auxMatrix

    @staticmethod
    def get_diagonals_entries(orden, pos):
        """
            Retorna los elementos de la diagonal en la posicion pos
        """
        return [(i, i+pos) for i in range(orden - pos)]

    @staticmethod
    def get_new_entry_fiedler_matrix(aux, pos):
        i, j = pos
        a11 = aux[i][j-1]
        a12 = aux[i][j]
        a21 = aux[i+1][j-1]
        a22 = aux[i+1][j]

        return random.random()*(a11*a22)/a21
    
    @staticmethod
    def create_lower_bidiagonal_matrix(orden, interval=[0, 1], manualEntry=False,
                                       integerEntry=False):
        """
            Retorna la matriz bidiagonal inferior del orden especificado,
            la cual es requerida para contruir una matriz totalmente positiva.
            Entre los argumentos tenemos la posibilidad tener entradas aleatorias, 
            por defecto. Ademas de poder ingresarlas manualmente.            
        """
        result = []
        for r in range(1, orden + 1):
            row_aux = []
            for c in range(1, orden + 1):
                if c > r:
                    row_aux.append(0)
                elif c < r:
                    row_aux.append(0)
                else:
                    row_aux.append(1)

            result.append(row_aux)
            del row_aux

        results = [copy.deepcopy(result) for x in range(1, orden)]
        aux = {}

        for m in range(1, orden):
            for k in range(m, orden):
                value = interval[0] + (interval[1] - interval[0]) * random.random(
                ) if manualEntry == False else float(raw_input('B{0} -> a{1}{2}: '.format(orden - m, k + 1, k)))
                results[m - 1][k][k -
                                  1] = math.ceil(value) if integerEntry else value
            aux['B{0}'.format(m)] = Matrix(results[m - 1])

        # return aux #[sp.Matrix(m) for m in results]
        # reversed([sp.Matrix(m) for m in results])
        f = [Matrix(m) for m in results]
        f.reverse()
        return f

    @staticmethod
    def create_upper_bidiagonal_matrix(orden, interval=[0, 1], manualEntry=False,
                                integerEntry=False):
        """
            Retorna la matriz bidiagonal superior del orden especificado,
            la cual es requerida para contruir una matriz totalmente positiva.
            Entre los argumentos tenemos la posibilidad tener entradas aleatorias, 
            por defecto. Ademas de poder ingresarlas manualmente.            
        """
        result = []
        for r in range(1, orden + 1):
            row_aux = []
            for c in range(1, orden + 1):
                if c > r:
                    row_aux.append(0)
                elif c < r:
                    row_aux.append(0)
                else:
                    row_aux.append(1)

            result.append(row_aux)
            del row_aux

        results = [copy.deepcopy(result) for x in range(1, orden)]
        aux = {}

        for m in range(1, orden):
            for k in range(m, orden):
                value = interval[0] + (interval[1] - interval[0]) * random.random() if manualEntry == False else float(raw_input('C{0} -> a{1}{2}: '.format(orden - m, k, k + 1)))
                results[m - 1][k - 1][k] = math.ceil(value) if integerEntry else value
            aux['C{0}'.format(orden - m)] = Matrix(results[m - 1])

        # return aux #[sp.Matrix(m) for m in results]
        return [Matrix(m) for m in results]

    @staticmethod
    def create_totally_positive_matrix(orden, interval=[0, 1], manualEntry=False, 
                            integerEntry=False, symmetric=False, report=False):
        """
            Retorna una matriz combinada construida por medio de factores matriciales 
            bidiagonales.
        """
        B = Matrix.create_lower_bidiagonal_matrix(orden, interval=interval, manualEntry=manualEntry, integerEntry=integerEntry)
        D = Matrix.create_diagonal_matrix(orden, manualEntry=manualEntry, interval=interval, integerEntry=integerEntry, identity=False)
        if symmetric:
            C = [x.T for x in B]
            C.reverse()
        else:
            C = Matrix.create_upper_bidiagonal_matrix(orden, interval=interval, manualEntry=manualEntry, integerEntry=integerEntry)
        
        aux = B + [D] + C
        prod = reduce((lambda x, y: x * y), aux)

        return {'product': prod, 'factors': aux}

    @staticmethod
    def create_totally_positive_matrix_with_diagonal_one(orden=3):
        auxMatrix = Matrix.create_diagonal_matrix(orden).tolist()
        fixedEntries = [(i,j) for i in range(orden - 2) for j in range(i+2, orden)]
        freeEntries = [(i,i+1) for i in range(orden - 1)]

        for entry in freeEntries:
            i, j = entry
            auxMatrix[i][j] = random.random()
            auxMatrix[j][i] = auxMatrix[i][j]

        for i in range(2, orden):
            for pos in Matrix.get_diagonals_entries(orden, i):
                i, j = pos
                auxMatrix[i][j] = Matrix.get_new_entry_fiedler_matrix(auxMatrix, pos)
                auxMatrix[j][i] = auxMatrix[i][j]
        tmp = Matrix(auxMatrix)

        return tmp if tmp.det() > 0 else Matrix.create_totally_positive_matrix_with_diagonal_one(orden)