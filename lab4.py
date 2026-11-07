import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from scipy.spatial import Voronoi, voronoi_plot_2d

# зчитування координат з файлу
points_list = []
with open('DS4.txt', 'r') as file:
    for line in file:
        coords = line.split()
        if len(coords) == 2:
            points_list.append([int(coords[0]), int(coords[1])])
            
points = np.array(points_list)

# пошук зв'язаних областей
grid = np.zeros((points[:, 0].max() + 2, points[:, 1].max() + 2), dtype=bool)
grid[points[:, 0], points[:, 1]] = True

labels, n_regions = ndimage.label(grid, structure=np.ones((3, 3)))
point_labels = labels[points[:, 0], points[:, 1]]

# обчислення центрів ваги для кожної області
centroids = np.array([points[point_labels == k].mean(axis=0) for k in range(1, n_regions + 1)])

# збереження центрів у текстовий файл
with open('centroids_DS4.txt', 'w') as f_out:
    for cx, cy in centroids:
        f_out.write(f"{cx:.2f} {cy:.2f}\n")

# діаграма Вороного
vor = Voronoi(centroids)

def setup_canvas():
    plt.figure(figsize=(9.6, 5.4), dpi=100)
    plt.scatter(points[:, 0], points[:, 1], color="black", s=5, alpha=0.1, linewidths=0)

# центри ваги
setup_canvas()
plt.scatter(centroids[:, 0], centroids[:, 1], color='red', s=25, zorder=3)
plt.xlim(0, 960)
plt.ylim(0, 540)
plt.savefig('result_lab4_centroids.png')
plt.close()

# центри ваги та діаграма Вороного
setup_canvas()
ax = plt.gca()
voronoi_plot_2d(vor, ax=ax, show_points=False, show_vertices=False, line_colors='blue', line_width=1.5, line_alpha=0.9)
plt.scatter(centroids[:, 0], centroids[:, 1], color='red', s=25, zorder=3)
plt.xlim(0, 960)
plt.ylim(0, 540)
plt.savefig('result_lab4.png')
plt.close()

print(f"Знайдено зв'язаних областей: {n_regions}")
print("Файли centroids_DS4.txt, result_lab4_centroids.png та result_lab4.png успішно збережено.")