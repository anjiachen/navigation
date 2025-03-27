# GitHub Pages 发布步骤

## 第一步：创建GitHub仓库

1. 在浏览器中访问 [GitHub](https://github.com/)
2. 登录您的GitHub账号
3. 点击页面右上角的"+"图标，选择"New repository"
4. 填写仓库信息：
   - Repository name: `sea-navigation-simulation`
   - Description: `15世纪海上航行模拟项目`
   - 选择"Public"（公开）
   - 不要勾选"Initialize this repository with a README"
   - 点击"Create repository"按钮

## 第二步：从本地推送代码

在您已经初始化的本地Git仓库中，执行以下命令（请替换为您的GitHub用户名）：

```
git remote set-url origin https://github.com/您的用户名/sea-navigation-simulation.git
git push -u origin main
```

当提示输入用户名和密码时，输入您的GitHub账号信息。

## 第三步：启用GitHub Pages

1. 推送完成后，在浏览器中访问您的仓库页面
2. 点击"Settings"选项卡
3. 在左侧菜单栏中，找到并点击"Pages"
4. 在"Source"部分，从下拉菜单中选择"main"分支，然后点击"Save"
5. 等待几分钟后，页面顶部会显示您的网站已发布的URL

## 第四步：访问您的页面

您的海上航行模拟项目将在以下地址可访问：
```
https://您的用户名.github.io/sea-navigation-simulation/map_navigation.html
```

## 注意事项

- GitHub Pages部署可能需要几分钟时间
- 如果您修改了代码，只需再次执行`git add`、`git commit`和`git push`命令即可更新网站 