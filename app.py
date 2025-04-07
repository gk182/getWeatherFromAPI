import requests
import json
import datetime
import matplotlib.pyplot as plt
import numpy as np
import os

# Hàm chuyển đổi °F sang °C (làm tròn)
def f_to_c(temp_f):
    return round((temp_f - 32) * 5 / 9)

# ==== URL API ====
url = ("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
       "%C4%90%C3%A0%20N%E1%BA%B5ng%2C%20Vi%E1%BB%87t%20Nam/last7days"
       "?include=days&key=ZVFM4CPAYC6VGYS7ZMFD9QMJK&contentType=json")

# Gọi API
response = requests.get(url)
if response.status_code != 200:
    print("Lỗi khi lấy dữ liệu:", response.status_code)
    print(response.text)
    exit()

# Giải mã JSON
data = response.json()
days = data.get("days", [])

# Tạo danh sách ngày, nhiệt độ trung bình (đổi sang °C) và độ ẩm
dates = [datetime.datetime.strptime(day["datetime"], "%Y-%m-%d") for day in days]
temps_c = [f_to_c(day["temp"]) for day in days]
humidities = [round(day["humidity"]) for day in days]

# ==== Xác định tên file dựa trên ngày cuối cùng của dữ liệu ====
end_date = dates[-1]
file_date_str = end_date.strftime("%d_%m_%Y")
filename = f"march_{end_date.year}_{file_date_str}.txt"

# ==== Đường dẫn file txt và file ảnh (đổi tên ảnh thành 7day.png) ====
txt_filepath = os.path.join("text", filename)
image_filename = "7day.png"  # Đổi tên ảnh thành 7day.png
image_filepath = os.path.join("images", image_filename)

# ==== GHI FILE TXT ====
with open(txt_filepath, "w", encoding='utf-8') as f:
    for date, temp, humidity in zip(dates, temps_c, humidities):
        date_str = date.strftime("%d_%m_%Y")
        f.write(f"DaNang,{date_str},{temp},{humidity}\n")

print(f"Đã lưu dữ liệu vào file: {txt_filepath}")

# ==== VẼ BIỂU ĐỒ ====
plt.figure(figsize=(10, 6))

# Vẽ cột độ ẩm (màu xanh)
plt.bar(dates, humidities, width=0.6, color='blue', alpha=0.6, label='Độ ẩm (%)')

# Vẽ đường nhiệt độ (màu đỏ)
plt.plot(dates, temps_c, color='red', marker='o', label='Nhiệt độ (°C)', linewidth=2)

# Thiết lập tiêu đề, nhãn trục và xoay nhãn trục x
plt.title("Biểu đồ thời tiết tại Đà Nẵng (Nhiệt độ tính theo °C)")
plt.xlabel("Ngày")
plt.ylabel("Giá trị")
plt.yticks(np.arange(0, 105, 5))
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

# ==== Lưu ảnh với tên file 7day.png ====
plt.savefig(image_filepath)
print(f"Đã lưu ảnh biểu đồ vào file: {image_filepath}")

plt.show()
