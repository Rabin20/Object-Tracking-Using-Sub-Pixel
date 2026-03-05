def update_roi(bbox, cx, cy):
    x, y, w, h = bbox
    new_x = int(x + cx - w/2)
    new_y = int(y + cy - h/2)
    return (new_x, new_y, w, h)
