from HeraEngine.types.Vec2 import Vec2

def ease_in_out_quadratic_bezier(p0,p1,p2,t):
    d =  t * t * (3.0 - 2.0 * t)
    return bezier_quadratic(p0,p1,p2,d)

def bezier_quadratic(p0, p1, p2, t):

    if not isinstance(p0,Vec2):
        raise TypeError("P0 should be a Vec2")
    if not isinstance(p1,Vec2):
        raise TypeError("P1 should be a Vec2")
    if not isinstance(p2,Vec2):
        raise TypeError("P2 should be a Vec2")

    
    return (p0 * (1 - t) ** 2) + (p1 * 2 * (1 - t) * t) + (p2 * t ** 2)
