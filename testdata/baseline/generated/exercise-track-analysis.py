def distance_summary(points):
    total = 0.0
    for previous, current in zip(points, points[1:]):
        total += distance(previous, current)
    return total
