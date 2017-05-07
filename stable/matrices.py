# -*- coding: utf-8 -*-
import sympy as sp
import random
import itertools as it
import copy
import jinja2

def genSymmetricMatrixWithDiagonalOne(n):
    result = []
    dim = n*(n-1)/2
    i = 0
    for r in range(1,n+1):
        row_aux = []
        for c in range(1,n+1):
            if c > r:
                row_aux.append(sp.Symbol('x{0}'.format(dim-i)))
                i+=1
            elif c < r:
                row_aux.append(0)
            else:
                row_aux.append(1)

        result.append(row_aux)
        del row_aux

    for r in range(n):
        for c in range(n):
            if c < r:
                result[r][c] = result[c][r]
 
    return sp.Matrix(result)

def genSymmetricMatrix(n):
    result = []
    for r in range(1,n+1):
        row_aux = []
        for c in range(1,n+1):
            if c >= r:
                row_aux.append(sp.Symbol('a{0}{1}'.format(r,c)))
            else:
                row_aux.append(sp.Symbol('a{0}{1}'.format(c,r)))

        result.append(row_aux)
        del row_aux
    return sp.Matrix(result)

def getCongruencyByDiagonal(m):
    m_copy = [list(m.row(i)) for i in range(m.rows)]
    dim = len(m_copy)
    for i in range(0,dim):
        for c in range(0,dim):
            m_copy[i][c]*=1/sp.sqrt(sp.Symbol('a{0}{1}'.format(i+1,i+1)))

        for r in range(0,dim):
            m_copy[r][i]*=1/sp.sqrt(sp.Symbol('a{0}{1}'.format(i+1,i+1)))

    return sp.Matrix(m_copy)

def getSubMatrices(m,o):
    dim = m.rows
    comb = list(it.combinations(range(dim),o))
    indexes = list(it.product(comb,comb))

    subMatrices  = []
    subMatriz_aux = []
    row = []

    for pair in indexes:
        for r in pair[0]:
            for c in pair[1]:
                row.append(m.row(r)[c])
            subMatriz_aux.append(list(row))
            del row[:]
        subMatrices.append(sp.Matrix(list(subMatriz_aux)))
        del subMatriz_aux[:]
    
    return subMatrices

def isaTotallyPositiveMatrix(m):
    return False not in [False not in [sp.det(y) > 0 for y in getSubMatrices(m,x)] for x in range(1,m.rows+1)]
    

def genReport(o):
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template("report.tex")


    symmetricMatrix = genSymmetricMatrix(o)
    congruentMatrix = getCongruencyByDiagonal(genSymmetricMatrix(o))

    context = {
        'orden': o,
        'symmetricmatrix': sp.latex(symmetricMatrix),
        'congruentmatrix': sp.latex(congruentMatrix)
    }

    tex = template.render(context)
    file = open(u'report/matrix_{0}x{1}.tex'.format(o, o), 'w')
    file.write(tex.encode('utf8'))
    file.close()

def getSubMatrixAsociated(m, entry):
    pos = [int(x) for x in str(entry.as_numer_denom()[0])[1:].split(',')]
    matrix = []
    row = []

    for r in pos:
        for c in pos:
            row.append(m.row(r-1)[c-1])
        matrix.append(list(row))
        del row[:]
    return matrix

def HadamardProduct(m1,m2):
	dim = m1.rows
	product = []
	row = []
	for r in range(dim):
		for c in range(dim):
			row.append(m1.row(r)[c]*m2.row(c)[c])
		product.append(list(row))
		del row[:]
	return sp.Matrix(product)

	def combinedMatrix(m):
		return HadamardProduct(m,m.inv().trasponse())

def getDifferentElements(l):
    aux1 = []
    aux2 = []
    
    for x in l:
        if x.det() not in aux1:
            aux1.append(x.det())
            aux2.append(x)

    return aux2

def genDiagonalMatrix(o, manual=False):
    result = []
    for r in range(1,o+1):
        row_aux = []
        for c in range(1,o+1):
            if c > r:
                row_aux.append(0)
            elif c < r:
                row_aux.append(0)
            else:
                row_aux.append(random.random() if manual==False else int(raw_input('D -> a{0}{1}: '.format(c,c))))

        result.append(row_aux)
        del row_aux
 
    return sp.Matrix(result)


