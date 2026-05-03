import cv2
import numpy as np
from sklearn.cluster import KMeans

def extract_colors(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (150, 150))
    pixels = img.reshape(-1, 3)

    kmeans = KMeans(n_clusters=5, n_init=10)
    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_

    brightness = np.mean(colors)

    if brightness > 180:
        family = "light"
    elif brightness > 120:
        family = "medium"
    else:
        family = "dark"

    return colors.astype(int).tolist(), family