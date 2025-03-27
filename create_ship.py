import cv2
import numpy as np

# 创建透明背景
ship = np.zeros((64, 64, 4), dtype=np.uint8)

# 绘制船身 - 橙色圆形
cv2.circle(ship, (32, 32), 15, (0, 150, 255, 255), -1)

# 绘制船舱 - 深橙色圆形
cv2.circle(ship, (32, 32), 10, (0, 100, 255, 255), -1)

# 绘制船帆 - 白色三角形
sail_pts = np.array([[32, 15], [20, 35], [44, 35]], dtype=np.int32)
cv2.fillConvexPoly(ship, sail_pts, (255, 255, 255, 255))

# 绘制船桅 - 红色
cv2.line(ship, (32, 15), (32, 45), (0, 0, 255, 255), 2)

# 保存图像
cv2.imwrite('ship.png', ship)

print("小船图像已创建: ship.png") 