import cv2
import numpy as np

# Function to apply homography and coordinate transformation
def apply_homography_and_transformation(H, T, u, v):
    transformed_u, transformed_v = np.dot(T, np.array([u, v]))
    uv = np.array([transformed_u, transformed_v, 1])
    x, y, w = np.dot(H, uv)
    return x / w, y / w

# Sample pixel space points (u, v) and real space points (x, y)
pixel_points = [(679, 44), (776, 130), (773, 344), (963, 172), (1205, 70), (1127, 344) ]
real_world_points = [(979.2, 1068.4), (724.3, 777.7), (81.2, 788.3), (600.1, 215.5), (920.6, -521.2), (88.8, -281.2) ]

# Transform the pixel space points
T = np.array([[0, -1], [-1, 0]])
transformed_pixel_points = [(-v, -u) for (u, v) in pixel_points]

# Compute the homography matrix
real_world_points = np.float32(real_world_points)
transformed_pixel_points = np.float32(transformed_pixel_points)

H, _ = cv2.findHomography(transformed_pixel_points, real_world_points)

# Test the mapping with a sample pixel space point
pixel_x, pixel_y = 940, 295
real_x, real_y = apply_homography_and_transformation(H, T, pixel_x, pixel_y)

print(f"Pixel coordinates ({pixel_x}, {pixel_y}) map to real-world coordinates ({real_x}, {real_y})")
