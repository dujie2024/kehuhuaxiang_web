// 全局变量
let currentParkingData = null;
let currentBookingData = null;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// 初始化应用
function initializeApp() {
    // 设置默认日期
    setDefaultDates();
    
    // 绑定导航事件
    bindNavigationEvents();
    
    // 绑定表单提交事件
    bindFormEvents();
    
    // 绑定图表生成按钮事件
    bindChartEvents();
}

// 设置默认日期（最近30天）
function setDefaultDates() {
    const today = new Date();
    const thirtyDaysAgo = new Date(today);
    thirtyDaysAgo.setDate(today.getDate() - 30);
    
    const todayStr = formatDate(today);
    const thirtyDaysAgoStr = formatDate(thirtyDaysAgo);
    
    document.getElementById('parking-start-date').value = thirtyDaysAgoStr;
    document.getElementById('parking-end-date').value = todayStr;
    document.getElementById('booking-start-date').value = thirtyDaysAgoStr;
    document.getElementById('booking-end-date').value = todayStr;
}

// 格式化日期为 YYYY-MM-DD
function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// 绑定导航事件
function bindNavigationEvents() {
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            const viewName = this.getAttribute('data-view');
            switchView(viewName);
            
            // 更新导航激活状态
            navItems.forEach(nav => nav.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

// 切换视图
function switchView(viewName) {
    const views = document.querySelectorAll('.view-container');
    views.forEach(view => view.classList.remove('active'));
    
    const targetView = document.getElementById(`${viewName}-view`);
    if (targetView) {
        targetView.classList.add('active');
    }
}

// 绑定表单提交事件
function bindFormEvents() {
    // 停车数据表单
    const parkingForm = document.getElementById('parking-form');
    parkingForm.addEventListener('submit', function(e) {
        e.preventDefault();
        analyzeParkingData();
    });
    
    // 预订数据表单
    const bookingForm = document.getElementById('booking-form');
    bookingForm.addEventListener('submit', function(e) {
        e.preventDefault();
        analyzeBookingData();
    });
}

// 绑定图表生成按钮事件
function bindChartEvents() {
    // 停车数据图表按钮
    const parkingChartBtn = document.getElementById('parking-chart-btn');
    parkingChartBtn.addEventListener('click', function() {
        generateParkingChart();
    });
    
    // 预订数据图表按钮
    const bookingChartBtn = document.getElementById('booking-chart-btn');
    bookingChartBtn.addEventListener('click', function() {
        generateBookingChart();
    });
}

// 分析停车数据
async function analyzeParkingData() {
    const formData = {
        parking_lot: document.getElementById('parking-lot').value,
        chart_type: document.getElementById('parking-chart-type').value,
        start_date: document.getElementById('parking-start-date').value,
        end_date: document.getElementById('parking-end-date').value
    };
    
    showLoading(true);
    
    try {
        const response = await fetch('/api/parking/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentParkingData = {
                data: result.data,
                ...formData
            };
            displayParkingResults(result.data);
            document.getElementById('parking-chart-btn').style.display = 'block';
            document.getElementById('parking-chart-container').style.display = 'none';
        } else {
            showError(result.message || '查询失败');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('网络请求失败，请检查服务器连接');
    } finally {
        showLoading(false);
    }
}

// 显示停车数据结果
function displayParkingResults(data) {
    const resultsContainer = document.getElementById('parking-results');
    
    if (!data || data.length === 0) {
        resultsContainer.innerHTML = '<div class="empty-state"><p>未找到符合条件的数据</p></div>';
        return;
    }
    
    let html = '';
    data.forEach((item, index) => {
        html += `
            <div class="result-card">
                <div class="result-rank">#${index + 1}</div>
                <div class="result-location">${item[0]}</div>
                <div class="result-count">${item[1].toLocaleString()} 辆</div>
            </div>
        `;
    });
    
    resultsContainer.innerHTML = html;
}

// 生成停车数据图表
async function generateParkingChart() {
    if (!currentParkingData) {
        showError('请先查询数据');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch('/api/parking/chart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(currentParkingData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            const chartContainer = document.getElementById('parking-chart-container');
            const chartImg = document.getElementById('parking-chart-img');
            
            chartImg.src = 'data:image/png;base64,' + result.chart;
            chartContainer.style.display = 'block';
            
            // 平滑滚动到图表
            chartContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            showError(result.message || '生成图表失败');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('网络请求失败，请检查服务器连接');
    } finally {
        showLoading(false);
    }
}

// 分析预订数据
async function analyzeBookingData() {
    const formData = {
        project: document.getElementById('project').value,
        chart_type: document.getElementById('booking-chart-type').value,
        start_date: document.getElementById('booking-start-date').value,
        end_date: document.getElementById('booking-end-date').value
    };
    
    showLoading(true);
    
    try {
        const response = await fetch('/api/booking/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentBookingData = {
                data: result.data,
                ...formData
            };
            displayBookingResults(result.data);
            document.getElementById('booking-chart-btn').style.display = 'block';
            document.getElementById('booking-chart-container').style.display = 'none';
        } else {
            showError(result.message || '查询失败');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('网络请求失败，请检查服务器连接');
    } finally {
        showLoading(false);
    }
}

// 显示预订数据结果
function displayBookingResults(data) {
    const resultsContainer = document.getElementById('booking-results');
    
    if (!data || data.length === 0) {
        resultsContainer.innerHTML = '<div class="empty-state"><p>未找到符合条件的数据</p></div>';
        return;
    }
    
    let html = '';
    data.forEach((item, index) => {
        html += `
            <div class="result-card">
                <div class="result-rank">#${index + 1}</div>
                <div class="result-location">${item[0]}</div>
                <div class="result-count">${item[1].toLocaleString()} 人</div>
            </div>
        `;
    });
    
    resultsContainer.innerHTML = html;
}

// 生成预订数据图表
async function generateBookingChart() {
    if (!currentBookingData) {
        showError('请先查询数据');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch('/api/booking/chart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(currentBookingData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            const chartContainer = document.getElementById('booking-chart-container');
            const chartImg = document.getElementById('booking-chart-img');
            
            chartImg.src = 'data:image/png;base64,' + result.chart;
            chartContainer.style.display = 'block';
            
            // 平滑滚动到图表
            chartContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            showError(result.message || '生成图表失败');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('网络请求失败，请检查服务器连接');
    } finally {
        showLoading(false);
    }
}

// 显示/隐藏加载动画
function showLoading(show) {
    const overlay = document.getElementById('loading-overlay');
    if (show) {
        overlay.classList.add('active');
    } else {
        overlay.classList.remove('active');
    }
}

// 显示错误消息
function showError(message) {
    alert('❌ ' + message);
}
