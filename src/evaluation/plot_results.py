import matplotlib.pyplot as plt

def plot_displacement_curve(displacements, save_path):
    plt.figure(figsize=(10,5))
    plt.plot(displacements)
    plt.xlabel("Frame")
    plt.ylabel("Subpixel Displacement (px)")
    plt.title("Subpixel Motion Curve")
    plt.grid(True)
    plt.savefig(save_path)
    plt.close()
