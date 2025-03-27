import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取图像
image_path = 'original_map.png'  # 更改为英文文件名
image = cv2.imread(image_path)

# 检查图像是否成功加载
if image is None:
    print(f"无法读取图像: {image_path}")
    print("请确保文件存在并且命名为'original_map.png'")
    print("尝试重命名'纯地图.png'为'original_map.png'")
    exit(1)

print(f"图像大小: {image.shape}")

# 转换颜色空间从BGR到RGB（OpenCV默认使用BGR）
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 展示图像中的一些像素颜色，以帮助确定黄色的范围
print("图像中的一些像素颜色样本:")
h, w, _ = image.shape
sample_points = [
    (w//4, h//4), 
    (w//2, h//4), 
    (3*w//4, h//4),
    (w//4, h//2), 
    (w//2, h//2), 
    (3*w//4, h//2),
    (w//4, 3*h//4), 
    (w//2, 3*h//4), 
    (3*w//4, 3*h//4)
]

for i, (x, y) in enumerate(sample_points):
    bgr_color = image[y, x]
    rgb_color = image_rgb[y, x]
    print(f"样本 {i+1} at ({x}, {y}): BGR={bgr_color}, RGB={rgb_color}")

# 转换到HSV颜色空间以更容易地提取黄色
image_hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)

# 显示一些HSV样本
for i, (x, y) in enumerate(sample_points):
    hsv_color = image_hsv[y, x]
    print(f"样本 {i+1} HSV: {hsv_color}")

# 现在我们尝试多种不同的HSV阈值范围来找出最佳的掩码
hsv_thresholds = [
    # 黄色范围，从宽松到严格
    ([20, 100, 100], [40, 255, 255], "yellow_mask_1.png", "严格黄色"),
    ([15, 50, 100], [45, 255, 255], "yellow_mask_2.png", "中等黄色"),
    ([10, 40, 40], [50, 255, 255], "yellow_mask_3.png", "宽松黄色"),
    # 更广泛的范围
    ([5, 20, 100], [55, 255, 255], "yellow_mask_4.png", "非常宽松黄色"),
    # 特定于地图的范围
    ([20, 70, 150], [35, 255, 255], "yellow_mask_5.png", "亮黄色"),
    ([15, 40, 150], [45, 200, 255], "yellow_mask_6.png", "暗黄色"),
]

print("\n生成不同的掩码以找到最佳设置...")
best_mask = None
best_contours_count = 0
best_mask_index = -1

for i, (lower, upper, filename, desc) in enumerate(hsv_thresholds):
    lower_array = np.array(lower)
    upper_array = np.array(upper)
    
    # 创建掩码
    mask = cv2.inRange(image_hsv, lower_array, upper_array)
    
    # 应用形态学操作来去除噪声
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # 保存掩码
    cv2.imwrite(filename, mask)
    
    # 找到轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 筛选大轮廓
    min_contour_area = 1000  # 可以根据实际需要调整
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
    
    print(f"掩码 {i+1} ({desc}): 找到 {len(filtered_contours)} 个大陆区域")
    
    # 更新最佳掩码
    if len(filtered_contours) > best_contours_count:
        best_contours_count = len(filtered_contours)
        best_mask = mask.copy()
        best_mask_index = i

if best_mask is not None:
    print(f"最佳掩码是 #{best_mask_index + 1}")
    cv2.imwrite('best_yellow_mask.png', best_mask)
    
    # 使用最佳掩码进行进一步处理
    contours, _ = cv2.findContours(best_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_contour_area = 1000
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
    
    # 在原图上绘制轮廓
    result_image = image_rgb.copy()
    cv2.drawContours(result_image, filtered_contours, -1, (255, 0, 0), 3)  # 使用蓝色绘制轮廓
    
    # 给每个大陆标号
    for i, contour in enumerate(filtered_contours):
        # 计算轮廓的中心
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
        
        # 在中心位置添加编号
        cv2.putText(result_image, str(i+1), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 5)
    
    # 保存结果
    cv2.imwrite('map_with_boundaries.png', cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR))
    
    # 创建更详细的信息图
    detailed_info = image_rgb.copy()
    for i, contour in enumerate(filtered_contours):
        # 计算轮廓的中心
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
        
        # 计算轮廓面积
        area = cv2.contourArea(contour)
        
        # 在中心位置添加编号和面积信息
        cv2.putText(detailed_info, f"#{i+1}: {area:.0f}px²", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        # 绘制轮廓
        cv2.drawContours(detailed_info, [contour], -1, (255, 0, 0), 3)
    
    # 保存详细信息图
    cv2.imwrite('map_with_detailed_info.png', cv2.cvtColor(detailed_info, cv2.COLOR_RGB2BGR))
    
    # 保存大陆信息到文本文件
    with open('continent_info.txt', 'w', encoding='utf-8') as f:
        f.write("大陆边界信息:\n")
        f.write("==============\n\n")
        for i, contour in enumerate(filtered_contours):
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            f.write(f"大陆 #{i+1}:\n")
            f.write(f"  面积: {area:.2f} 像素²\n")
            f.write(f"  周长: {perimeter:.2f} 像素\n\n")
    
    # 可视化处理结果
    plt.figure(figsize=(15, 10))
    
    plt.subplot(131)
    plt.imshow(image_rgb)
    plt.title('Original Map')
    plt.axis('off')
    
    plt.subplot(132)
    plt.imshow(best_mask, cmap='gray')
    plt.title('Best Yellow Mask')
    plt.axis('off')
    
    plt.subplot(133)
    plt.imshow(result_image)
    plt.title('Map with Boundaries')
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig('map_boundaries_visualization.png')
    plt.close()

else:
    print("没有找到适合的掩码")

# 比较不同的掩码
plt.figure(figsize=(15, 10))
for i, (lower, upper, filename, desc) in enumerate(hsv_thresholds):
    mask = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    plt.subplot(2, 3, i+1)
    plt.imshow(mask, cmap='gray')
    plt.title(f'Mask {i+1}: {desc}')
    plt.axis('off')

plt.tight_layout()
plt.savefig('yellow_masks_comparison.png')
plt.close()

print("处理完成，图片已保存。") 