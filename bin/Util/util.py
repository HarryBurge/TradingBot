import numpy

def line_of_best_fit(*args):

    yvector = []
    xmatrix = []

    for x,y in args:
        yvector.append([round(y, 4)])
        xmatrix.append([x, 1])

    yvector = numpy.array(yvector)
    xmatrix = numpy.array(xmatrix)

    try:
        theta_hat = numpy.linalg.inv(xmatrix.T @ xmatrix) @ xmatrix.T @ yvector
        theta_hat = theta_hat.tolist()

    except numpy.linalg.LinAlgError:
        return [[0],[0]]

    return theta_hat


def gradient_of_points(points, num_nodes_gradient):

    # print(points, type(points),  num_nodes_gradient)
    if num_nodes_gradient % 2 == 0 and num_nodes_gradient > 1:
        return False
    elif len(points) < num_nodes_gradient+2:
        return []
    
    gradient_points = []

    for index, point in enumerate(points):
        
        if index < num_nodes_gradient//2:
            gradient_points.append(line_of_best_fit(*[(x, points[x]) for x in range(num_nodes_gradient//2+1)])[0][0])

        elif index > len(points) - num_nodes_gradient//2 -1:
            gradient_points.append(line_of_best_fit(*[(x, points[x]) for x in range(-num_nodes_gradient//2, 0, 1)])[0][0])

        else:
            gradient_points.append(line_of_best_fit(*[(x, points[x]) for x in range(index-num_nodes_gradient//2, index+num_nodes_gradient//2+1, 1)])[0][0])

    return gradient_points


def points_of_gradient_change(points, num_nodes_gradient):

    if num_nodes_gradient % 2 == 0 and num_nodes_gradient > 1:
        return False
    elif len(points) < num_nodes_gradient+2:
        return []

    dxdy = gradient_of_points(points, num_nodes_gradient)
    d2xdy2 = gradient_of_points(dxdy, num_nodes_gradient)

    peaks = []

    for index, point in enumerate(d2xdy2):
        if round(point, 2) == 0:
            peaks.append(index)

    return peaks
