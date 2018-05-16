import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [0,
              255,
              255]]
    areflect = [0.1,
                0.1,
                0.1]
    dreflect = [0.5,
                0.5,
                0.5]
    sreflect = [0.5,
                0.5,
                0.5]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 20
    polygons = []
    edges = []

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
        print commands 
        for c in commands: 
            if c[0] == 'push': 
                stack.append( [x[:] for x in stack[-1]] )
            elif c[0] == 'pop': 
                stack.pop() 
            elif c[0] == 'save': 
                save_extension(screen, c[1] + c[2])
            elif c[0] == 'display': 
                display(screen)
            elif c[0] == 'sphere': 
                add_sphere(polygons,
                       float(c[1]), float(c[2]), float(c[3]),
                       float(c[4]), step_3d)
                matrix_mult( stack[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []
            elif c[0] == 'torus':
                add_torus(polygons,
                      float(c[1]), float(c[2]), float(c[3]),
                      float(c[4]), float(c[5]), step_3d)
                matrix_mult( stack[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []
            elif c[0] == 'box':
                add_box(polygons,
                    float(c[1]), float(c[2]), float(c[3]),
                    float(c[4]), float(c[5]), float(c[6]))
                matrix_mult( stack[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []
            elif c[0] == 'line': 
                add_edge( edges,
                      float(c[1]), float(c[2]), float(c[3]),
                      float(c[4]), float(c[5]), float(c[6]) )
                matrix_mult( stack[-1], edges )
                draw_lines(edges, screen, zbuffer, color)
                edges = []
            elif c[0] == "move":
                t = make_translate(float(c[1]), float(c[2]), float(c[3]))
                matrix_mult( stack[-1], t )
                stack[-1] = [ x[:] for x in t]
            elif c[0] == "scale":
                t = make_scale(float(c[1]), float(c[2]), float(c[3]))
                matrix_mult( stack[-1], t )
                stack[-1] = [ x[:] for x in t]
            elif c[0] == "rotate":
                theta = float(c[2]) * (math.pi / 180)
                if c[1] == 'x':
                    t = make_rotX(theta)
                elif c[1] == 'y':
                    t = make_rotY(theta)
                else:
                    t = make_rotZ(theta)
                matrix_mult( stack[-1], t )
                stack[-1] = [ x[:] for x in t]

    else:
        print "Parsing failed."
        return
