// 停车数据分析模块
let currentData = null;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializePage();
});

// 初始化页面
function initializePage() {
    setDefaultDates();
    loadOptions();
    bindEvents();
}

// 设置默认日期
function setDefaultDates() {
    const today = new Date();
    const thirtyDaysAgo = new Date(today);
    thirtyDaysAgo.setDate(today.getDate() - 30);
    
    document.getElementById('start-date').value = formatDate(thirtyDaysAgo);
    document.getElementById('end-date').value = formatDate(today);
}

// 格式化日期
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

// 加载选项
async function loadOptions() {
    try {
        const response = await fetch('/parking/api/options');
        const result = await response.json();
        
        if (result.success) {
            populateSelect('parking-lot', result.data.parking_lots);
            populateSelect('chart-type', result.data.chart_types);
        }
    } catch (error) {
        console.error('加载选项失败:', error);
    }
}

// 填充下拉框
function populateSelect(id, options) {
    const select = document.getElementById(id);
    select.innerHTML = '';
    options.forEach(option => {
        const opt = document.createElement('option');
        opt.value = option;
        opt.textContent = option;
        select.appendChild(opt);
    });
}

// 绑定事件
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

// 处理表单提交
async function handleSubmit(e) {
    e.preventDefault();
    
    const formData = {
        parking_lot: document.getElementById('parking-lot').value,
        chart_type: document.getElementById('chart-type').value,
        start_date: document.getElementById('start-date').value,
        end_date: document.getElementById('end-date').value
    };
    
    showLoading(true);
    
    try {
        // 判断是否为驻留时长分析
        if (formData.chart_type === '驻留时长分析') {
            await handleDurationAnalysis(formData);
        } else {
            const response = await fetch('/parking/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                currentData = { data: result.data, ...formData };
                displayResults(result.data);
                document.getElementById('chart-btn').style.display = 'block';
                document.getElementById('chart-container').style.display = 'none';
            } else {
                showError(result.message || '查询失败');
            }
        }
    } catch (error) {
        console.error('查询失败:', error);
        showError('网络请求失败，请检查服务器连接');
    } finally {
        showLoading(false);
    }
}

// 显示结果
function displayResults(data) {
    const container = document.getElementById('results-container');
    
    if (!data || data.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>未找到符合条件的数据</p></div>';
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
    
    container.innerHTML = html;
}

// 生成图表
async function generateChart() {
    if (!currentData) {
        showError('请先查询数据');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch('/parking/api/chart', {
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

// 显示/隐藏加载动画
function showLoading(show) {
    const overlay = document.getElementById('loading-overlay');
    overlay.classList.toggle('active', show);
}

// 显示错误
function showError(message) {
    alert('❌ ' + message);
}

// 处理驻留时长分析
async function handleDurationAnalysis(formData) {
    const response = await fetch('/parking/api/duration', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            parking_lot: formData.parking_lot,
            start_date: formData.start_date,
            end_date: formData.end_date
        })
    });
    
    const result = await response.json();
    
    if (result.success) {
        displayDurationResults(result);
        document.getElementById('chart-btn').style.display = 'none';
        document.getElementById('chart-container').style.display = 'none';
    } else {
        showError(result.message || '驻留时长分析失败');
    }
}

// 显示驻留时长分析结果
function displayDurationResults(result) {
    const container = document.getElementById('results-container');
    
    if (!result.distribution || result.distribution.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>未找到符合条件的数据</p></div>';
        return;
    }
    
    let html = '<div class="duration-analysis">';
    
    // 1. 驻留时长分布
    html += '<div class="duration-section">';
    html += '<h3>📊 驻留时长分布</h3>';
    html += '<div class="duration-distribution">';
    
    result.distribution.forEach(item => {
        const range = item[0];
        const count = item[1];
        const percentage = item[2];
        
        html += `
            <div class="duration-card">
                <div class="duration-range">${range}</div>
                <div class="duration-stats">
                    <div class="duration-count">${count.toLocaleString()} 辆</div>
                    <div class="duration-percentage">${percentage}%</div>
                </div>
                <div class="duration-bar">
                    <div class="duration-bar-fill" style="width: ${percentage}%"></div>
                </div>
            </div>
        `;
    });
    
    html += '</div></div>';
    
    // 2. 省份驻留时长对比
    if (result.province_comparison && result.province_comparison.length > 0) {
        html += '<div class="duration-section">';
        html += '<h3>🗺️ 各省份平均驻留时长 (Top 20)</h3>';
        html += '<div class="province-comparison">';
        
        result.province_comparison.forEach((item, index) => {
            const province = item[0];
            const count = item[1];
            const avgHours = item[2];
            const maxHours = item[3];
            
            html += `
                <div class="province-card">
                    <div class="province-rank">#${index + 1}</div>
                    <div class="province-name">${province}</div>
                    <div class="province-stats">
                        <div class="stat-item">
                            <span class="stat-label">车辆数:</span>
                            <span class="stat-value">${count.toLocaleString()}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">平均:</span>
                            <span class="stat-value highlight">${avgHours} 小时</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">最长:</span>
                            <span class="stat-value">${maxHours} 小时</span>
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += '</div></div>';
    }
    
    // 3. 驻留时长趋势
    if (result.trend && result.trend.length > 0) {
        html += '<div class="duration-section">';
        html += '<h3>📈 驻留时长趋势</h3>';
        html += '<div class="trend-table">';
        html += '<table><thead><tr><th>日期</th><th>车辆数</th><th>平均驻留时长</th></tr></thead><tbody>';
        
        result.trend.forEach(item => {
            const dateStr = item[0];
            const count = item[1];
            const avgHours = item[2];
            
            // 格式化日期为 YYYY-MM-DD
            const formattedDate = formatDisplayDate(dateStr);
            
            html += `
                <tr>
                    <td>${formattedDate}</td>
                    <td>${count.toLocaleString()} 辆</td>
                    <td><strong>${avgHours} 小时</strong></td>
                </tr>
            `;
        });
        
        html += '</tbody></table></div></div>';
    }
    
    html += '</div>';
    container.innerHTML = html;
}
