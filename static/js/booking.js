// 预订数据分析模块
let currentData = null;

document.addEventListener('DOMContentLoaded', function() {
    initializePage();
});

function initializePage() {
    setDefaultDates();
    loadOptions();
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

async function loadOptions() {
    try {
        const response = await fetch('/booking/api/options');
        const result = await response.json();
        
        if (result.success) {
            populateSelect('project', result.data.projects);
            populateSelect('chart-type', result.data.chart_types);
        }
    } catch (error) {
        console.error('加载选项失败:', error);
    }
}

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
        project: document.getElementById('project').value,
        chart_type: document.getElementById('chart-type').value,
        start_date: document.getElementById('start-date').value,
        end_date: document.getElementById('end-date').value
    };
    
    showLoading(true);
    
    try {
        const response = await fetch('/booking/api/analyze', {
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
    } catch (error) {
        console.error('查询失败:', error);
        showError('网络请求失败，请检查服务器连接');
    } finally {
        showLoading(false);
    }
}

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
                <div class="result-count">${item[1].toLocaleString()} 人</div>
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
        const response = await fetch('/booking/api/chart', {
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
