// 定义16世纪重要地点的位置
const historicalLocations = [
    {
        id: 'portugal',
        name: '葡萄牙',
        x: 412,
        y: 151,
        description: '航海强国，探险家的起点'
    },
    {
        id: 'spain',
        name: '西班牙',
        x: 434,
        y: 162,
        description: '哥伦布航行的赞助国'
    },
    {
        id: 'bahamas',
        name: '巴哈马群岛',
        x: 194,
        y: 196,
        description: '哥伦布首次登陆地点'
    },
    {
        id: 'magellan',
        name: '麦哲伦海峡',
        x: 182,
        y: 485,
        description: '连接大西洋和太平洋的海峡'
    },
    {
        id: 'goodhope',
        name: '好望角',
        x: 498,
        y: 414,
        description: '通往印度洋的门户'
    },
    {
        id: 'malindi',
        name: '马林迪',
        x: 550,
        y: 322,
        description: '非洲东海岸的贸易港口'
    },
    {
        id: 'calicut',
        name: '卡里库特',
        x: 635,
        y: 273,
        description: '印度重要的香料贸易中心'
    }
];

// 在地图上创建和管理地点标记
function initializeLocationMarkers() {
    const gameContainer = document.querySelector('.game-container');
    
    // 为每个地点创建标记
    historicalLocations.forEach(location => {
        createLocationMarker(location, gameContainer);
    });
}

// 创建单个地点标记
function createLocationMarker(location, container) {
    // 创建标记点
    const marker = document.createElement('div');
    marker.className = 'location-marker';
    marker.id = `marker-${location.id}`;
    marker.style.left = `${location.x}px`;
    marker.style.top = `${location.y}px`;
    marker.dataset.name = location.name;
    marker.dataset.id = location.id;
    
    // 创建标签
    const label = document.createElement('div');
    label.className = 'location-label';
    label.textContent = location.name;
    label.id = `label-${location.id}`;
    
    // 添加到容器
    marker.appendChild(label);
    container.appendChild(marker);
    
    // 添加拖动功能
    enableDragging(marker, label);
}

// 启用拖动功能
function enableDragging(marker, label) {
    let isDragging = false;
    let offsetX, offsetY;
    
    // 鼠标按下事件
    marker.addEventListener('mousedown', function(e) {
        isDragging = true;
        marker.classList.add('dragging');
        
        // 计算鼠标相对于标记的偏移
        const rect = marker.getBoundingClientRect();
        offsetX = e.clientX - rect.left;
        offsetY = e.clientY - rect.top;
        
        e.preventDefault();
    });
    
    // 鼠标移动事件
    document.addEventListener('mousemove', function(e) {
        if (!isDragging) return;
        
        // 计算新位置
        const gameContainer = marker.parentElement;
        const containerRect = gameContainer.getBoundingClientRect();
        const newLeft = e.clientX - containerRect.left - offsetX;
        const newTop = e.clientY - containerRect.top - offsetY;
        
        // 确保标记不会拖出容器
        const markerWidth = marker.offsetWidth;
        const markerHeight = marker.offsetHeight;
        
        const boundedLeft = Math.max(0, Math.min(containerRect.width - markerWidth, newLeft));
        const boundedTop = Math.max(0, Math.min(containerRect.height - markerHeight, newTop));
        
        // 更新位置
        marker.style.left = `${boundedLeft + markerWidth/2}px`;
        marker.style.top = `${boundedTop + markerHeight/2}px`;
        
        // 保存新位置
        const locationId = marker.dataset.id;
        const locationIndex = historicalLocations.findIndex(loc => loc.id === locationId);
        if (locationIndex !== -1) {
            historicalLocations[locationIndex].x = boundedLeft + markerWidth/2;
            historicalLocations[locationIndex].y = boundedTop + markerHeight/2;
        }
    });
    
    // 鼠标释放事件
    document.addEventListener('mouseup', function() {
        if (isDragging) {
            isDragging = false;
            marker.classList.remove('dragging');
        }
    });
    
    // 鼠标离开窗口
    document.addEventListener('mouseleave', function() {
        if (isDragging) {
            isDragging = false;
            marker.classList.remove('dragging');
        }
    });
    
    // 显示/隐藏详细信息
    marker.addEventListener('mouseover', function() {
        const locationId = marker.dataset.id;
        const location = historicalLocations.find(loc => loc.id === locationId);
        if (location) {
            label.textContent = `${location.name}: ${location.description}`;
        }
    });
    
    marker.addEventListener('mouseout', function() {
        const locationId = marker.dataset.id;
        const location = historicalLocations.find(loc => loc.id === locationId);
        if (location) {
            label.textContent = location.name;
        }
    });
}

// 导出初始化函数
export { initializeLocationMarkers }; 