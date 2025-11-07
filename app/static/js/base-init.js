console.log('base-init.js loading...'); // 添加调试日志

// 初始化日期时间显示
function initializeDateTime() {
    console.log('Initializing date time...'); // 添加调试日志
    // 更新年份
    const yearElement = document.getElementById('current-year');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
    
    // 更新时间
    function updateTime() {
        const timeElement = document.getElementById('current-time');
        if (timeElement) {
            timeElement.textContent = moment().format('YYYY-MM-DD HH:mm:ss');
        }
    }
    updateTime();
    setInterval(updateTime, 1000);
}

// 初始化语言选择器
function initializeLanguageSelector() {
    console.log('Initializing language selector...'); // 添加调试日志
    const selector = document.getElementById('language-selector');
    if (selector) {
        // 设置初始值
        const currentLocale = localStorage.getItem('userLocale') || 'zh-CN';
        selector.value = currentLocale;
        
        // 添加切换事件
        selector.addEventListener('change', function(e) {
            const newLocale = e.target.value;
            localStorage.setItem('userLocale', newLocale);
            window.location.reload();
        });
    }
}

// DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded in base-init.js'); // 添加调试日志
    
    // 初始化本地化
    if (typeof moment !== 'undefined') {
        moment.locale('zh-CN');
    } else {
        console.error('moment is not loaded!');
    }
    
    // 更新时间日期显示
    initializeDateTime();
    
    // 初始化语言选择器
    initializeLanguageSelector();
});

// 添加错误处理
window.onerror = function(msg, url, line, col, error) {
    console.error('Error: ' + msg + '\nURL: ' + url + '\nLine: ' + line + '\nColumn: ' + col + '\nError object: ' + error);
    return false;
}; 