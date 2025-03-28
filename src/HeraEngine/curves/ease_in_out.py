def ease_in_out(A, B, t):
    t = max(0, min(1, t))  
    d = t * t * t * (t * (t * 6 - 15) + 10)  
    return A + (B - A) * d
