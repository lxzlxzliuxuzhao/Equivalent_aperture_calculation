import math
import csv
import matplotlib.pyplot as plt

def calculate_crop_factor(effective_sensor_width_mm, effective_sensor_height_mm, original_focal_length, cropped_focal_length):
    effective_sensor_diagonal_mm = math.sqrt(effective_sensor_width_mm**2 + effective_sensor_height_mm**2)
    zoom_factor = cropped_focal_length / original_focal_length
    effective_sensor_diagonal = effective_sensor_diagonal_mm / zoom_factor
    full_frame_diagonal = math.sqrt(36**2 + 24**2)
    return full_frame_diagonal / effective_sensor_diagonal

def calculate_equivalent_aperture(real_aperture, crop_factor):
    return real_aperture * crop_factor

# 定义摄像头参数（包括使用部分传感器的实际尺寸）
cameras = [
    {"id": 1, "effective_sensor_width_mm": 6.4, "effective_sensor_height_mm": 4.8, "real_aperture": 2.2, "original_focal_length": 14, "color": "blue"},
    {"id": 2, "effective_sensor_width_mm": 9.18, "effective_sensor_height_mm": 6.88, "real_aperture": 1.6, "original_focal_length": 23, "color": "red"},
    {"id": 3, "effective_sensor_width_mm": 6.4, "effective_sensor_height_mm": 4.8, "real_aperture": 2.6, "original_focal_length": 70, "color": "green"},
]

focal_lengths = range(13, 201, 1)
best_apertures = {focal_length: {"aperture": float('inf'), "camera_id": None} for focal_length in focal_lengths}

for camera in cameras:
    camera_focal_lengths = range(int(camera["original_focal_length"]), 201, 1)
    for cropped_focal_length in camera_focal_lengths:
        crop_factor = calculate_crop_factor(camera["effective_sensor_width_mm"], camera["effective_sensor_height_mm"], camera["original_focal_length"], cropped_focal_length)
        equivalent_aperture = calculate_equivalent_aperture(camera["real_aperture"], crop_factor)
        if cropped_focal_length in camera_focal_lengths and equivalent_aperture < best_apertures[cropped_focal_length]["aperture"]:
            best_apertures[cropped_focal_length]["aperture"] = equivalent_aperture
            best_apertures[cropped_focal_length]["camera_id"] = camera["id"]

# 保存结果到CSV文件
filename = "aperture_results.csv"
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Focal Length (mm)', 'Best Aperture Value (Negative)', 'Camera ID'])
    for focal_length, info in best_apertures.items():
        writer.writerow([focal_length, -info["aperture"], info["camera_id"]])

print(f"Data saved to {filename}")

# 可选：绘制图表
plt.figure(figsize=(10, 6))
for camera in cameras:
    focal_lengths = [fl for fl, info in best_apertures.items() if info["camera_id"] == camera["id"]]
    negative_apertures = [-info["aperture"] for fl, info in best_apertures.items() if info["camera_id"] == camera["id"]]
    plt.plot(focal_lengths, negative_apertures, marker='o', color=camera["color"], label=f"CMOS {camera['id']} (Effective Sensor: {camera['effective_sensor_width_mm']}mm x {camera['effective_sensor_height_mm']}mm)")

plt.xlabel('焦距 (mm)')
plt.ylabel('等效光圈 (负数表示)')
plt.title('不同CMOS摄像头的等效光圈（负数表示）随焦距变化')
plt.grid(True)
plt.legend()
plt.show()

