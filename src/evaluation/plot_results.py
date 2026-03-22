import matplotlib

def plot_displacement_curve(displacements, save_path):
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.switch_backend('Agg')
    
    plt.figure(figsize=(10,5))
    plt.plot(displacements)
    plt.xlabel("Frame")
    plt.ylabel("Subpixel Displacement (px)")
    plt.title("Subpixel Motion Curve")
    plt.grid(True)
    plt.savefig(save_path)
    plt.close('all')
