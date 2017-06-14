import jinja2
import os

def templateLoader(templateName):
    templateLoad = jinja2.FileSystemLoader(searchpath="./templates/")
    templateEnv = jinja2.Environment(loader=templateLoad)
    return templateEnv.get_template(templateName)

def totally_positive_matrix(orden, matrix, symmetric=False):
    template = templateLoader("totallyPositiveMatrixWithFactors.tex")
    
    Bi = ['B_{'+str(x)+'}' for x in range(1,orden)]
    if symmetric:
        Ci = [x+'^{T}' for x in Bi]
    else:
        Ci = ['C_{'+str(orden - x)+'}' for x in range(1,orden)]
    
    tmp = Bi + ['D'] + Ci
    factorization = "".join(tmp)

def sub_matrices(orden, dictMatrixInfo, name='0'):
    context = {
        'matrix_orden': orden,
        'matrix': dictMatrixInfo
    }

    template = templateLoader('subMatrices.tex')
    tex = template.render(context)
    file = open(u'Reports/allSubMatrices_{0}.tex'.format(name), 'w')
    file.write(tex.encode('utf8'))
    file.close()
    #os.system('')


    