def genLowerBiDiagonalMatrix(o, manual=False):
    result = []
    for r in range(1,o+1):
        row_aux = []
        for c in range(1,o+1):
            if c > r:
                row_aux.append(0)
            elif c < r:
                row_aux.append(0)
            else:
                row_aux.append(1)

        result.append(row_aux)
        del row_aux

    results = [copy.deepcopy(result) for x in range(1,o)]
    aux = {}

    for m in range(1,o):
        for k in range(m,o):        
            results[m-1][k][k-1] = random.random() if manual==False else int(raw_input('B{0} -> a{1}{2}: '.format(o-m, k+1,k)))
        aux['B{0}'.format(m)]= sp.Matrix(results[m-1])

    #return aux #[sp.Matrix(m) for m in results]
    f = [sp.Matrix(m) for m in results] #reversed([sp.Matrix(m) for m in results])
    f.reverse()
    return f

def genUpperBiDiagonalMatrix(o,manual=False):
    result = []
    for r in range(1,o+1):
        row_aux = []
        for c in range(1,o+1):
            if c > r:
                row_aux.append(0)
            elif c < r:
                row_aux.append(0)
            else:
                row_aux.append(1)

        result.append(row_aux)
        del row_aux

    results = [copy.deepcopy(result) for x in range(1,o)]
    aux = {}

    for m in range(1,o):
        for k in range(m,o):        
            results[m-1][k-1][k] = random.random() if manual==False else int(raw_input('C{0} -> a{1}{2}: '.format(o-m, k,k+1)))
        aux['C{0}'.format(o-m)]= sp.Matrix(results[m-1])

    #return aux #[sp.Matrix(m) for m in results]
    return [sp.Matrix(m) for m in results]

def genTotallyPositiveMatriz(o,manual=False):
    B = genLowerBiDiagonalMatrix(o,manual=manual)
    D = genDiagonalMatrix(o,manual=manual)
    C = genUpperBiDiagonalMatrix(o,manual=manual)

    aux = B + [D] + C
    return reduce((lambda x,y: x*y),aux)

def genReportMatrix(m,name):
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template("reportTotallyPositiveMatrix.tex")

    dim = m[0].rows
    dictMatricesInfo = [{'matriz':sp.latex(x),'submatrices':[{'sub':[{'matriz':sp.latex(y), 'det':sp.latex(y.det())} for y in getSubMatrices(x,o)],'orden':o} for o in range(1,dim+1)]} for x in m]
    #submatrices = [{'sub':[{'matriz':sp.latex(y), 'det':sp.latex(y.det())} for y in getSubMatrices(m,o)],'orden':o} for o in range(1,dim+1)]
    
    """
    context = {
        'matrix_orden': dim,
        'matrix': sp.latex(m),
        'submatrices': submatrices
    }
    """

    context = {
        'matrix_orden': dim,
        'matrix': dictMatricesInfo,
    }

    tex = template.render(context)
    file = open(u'subMatrices_report/{0}.tex'.format(name), 'w')
    file.write(tex.encode('utf8'))
    file.close()


def genReportAboutSubMatrices(m,o):
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template("report_sub.tex")

    dim = m.rows
    subMatrices = getSubMatrices(m,o)
    subMatricesDiff = getDifferentElements(subMatrices)
    dets = [x.det() for x in subMatricesDiff]

    latex_body = "".join(["\n$$"+sp.latex(subMatricesDiff[x])+" \hspace{2cm} "+sp.latex(dets[x])+"$$" for x in range(len(subMatricesDiff))])
    
    context = {
        'matrix_orden': dim,
        'submatrix_orden': o,
        'matrix': sp.latex(m),
        'submatrices': latex_body
    }

    tex = template.render(context)
    file = open(u'subMatrices_report/submatrices_{0}x{1}_of_{2}x{3}.tex'.format(o, o,dim,dim), 'w')
    file.write(tex.encode('utf8'))
    file.close()

