import cv2
import numpy as np
import matplotlib.pyplot as plt
import json
import os

class ContinentDetector:
    def __init__(self, image_path):
        """初始化大陆检测器"""
        self.image_path = image_path
        self.image = None
        self.image_rgb = None
        self.image_hsv = None
        self.best_mask = None
        self.continents = []
        self.continent_contours = []
        
        # 创建输出目录
        self.output_dir = "continent_data"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_image(self):
        """加载图像并进行预处理"""
        self.image = cv2.imread(self.image_path)
        if self.image is None:
            raise ValueError(f"无法读取图像: {self.image_path}")
        
        print(f"图像大小: {self.image.shape}")
        self.image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.image_hsv = cv2.cvtColor(self.image_rgb, cv2.COLOR_RGB2HSV)
        return self
    
    def analyze_colors(self):
        """分析图像中的颜色分布"""
        h, w, _ = self.image.shape
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
        
        print("图像中的一些像素颜色样本:")
        for i, (x, y) in enumerate(sample_points):
            bgr_color = self.image[y, x]
            rgb_color = self.image_rgb[y, x]
            hsv_color = self.image_hsv[y, x]
            print(f"样本 {i+1} at ({x}, {y}):")
            print(f"  BGR: {bgr_color}")
            print(f"  RGB: {rgb_color}")
            print(f"  HSV: {hsv_color}")
        
        return self
    
    def detect_continents(self, save_intermediate=True):
        """检测地图中的大陆"""
        # 尝试不同的HSV阈值来找到最佳掩码
        hsv_thresholds = [
            ([20, 100, 100], [40, 255, 255], "严格黄色"),
            ([15, 50, 100], [45, 255, 255], "中等黄色"),
            ([10, 40, 40], [50, 255, 255], "宽松黄色"),
            ([5, 20, 100], [55, 255, 255], "非常宽松黄色"),
            ([20, 70, 150], [35, 255, 255], "亮黄色"),
            ([15, 40, 150], [45, 200, 255], "暗黄色"),
        ]
        
        print("\n生成不同的掩码以找到最佳设置...")
        best_contours_count = 0
        best_mask_index = -1
        
        masks = []
        
        for i, (lower, upper, desc) in enumerate(hsv_thresholds):
            lower_array = np.array(lower)
            upper_array = np.array(upper)
            
            # 创建掩码
            mask = cv2.inRange(self.image_hsv, lower_array, upper_array)
            
            # 应用形态学操作来去除噪声
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            if save_intermediate:
                mask_filename = os.path.join(self.output_dir, f"mask_{i+1}.png")
                cv2.imwrite(mask_filename, mask)
            
            masks.append((mask, desc))
            
            # 找到轮廓
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # 筛选大轮廓
            min_contour_area = 1000
            filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
            
            print(f"掩码 {i+1} ({desc}): 找到 {len(filtered_contours)} 个大陆区域")
            
            # 更新最佳掩码
            if len(filtered_contours) > best_contours_count:
                best_contours_count = len(filtered_contours)
                self.best_mask = mask.copy()
                best_mask_index = i
        
        if self.best_mask is not None:
            print(f"最佳掩码是 #{best_mask_index + 1}: {hsv_thresholds[best_mask_index][2]}")
            best_mask_filename = os.path.join(self.output_dir, "best_mask.png")
            cv2.imwrite(best_mask_filename, self.best_mask)
            
            # 使用最佳掩码进行进一步处理
            contours, _ = cv2.findContours(self.best_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            min_contour_area = 1000
            self.continent_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
            
            # 保存每个大陆的详细信息
            for i, contour in enumerate(self.continent_contours):
                area = cv2.contourArea(contour)
                perimeter = cv2.arcLength(contour, True)
                
                # 计算轮廓的中心
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                else:
                    cX, cY = 0, 0
                
                # 计算轮廓的边界框
                x, y, w, h = cv2.boundingRect(contour)
                
                # 提取轮廓点
                contour_points = contour.reshape(-1, 2).tolist()
                
                # 简化轮廓（减少点的数量，提高效率）
                epsilon = 0.002 * perimeter
                approx_contour = cv2.approxPolyDP(contour, epsilon, True)
                approx_points = approx_contour.reshape(-1, 2).tolist()
                
                continent_info = {
                    "id": i + 1,
                    "area": float(area),
                    "perimeter": float(perimeter),
                    "center": [cX, cY],
                    "bounding_box": [x, y, w, h],
                    "contour_points": contour_points,
                    "simplified_contour": approx_points
                }
                
                self.continents.append(continent_info)
            
            # 可视化比较不同的掩码
            if save_intermediate:
                plt.figure(figsize=(15, 10))
                for i, (mask, desc) in enumerate(masks):
                    plt.subplot(2, 3, i+1)
                    plt.imshow(mask, cmap='gray')
                    plt.title(f'Mask {i+1}: {desc}')
                    plt.axis('off')
                
                plt.tight_layout()
                mask_comparison_filename = os.path.join(self.output_dir, "mask_comparison.png")
                plt.savefig(mask_comparison_filename)
                plt.close()
        else:
            print("没有找到适合的掩码")
        
        return self
    
    def visualize_results(self):
        """可视化检测结果"""
        if not self.continent_contours:
            print("没有检测到大陆，无法可视化")
            return self
        
        # 在原图上绘制轮廓
        result_image = self.image_rgb.copy()
        cv2.drawContours(result_image, self.continent_contours, -1, (255, 0, 0), 3)
        
        # 给每个大陆标号
        for i, continent in enumerate(self.continents):
            cX, cY = continent["center"]
            cv2.putText(result_image, str(i+1), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 5)
        
        # 保存结果
        result_filename = os.path.join(self.output_dir, "map_with_boundaries.png")
        cv2.imwrite(result_filename, cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR))
        
        # 创建更详细的信息图
        detailed_info = self.image_rgb.copy()
        for continent in self.continents:
            cX, cY = continent["center"]
            area = continent["area"]
            contour_idx = continent["id"] - 1
            
            # 在中心位置添加编号和面积信息
            cv2.putText(detailed_info, f"#{continent['id']}: {area:.0f}px²", 
                        (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            # 绘制轮廓
            cv2.drawContours(detailed_info, [self.continent_contours[contour_idx]], -1, (255, 0, 0), 3)
            
            # 绘制边界框
            x, y, w, h = continent["bounding_box"]
            cv2.rectangle(detailed_info, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # 保存详细信息图
        detailed_filename = os.path.join(self.output_dir, "map_with_detailed_info.png")
        cv2.imwrite(detailed_filename, cv2.cvtColor(detailed_info, cv2.COLOR_RGB2BGR))
        
        # 可视化处理结果（并排显示）
        plt.figure(figsize=(15, 10))
        
        plt.subplot(131)
        plt.imshow(self.image_rgb)
        plt.title('Original Map')
        plt.axis('off')
        
        plt.subplot(132)
        plt.imshow(self.best_mask, cmap='gray')
        plt.title('Continent Mask')
        plt.axis('off')
        
        plt.subplot(133)
        plt.imshow(result_image)
        plt.title('Detected Continents')
        plt.axis('off')
        
        plt.tight_layout()
        visualization_filename = os.path.join(self.output_dir, "detection_visualization.png")
        plt.savefig(visualization_filename)
        plt.close()
        
        return self
    
    def save_continent_data(self):
        """保存大陆数据到JSON文件"""
        if not self.continents:
            print("没有检测到大陆，无法保存数据")
            return self
        
        # 保存为JSON文件
        continent_data = {
            "continents": self.continents,
            "image_size": self.image.shape[:2],
            "total_continents": len(self.continents)
        }
        
        json_filename = os.path.join(self.output_dir, "continent_data.json")
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(continent_data, f, ensure_ascii=False, indent=2)
        
        # 保存为文本文件
        txt_filename = os.path.join(self.output_dir, "continent_info.txt")
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write("大陆边界信息:\n")
            f.write("==============\n\n")
            for continent in self.continents:
                f.write(f"大陆 #{continent['id']}:\n")
                f.write(f"  面积: {continent['area']:.2f} 像素²\n")
                f.write(f"  周长: {continent['perimeter']:.2f} 像素\n")
                f.write(f"  中心点: ({continent['center'][0]}, {continent['center'][1]})\n")
                f.write(f"  边界框: x={continent['bounding_box'][0]}, y={continent['bounding_box'][1]}, w={continent['bounding_box'][2]}, h={continent['bounding_box'][3]}\n")
                f.write(f"  简化轮廓点数: {len(continent['simplified_contour'])}\n\n")
        
        print(f"已保存大陆数据到 {json_filename} 和 {txt_filename}")
        return self


if __name__ == "__main__":
    # 使用示例
    detector = ContinentDetector("original_map.png")
    detector.load_image() \
           .analyze_colors() \
           .detect_continents() \
           .visualize_results() \
           .save_continent_data()
    
    print(f"检测到 {len(detector.continents)} 个大陆区域")
    print("处理完成，数据和图片已保存到 'continent_data' 目录。") 