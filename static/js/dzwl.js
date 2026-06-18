// 电子围栏客流分析模块
let currentData = null;

document.addEventListener('DOMContentLoaded', function() {
    initializePage();
});

function initializePage() {
    setDefaultDates();
    bindEvents();
}

function setDefaultDates() {
    const today = new Date();
    const thirtyDaysAgo = new Date(today);
    thirtyDaysAgo.setDate(today.getDate() - 30);
    
    document.getElementById('start-date').value = formatDate(thirtyDaysAgo);
    document.getElementById('end-date').value = formatDate(today);
}

function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// 格式化显示日期（处理后端返回的日期格式）
function formatDisplayDate(dateStr) {
    if (!dateStr) return '';
    
    // 如果已经是YYYY-MM-DD格式，直接返回
    if (/^\d{4}-\d{2}-\d{2}$/.test(dateStr)) {
        return dateStr;
    }
    
    // 处理GMT格式或其他Date格式
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) {
        return dateStr; // 如果无法解析，返回原始字符串
    }
    
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

function bindEvents() {
    document.getElementById('query-form').addEventListener('submit', handleSubmit);
    document.getElementById('chart-btn').addEventListener('click', generateChart);
    
    // 快速日期按钮
    document.querySelectorAll('.btn-quick').forEach(btn => {
        btn.addEventListener('click', function() {
            // 移除所有按钮的active类
            document.querySelectorAll('.btn-quick').forEach(b => b.classList.remove('active'));
            // 为当前按钮添加active类
            this.classList.add('active');
            
            const startDate = this.getAttribute('data-start');
            const endDate = this.getAttribute('data-end');
            document.getElementById('start-date').value = startDate;
            document.getElementById('end-date').value = endDate;
        });
    });
    
    // 手动修改日期时，移除所有快速按钮的active状态
    document.getElementById('start-date').addEventListener('change', clearQuickDateActive);
    document.getElementById('end-date').addEventListener('change', clearQuickDateActive);
}

function clearQuickDateActive() {
    document.querySelectorAll('.btn-quick').forEach(btn => btn.classList.remove('active'));
}

async function handleSubmit(e) {
    e.preventDefault();
    
    const formData = {
        start_date: document.getElementById('start-date').value,
        end_date: document.getElementById('end-date').value
    };
    
    showLoading(true);
    
    try {
        const response = await fetch('/dzwl/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentData = { data: result.data, ...formData };
            displayStatistics(result.statistics);
            displayResults(result.data);
            document.getElementById('chart-btn').style.display = 'block';
            document.getElementById('chart-container').style.display = 'none';
        } else {
            showError(result.message || '查询失败');
        }
    } catch (error) {
        console.error('查询失败:', error);
        showError('网络请求失败，请检查服务器连接');
    } finally {
        showLoading(false);
    }
}

function displayStatistics(stats) {
    const container = document.getElementById('stats-container');
    
    const html = `
        <div class="stat-card">
            <div class="stat-label">📅 统计天数</div>
            <div class="stat-value">${stats.days} 天</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">📥 总进入</div>
            <div class="stat-value" style="color: #2ca02c;">${parseInt(stats.total_enter).toLocaleString()} 人</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">📤 总离开</div>
            <div class="stat-value" style="color: #ff7f0e;">${parseInt(stats.total_exit).toLocaleString()} 人</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">📊 日均进入</div>
            <div class="stat-value" style="color: #9467bd;">${Math.round(stats.avg_enter).toLocaleString()} 人</div>
        </div>
    `;
    
    container.innerHTML = html;
}

function displayResults(data) {
    const container = document.getElementById('results-container');
    
    if (!data || data.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>未找到符合条件的数据</p></div>';
        return;
    }
    
    let html = '';
    data.forEach((item) => {
        const formattedDate = formatDisplayDate(item[0]);
        html += `
            <div class="flow-card">
                <div class="flow-date">${formattedDate}</div>
                <div class="flow-enter">进入: ${parseInt(item[1]).toLocaleString()} 人</div>
                <div class="flow-exit">离开: ${parseInt(item[2]).toLocaleString()} 人</div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

async function generateChart() {
    if (!currentData) {
        showError('请先查询数据');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch('/dzwl/api/chart', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            const chartContainer = document.getElementById('chart-container');
            const chartImg = document.getElementById('chart-img');
            
            chartImg.src = 'data:image/png;base64,' + result.chart;
            chartContainer.style.display = 'block';
            chartContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            showError(result.message || '生成图表失败');
        }
    } catch (error) {
        console.error('生成图表失败:', error);
        showError('网络请求失败');
    } finally {
        showLoading(false);
    }
}

function showLoading(show) {
    const overlay = document.getElementById('loading-overlay');
    overlay.classList.toggle('active', show);
}

function showError(message) {
    alert('❌ ' + message);
}
