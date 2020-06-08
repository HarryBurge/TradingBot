import numpy

def line_of_best_fit(*args):

    yvector = []
    xmatrix = []

    for x,y in args:
        yvector.append([y])
        xmatrix.append([x, 1])

    yvector = numpy.array(yvector)
    xmatrix = numpy.array(xmatrix)

    try:
        theta_hat = numpy.linalg.inv(xmatrix.T @ xmatrix) @ xmatrix.T @ yvector
        theta_hat = theta_hat.tolist()

    except numpy.linalg.LinAlgError:
        return [[0],[0]]

    return theta_hat