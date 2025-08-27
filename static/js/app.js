// Global variables
let activeInstances = new Set();
let updateInterval;
let completedInstances = new Set();

// DOM Elements
const attackForm = document.getElementById('attackForm');
const alertContainer = document.getElementById('alertContainer');
const instancesContainer = document.getElementById('instancesContainer');

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    attackForm.addEventListener('submit', handleAttackSubmit);
    updateInstances();
    startStatusUpdates();
});

// Form submission handler
async function handleAttackSubmit(e) {
    e.preventDefault();
    
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    // Show loading state
    setButtonLoading(submitBtn, 'Đang Bắt Đầu Tấn Công...');
    
    const formData = getFormData();
    
    if (!validateFormData(formData)) {
        resetButton(submitBtn, originalText);
        return;
    }
    
    try {
        const response = await startAttack(formData);
        
        if (response.ok) {
            const data = await response.json();
            showAlert(data.message, 'success');
            activeInstances.add(data.instance_id);
            updateInstances();
            startStatusUpdates();
            monitorAttackCompletion();
            resetForm();
        } else {
            const data = await response.json();
            showAlert(data.error, 'danger');
        }
    } catch (error) {
        showAlert('Lỗi khi bắt đầu tấn công: ' + error.message, 'danger');
    } finally {
        resetButton(submitBtn, originalText);
    }
}

// Get form data
function getFormData() {
    return {
        username: document.getElementById('username').value.trim(),
        threads: parseInt(document.getElementById('threads').value),
        question: document.getElementById('question').value.trim() || 'mNGL Tool',
        enable_emoji: document.getElementById('enableEmoji').checked
    };
}

// Validate form data
function validateFormData(data) {
    if (!data.username) {
        showAlert('Vui lòng nhập tên người dùng', 'danger');
        return false;
    }
    
    if (data.threads < 1 || data.threads > 500) {
        showAlert('Số threads phải từ 1 đến 500', 'danger');
        return false;
    }
    
    return true;
}

// Start attack API call
async function startAttack(data) {
    return await fetch('/start', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });
}

// Reset form
function resetForm() {
    attackForm.reset();
    document.getElementById('threads').value = '50';
}

// Button utilities
function setButtonLoading(button, text) {
    button.innerHTML = `<span class="loading-spinner"></span> ${text}`;
    button.disabled = true;
}

function resetButton(button, originalText) {
    button.innerHTML = originalText;
    button.disabled = false;
}

// Alert system
function showAlert(message, type) {
    const alert = createAlertElement(message, type);
    alertContainer.appendChild(alert);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 3000);
}

function createAlertElement(message, type) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    
    const icon = getAlertIcon(type);
    
    alert.innerHTML = `
        <i class="fas ${icon}"></i>
        ${message}
        <button class="alert-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    return alert;
}

function getAlertIcon(type) {
    switch (type) {
        case 'success': return 'fa-check-circle';
        case 'danger': return 'fa-exclamation-triangle';
        case 'info': return 'fa-info-circle';
        default: return 'fa-info-circle';
    }
}

// Update instances display
async function updateInstances() {
    try {
        const response = await fetch('/instances');
        const instances = await response.json();
        
        if (instances.length === 0) {
            instancesContainer.innerHTML = '<p class="text-muted">Không có cuộc tấn công nào đang hoạt động</p>';
            return;
        }
        
        const html = generateInstancesHTML(instances);
        instancesContainer.innerHTML = html;
        
        updateStatistics(instances);
        
    } catch (error) {
        console.error('Error updating instances:', error);
    }
}

// Generate HTML for instances
function generateInstancesHTML(instances) {
    let html = '';
    
    instances.forEach(instance => {
        const progress = (instance.successful_runs / instance.target_threads) * 100;
        const statusClass = `status-${instance.status}`;
        const statusIcon = getStatusIcon(instance.status);
        const statusText = getStatusText(instance.status);
        
        html += `
            <div class="status-card ${statusClass} ${instance.status === 'running' ? 'pulse' : ''}">
                <div class="status-header">
                    <h4>
                        <i class="fas ${statusIcon}"></i> Cuộc Tấn Công #${instance.id}
                    </h4>
                    <span class="badge badge-${instance.status}">${statusText}</span>
                </div>
                
                <div class="status-details">
                    <p><strong>Tên Người Dùng:</strong> ${instance.username}</p>
                    <p><strong>Tin Nhắn:</strong> ${instance.question}</p>
                    <p><strong>Tiến Độ:</strong> ${instance.successful_runs}/${instance.target_threads} tin nhắn đã gửi</p>
                    ${instance.completion_message ? `<p class="completion-message"><i class="fas fa-check-circle"></i> ${instance.completion_message}</p>` : ''}
                </div>
                
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${progress}%"></div>
                </div>
                
                ${instance.status === 'running' ? 
                    `<button class="btn btn-danger" onclick="stopAttack(${instance.id})">
                        <i class="fas fa-stop"></i> Dừng Tấn Công
                    </button>` : ''
                }
            </div>
        `;
    });
    
    return html;
}

// Get status icon
function getStatusIcon(status) {
    switch (status) {
        case 'running': return 'fa-play';
        case 'completed': return 'fa-check';
        case 'stopped': return 'fa-pause';
        case 'error': return 'fa-exclamation-triangle';
        default: return 'fa-info-circle';
    }
}

// Get status text
function getStatusText(status) {
    switch (status) {
        case 'running': return 'ĐANG CHẠY';
        case 'completed': return 'HOÀN THÀNH';
        case 'stopped': return 'ĐÃ DỪNG';
        case 'error': return 'LỖI';
        default: return 'UNKNOWN';
    }
}

// Update statistics
function updateStatistics(instances) {
    let totalMessages = 0;
    let activeCount = 0;
    
    instances.forEach(instance => {
        if (instance.status === 'running') activeCount++;
        totalMessages += instance.successful_runs;
    });
    
    document.getElementById('totalAttacks').textContent = instances.length;
    document.getElementById('totalMessages').textContent = totalMessages;
    document.getElementById('activeAttacks').textContent = activeCount;
}

// Stop attack
async function stopAttack(instanceId) {
    const button = event.target.closest('button');
    const originalText = button.innerHTML;
    
    setButtonLoading(button, 'Đang Dừng...');
    
    try {
        const response = await fetch(`/stop/${instanceId}`);
        const data = await response.json();
        
        if (response.ok) {
            showAlert(data.message, 'info');
            setTimeout(() => updateInstances(), 1000);
        } else {
            showAlert(data.error, 'danger');
            resetButton(button, originalText);
        }
    } catch (error) {
        showAlert('Lỗi khi dừng tấn công: ' + error.message, 'danger');
        resetButton(button, originalText);
    }
}

// Monitor attack completion
function monitorAttackCompletion() {
    const checkCompletion = async () => {
        try {
            const response = await fetch('/instances');
            const instances = await response.json();
            
            instances.forEach(instance => {
                if (instance.status === 'completed' && 
                    instance.completion_message && 
                    !completedInstances.has(instance.id)) {
                    showAlert(instance.completion_message, 'success');
                    completedInstances.add(instance.id);
                }
            });
        } catch (error) {
            console.error('Error monitoring completion:', error);
        }
    };
    
    // Check every 2 seconds for completion
    const interval = setInterval(checkCompletion, 2000);
    
    // Stop monitoring after 5 minutes
    setTimeout(() => {
        clearInterval(interval);
    }, 300000);
}

// Start status updates
function startStatusUpdates() {
    if (updateInterval) clearInterval(updateInterval);
    updateInterval = setInterval(updateInstances, 2000);
}
