// 小船航行和碰撞检测
document.addEventListener('DOMContentLoaded', function() {
    // 获取大陆数据
    fetch('continent_data/continent_data.json')
        .then(response => response.json())
        .then(data => {
            // 初始化游戏
            initGame(data);
        })
        .catch(error => {
            console.error('加载大陆数据失败:', error);
            alert('加载大陆数据失败，请确保已运行检测脚本生成数据。');
        });
});

function initGame(continentData) {
    // 获取DOM元素
    const mapCanvas = document.getElementById('mapCanvas');
    const ship = document.getElementById('ship');
    const ctx = mapCanvas.getContext('2d');
    
    // 设置画布大小
    mapCanvas.width = 1024;
    mapCanvas.height = 605;
    
    // 加载地图图像
    const mapImage = new Image();
    mapImage.src = 'original_map.png';
    
    // 小船状态
    const shipState = {
        x: mapCanvas.width / 2,
        y: mapCanvas.height / 2,
        width: 30,
        height: 30,
        speed: 1.25, // 降低为原来的25% (原来是5)
        velocityX: 0,
        velocityY: 0,
        rotation: 0,
        traceMode: false, // 是否开启轨迹模式
        totalDistance: 0 // 跟踪总航行距离
    };
    
    // 轨迹数据
    const traces = [];
    
    // 航行数据显示
    const navigationData = {
        visible: false,
        distance: 0,
        time: 0,
        cost: 0
    };
    
    // 创建航行数据面板
    const navPanel = document.createElement('div');
    navPanel.className = 'navigation-panel';
    navPanel.style.display = 'none';
    navPanel.innerHTML = `
        <h3>15世纪航行数据</h3>
        <p class="nav-distance">航行距离: <span>0</span> 海里</p>
        <p class="nav-time">预计用时: <span>0</span> 天</p>
        <p class="nav-cost">所需费用: <span>0</span> 金币</p>
    `;
    document.querySelector('.game-container').appendChild(navPanel);
    
    // 键盘状态
    const keys = {
        ArrowUp: false,
        ArrowDown: false,
        ArrowLeft: false,
        ArrowRight: false,
        a: false, // 添加A键状态
        A: false  // 大写A
    };
    
    // 监听键盘事件
    document.addEventListener('keydown', function(event) {
        if (keys.hasOwnProperty(event.key)) {
            keys[event.key] = true;
            
            // 启用轨迹模式
            if (event.key === 'a' || event.key === 'A') {
                shipState.traceMode = true;
                navPanel.style.display = 'block';
                navigationData.visible = true;
            }
            
            event.preventDefault();
        }
    });
    
    document.addEventListener('keyup', function(event) {
        if (keys.hasOwnProperty(event.key)) {
            keys[event.key] = false;
            
            // 禁用轨迹模式
            if (event.key === 'a' || event.key === 'A') {
                shipState.traceMode = false;
                navPanel.style.display = 'none';
                navigationData.visible = false;
            }
            
            event.preventDefault();
        }
    });
    
    // 绘制地图
    mapImage.onload = function() {
        // 绘制地图
        ctx.drawImage(mapImage, 0, 0, mapCanvas.width, mapCanvas.height);
        
        // 初始化小船位置
        initializeShipPosition(shipState, continentData);
        updateShipPosition(ship, shipState);
        
        // 开始游戏循环
        gameLoop();
    };
    
    // 游戏主循环
    function gameLoop() {
        // 清除画布
        ctx.clearRect(0, 0, mapCanvas.width, mapCanvas.height);
        
        // 绘制地图
        ctx.drawImage(mapImage, 0, 0, mapCanvas.width, mapCanvas.height);
        
        // 保存上一个位置
        const prevX = shipState.x;
        const prevY = shipState.y;
        
        // 更新小船位置
        updateShipMovement(shipState, keys);
        
        // 计算移动距离
        const dx = shipState.x - prevX;
        const dy = shipState.y - prevY;
        const distance = Math.sqrt(dx * dx + dy * dy);
        shipState.totalDistance += distance;
        
        // 更新航行数据
        if (navigationData.visible) {
            // 假设1像素 = 2海里 (换算比例)
            const nauticalMiles = Math.floor(shipState.totalDistance * 2);
            
            // 15世纪船只航速调整，考虑多种因素：
            // 1. 基础航速：约25-30海里/天
            // 2. 恶劣天气、逆风等降低效率：降低20%
            // 3. 停靠补给、修船、等待季风等：增加30%时间
            // 4. 航线探索、绕路等：增加15%距离
            // 最终平均：约20海里/天的有效前进速度
            const days = Math.ceil(nauticalMiles / 20);
            
            // 成本考虑：
            // - 船员工资：每天每人约0.5金币 × 100人 = 50金币/天
            // - 船只折旧：约10金币/天
            // - 补给消耗：约15金币/天
            // - 港口费用：每访问一个主要港口约100金币，假设每20天访问一次
            const portCosts = Math.floor(days / 20) * 100;
            const dailyCosts = days * 75;
            const cost = dailyCosts + portCosts;
            
            document.querySelector('.nav-distance span').textContent = nauticalMiles;
            document.querySelector('.nav-time span').textContent = days;
            document.querySelector('.nav-cost span').textContent = cost;
        }
        
        // 检测碰撞并处理
        handleCollisions(shipState, continentData);
        
        // 如果启用了轨迹模式且移动了，添加轨迹点
        if (shipState.traceMode && (dx !== 0 || dy !== 0)) {
            // 每次移动都添加轨迹点，增加采样率
            addTracePoint(shipState.x, shipState.y);
        }
        
        // 当轨迹模式关闭时，清空轨迹点
        if (!shipState.traceMode && traces.length > 0) {
            traces.length = 0; // 清空数组
        }
        
        // 绘制轨迹
        drawTraces(ctx);
        
        // 更新DOM中的小船位置
        updateShipPosition(ship, shipState);
        
        // 请求下一帧
        requestAnimationFrame(gameLoop);
    }
    
    // 添加轨迹点
    function addTracePoint(x, y) {
        const now = Date.now();
        
        // 如果轨迹为空或与最后一个轨迹点距离足够远才添加新点
        // 这样可以减少轨迹点密度，使虚线效果更明显
        const minDistance = 15; // 最小距离间隔
        
        if (traces.length === 0) {
            traces.push({
                x,
                y,
                timestamp: now
            });
        } else {
            const lastPoint = traces[traces.length - 1];
            const dx = x - lastPoint.x;
            const dy = y - lastPoint.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance >= minDistance) {
                traces.push({
                    x,
                    y,
                    timestamp: now
                });
            }
        }
        
        // 注释掉自动清除轨迹的代码，现在轨迹会一直保留直到A键松开
        // while (traces.length > 0 && now - traces[0].timestamp > 5000) {
        //     traces.shift();
        // }
    }
    
    // 绘制轨迹
    function drawTraces(ctx) {
        ctx.save();
        
        // 使用深蓝色粗线，更加明显
        ctx.strokeStyle = '#003399';
        ctx.lineWidth = 4; 
        
        // 减小虚线间隔 - 8像素线段，20像素空白
        ctx.setLineDash([8, 20]);
        
        // 只有当有足够的点时才绘制
        if (traces.length > 1) {
            // 绘制整条路径而不是单独的线段
            ctx.beginPath();
            ctx.moveTo(traces[0].x, traces[0].y);
            
            for (let i = 1; i < traces.length; i++) {
                ctx.lineTo(traces[i].x, traces[i].y);
            }
            
            ctx.stroke();
        }
        
        ctx.restore();
    }
    
    // 初始化小船位置，确保在海洋中
    function initializeShipPosition(shipState, continentData) {
        let validPosition = false;
        let attempts = 0;
        const maxAttempts = 100;
        
        while (!validPosition && attempts < maxAttempts) {
            shipState.x = Math.random() * (mapCanvas.width - 100) + 50;
            shipState.y = Math.random() * (mapCanvas.height - 100) + 50;
            
            if (!isCollidingWithContinents(shipState, continentData)) {
                validPosition = true;
            }
            
            attempts++;
        }
        
        // 如果找不到，使用固定位置
        if (!validPosition) {
            shipState.x = mapCanvas.width / 2;
            shipState.y = mapCanvas.height / 2;
        }
    }
    
    // 更新小船移动
    function updateShipMovement(shipState, keys) {
        // 根据键盘输入计算速度
        shipState.velocityX = 0;
        shipState.velocityY = 0;
        
        if (keys.ArrowUp) {
            shipState.velocityY = -shipState.speed;
            shipState.rotation = 0;
        }
        if (keys.ArrowDown) {
            shipState.velocityY = shipState.speed;
            shipState.rotation = 180;
        }
        if (keys.ArrowLeft) {
            shipState.velocityX = -shipState.speed;
            shipState.rotation = 270;
        }
        if (keys.ArrowRight) {
            shipState.velocityX = shipState.speed;
            shipState.rotation = 90;
        }
        
        // 对角线移动
        if (keys.ArrowUp && keys.ArrowLeft) {
            shipState.rotation = 315;
        } else if (keys.ArrowUp && keys.ArrowRight) {
            shipState.rotation = 45;
        } else if (keys.ArrowDown && keys.ArrowLeft) {
            shipState.rotation = 225;
        } else if (keys.ArrowDown && keys.ArrowRight) {
            shipState.rotation = 135;
        }
        
        // 计算新位置
        shipState.x += shipState.velocityX;
        shipState.y += shipState.velocityY;
        
        // 防止船出界
        shipState.x = Math.max(shipState.width/2, Math.min(mapCanvas.width - shipState.width/2, shipState.x));
        shipState.y = Math.max(shipState.height/2, Math.min(mapCanvas.height - shipState.height/2, shipState.y));
    }
    
    // 处理碰撞
    function handleCollisions(shipState, continentData) {
        if (isCollidingWithContinents(shipState, continentData)) {
            // 碰撞反弹 - 将船移回上一个位置
            shipState.x -= shipState.velocityX * 1.5;
            shipState.y -= shipState.velocityY * 1.5;
            
            // 如果仍然碰撞，可能陷入边缘，尝试更远距离移动
            if (isCollidingWithContinents(shipState, continentData)) {
                shipState.x -= shipState.velocityX * 2;
                shipState.y -= shipState.velocityY * 2;
            }
            
            // 添加一些反弹效果
            shipState.velocityX = -shipState.velocityX * 0.5;
            shipState.velocityY = -shipState.velocityY * 0.5;
        }
    }
    
    // 检测小船是否与大陆碰撞
    function isCollidingWithContinents(shipState, continentData) {
        const { continents } = continentData;
        const shipHitbox = {
            x: shipState.x - shipState.width/2,
            y: shipState.y - shipState.height/2,
            width: shipState.width,
            height: shipState.height
        };
        
        // 检查所有大陆
        for (const continent of continents) {
            // 先做边界框检查（快速筛选）
            const bbox = continent.bounding_box;
            
            if (isOverlappingRect(shipHitbox, {
                x: bbox[0],
                y: bbox[1],
                width: bbox[2],
                height: bbox[3]
            })) {
                // 然后使用点多边形检测做更精细的检测
                const points = continent.simplified_contour;
                
                // 检查船的四个角是否在多边形内
                const shipCorners = [
                    {x: shipHitbox.x, y: shipHitbox.y},
                    {x: shipHitbox.x + shipHitbox.width, y: shipHitbox.y},
                    {x: shipHitbox.x, y: shipHitbox.y + shipHitbox.height},
                    {x: shipHitbox.x + shipHitbox.width, y: shipHitbox.y + shipHitbox.height}
                ];
                
                for (const corner of shipCorners) {
                    if (isPointInPolygon(corner, points)) {
                        return true;
                    }
                }
                
                // 检查多边形的边是否与船的边相交
                const shipEdges = [
                    [{x: shipHitbox.x, y: shipHitbox.y}, {x: shipHitbox.x + shipHitbox.width, y: shipHitbox.y}],
                    [{x: shipHitbox.x + shipHitbox.width, y: shipHitbox.y}, {x: shipHitbox.x + shipHitbox.width, y: shipHitbox.y + shipHitbox.height}],
                    [{x: shipHitbox.x + shipHitbox.width, y: shipHitbox.y + shipHitbox.height}, {x: shipHitbox.x, y: shipHitbox.y + shipHitbox.height}],
                    [{x: shipHitbox.x, y: shipHitbox.y + shipHitbox.height}, {x: shipHitbox.x, y: shipHitbox.y}]
                ];
                
                for (let i = 0; i < points.length; i++) {
                    const j = (i + 1) % points.length;
                    const edge = [{x: points[i][0], y: points[i][1]}, {x: points[j][0], y: points[j][1]}];
                    
                    for (const shipEdge of shipEdges) {
                        if (doLinesIntersect(shipEdge[0], shipEdge[1], edge[0], edge[1])) {
                            return true;
                        }
                    }
                }
            }
        }
        
        return false;
    }
    
    // 更新小船DOM位置
    function updateShipPosition(shipElement, shipState) {
        shipElement.style.left = `${shipState.x}px`;
        shipElement.style.top = `${shipState.y}px`;
        shipElement.style.transform = `translate(-50%, -50%) rotate(${shipState.rotation}deg)`;
    }
    
    // 工具函数: 检查两个矩形是否重叠
    function isOverlappingRect(rect1, rect2) {
        return !(
            rect1.x + rect1.width < rect2.x ||
            rect1.x > rect2.x + rect2.width ||
            rect1.y + rect1.height < rect2.y ||
            rect1.y > rect2.y + rect2.height
        );
    }
    
    // 工具函数: 检查点是否在多边形内
    function isPointInPolygon(point, polygon) {
        let inside = false;
        for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
            const xi = polygon[i][0], yi = polygon[i][1];
            const xj = polygon[j][0], yj = polygon[j][1];
            
            const intersect = ((yi > point.y) !== (yj > point.y))
                && (point.x < (xj - xi) * (point.y - yi) / (yj - yi) + xi);
            
            if (intersect) inside = !inside;
        }
        
        return inside;
    }
    
    // 工具函数: 检查两条线段是否相交
    function doLinesIntersect(p1, p2, p3, p4) {
        function ccw(a, b, c) {
            return (c.y - a.y) * (b.x - a.x) > (b.y - a.y) * (c.x - a.x);
        }
        
        return ccw(p1, p3, p4) !== ccw(p2, p3, p4) && ccw(p1, p2, p3) !== ccw(p1, p2, p4);
    }
} 