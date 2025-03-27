# 海上航行模拟项目部署指南

## 1. 创建GitHub仓库

1. 登录到您的GitHub账号
2. 点击右上角"+"图标，选择"New repository"
3. 输入仓库名：`sea-navigation-simulation`
4. 添加描述：`15世纪海上航行模拟项目`
5. 选择公开仓库（Public）
6. 不要勾选初始化选项（因为我们已经有了文件）
7. 点击"Create repository"

## 2. 将本地仓库推送到GitHub

在命令行中执行以下命令（请将`yourusername`替换为您的GitHub用户名）：

```bash
git remote add origin https://github.com/yourusername/sea-navigation-simulation.git
git branch -M main
git push -u origin main
```

## 3. 启用GitHub Pages

1. 进入GitHub仓库页面
2. 点击"Settings"选项卡
3. 滚动到"GitHub Pages"部分
4. 在"Source"下拉菜单中选择"main"分支
5. 点击"Save"按钮

几分钟后，您的项目将在以下地址可访问：
`https://yourusername.github.io/sea-navigation-simulation/map_navigation.html`

## 4. 更新README中的链接

部署成功后，编辑README.md文件，将"在线体验"部分的链接更新为：
`https://yourusername.github.io/sea-navigation-simulation/map_navigation.html`

## 注意事项

1. GitHub Pages可能需要几分钟时间来处理您的站点
2. 如果您看到404错误，请确认仓库设置中的GitHub Pages配置是否正确
3. 您可能需要修改README.md中的链接，使其指向正确的GitHub Pages地址 