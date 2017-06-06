import jinja2

def templateLoader(templateName):
    templateLoad = jinja2.FileSystemLoader(searchpath="./template/")
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

    

