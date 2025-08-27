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
    // Force clear any existing instances first
    if (instancesContainer) {
        instancesContainer.innerHTML = '';
    }
    
    attackForm.addEventListener('submit', handleAttackSubmit);
    updateInstances();
    startStatusUpdates();
    
    // Add mobile-specific optimizations
    addMobileOptimizations();
});

// Mobile optimizations
function addMobileOptimizations() {
    // Prevent zoom on input focus (iOS)
    const inputs = document.querySelectorAll('input, textarea');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            if (window.innerWidth <= 768) {
                setTimeout(() => {
                    this.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }, 300);
            }
        });
    });
    
    // Add touch feedback
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.95)';
        });
        
        button.addEventListener('touchend', function() {
            this.style.transform = '';
        });
    });
    
    // Optimize for mobile performance
    if (window.innerWidth <= 768) {
        // Reduce update frequency on mobile
        if (updateInterval) clearInterval(updateInterval);
        updateInterval = setInterval(updateInstances, 3000); // 3 seconds instead of 2
    }
}

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
            
            // Scroll to instances on mobile
            if (window.innerWidth <= 768) {
                setTimeout(() => {
                    instancesContainer.scrollIntoView({ behavior: 'smooth' });
                }, 500);
            }
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
        question: document.getElementById('question').value.trim() || 'Marine',
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
    
    if (data.question.length > 70) {
        showAlert('Tin nhắn không được quá 70 ký tự', 'danger');
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
        <span>${message}</span>
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
        const allInstances = await response.json();
        
        // Debug: Log all instances to see what we're getting
        console.log('All instances received:', allInstances);
        
        // Filter out completed or stopped attacks - only show running ones
        const instances = allInstances.filter(instance => {
            console.log(`Instance ${instance.id}: status = ${instance.status}`);
            return instance.status === 'running';
        });
        
        console.log('Filtered instances (running only):', instances);
        
        // Force clear the container first
        instancesContainer.innerHTML = '';
        
        if (instances.length === 0) {
            instancesContainer.innerHTML = `
                <div style="text-align: center; padding: 40px 20px;">
                    <i class="fas fa-info-circle" style="font-size: 3rem; color: #666; margin-bottom: 15px;"></i>
                    <p class="text-muted">Không có cuộc tấn công nào đang hoạt động</p>
                </div>
            `;
            console.log('Container cleared - no running instances');
            return;
        }
        
        const html = generateInstancesHTML(instances);
        console.log('Generated HTML for running instances:', html);
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
    
    // Update numbers directly without animation to avoid jumping
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
    
    // Force immediate update to apply filter
    updateInstances();
    
    // Adjust update frequency based on screen size - optimized for speed
    const updateFrequency = window.innerWidth <= 768 ? 1500 : 1000; // Giảm thời gian cập nhật để tăng tốc độ
    updateInterval = setInterval(updateInstances, updateFrequency);
}

// Handle window resize
window.addEventListener('resize', function() {
    // Restart status updates with new frequency
    startStatusUpdates();
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        if (document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA') {
            attackForm.dispatchEvent(new Event('submit'));
        }
    }
    
    // Escape to close alerts
    if (e.key === 'Escape') {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => alert.remove());
    }
});



// Add service worker for offline support (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('SW registered: ', registration);
            })
            .catch(function(registrationError) {
                console.log('SW registration failed: ', registrationError);
            });
    });
}


