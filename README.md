# 海上航行模拟

这是一个基于网页的海上航行模拟项目，模拟15世纪大航海时代的航海探索。用户可以控制一艘小船在世界地图上航行，同时体验当时的航行条件和挑战。

## 功能特点

- 使用方向键控制小船在海洋中航行
- 按住A键显示航线轨迹和详细的航行数据
- 碰到大陆会自动反弹
- 世界地图上标注了重要的历史航海地点，可拖动调整位置
- 基于15世纪航海技术的真实航行数据计算

## 在线体验

你可以在这里体验项目：[海上航行模拟](https://github.com/yourusername/sea-navigation-simulation)

## 本地运行

1. 克隆仓库
   ```
   git clone https://github.com/yourusername/sea-navigation-simulation.git
   cd sea-navigation-simulation
   ```

2. 启动简易服务器
   ```
   python start_server.py
   ```

3. 在浏览器中访问
   ```
   http://localhost:8000/map_navigation.html
   ```

## 技术实现

- 使用Canvas绘制地图和航行轨迹
- 基于大陆轮廓数据的精确碰撞检测
- 模块化JavaScript实现地点标记和船只控制
- 响应式设计，适应不同屏幕大小

## 数据说明

- 航行距离：1像素 = 2海里
- 航行速度：基于15世纪船只平均每天20海里的速度
- 航行成本：考虑船员工资、船只折旧、补给和港口费用

## 贡献指南

欢迎提交问题和改进建议！请随时提交Issue或Pull Request。

## 许可

MIT许可证 