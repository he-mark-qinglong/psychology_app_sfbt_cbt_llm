console.log('localization.js loading...');

// 确保 i18next 已加载
if (typeof i18next === 'undefined') {
    console.error('i18next is not loaded!');
    throw new Error('i18next is required');
}

const translations = {
    'zh-CN': {
        '未设置': '未设置',
        '阶段列表': '阶段列表',
        '阶段指导': '阶段指导',
        '输入消息...': '输入消息...',
        '发送': '发送',
        '保存修改': '保存修改',
        '初始化失败': '初始化失败',
        '当前用户：': '当前用户：',
        '未登录用户': '未登录用户',
        '切换用户': '切换用户',
        // ... 其他翻译
    },
    'en': {
        '未设置': 'Not Set',
        '阶段列表': 'Stage List',
        '阶段指导': 'Stage Guide',
        '输入消息...': 'Enter message...',
        '发送': 'Send',
        '保存修改': 'Save Changes',
        '初始化失败': 'Initialization Failed',
        '当前用户：': 'Current User:',
        '未登录用户': 'Not Logged In',
        '切换用户': 'Switch User',
        // ... 其他翻译
    }
};

// 初始化 i18next
console.log('Initializing i18next...');
i18next.init({
    lng: localStorage.getItem('userLocale') || 'zh-CN',
    resources: {
        'zh-CN': { translation: translations['zh-CN'] },
        'en': { translation: translations['en'] }
    },
    fallbackLng: 'zh-CN',
    debug: true
}).then(() => {
    console.log('i18next initialized with language:', i18next.language);
    // 触发语言更新事件
    document.dispatchEvent(new Event('languageChanged'));
});

// 监听语言变化
document.addEventListener('languageChanged', () => {
    console.log('Language changed, updating UI...');
    updateUITexts();
});

// 更新界面文本
function updateUITexts() {
    console.log('Updating UI texts...');
    // 更新所有带有 data-i18n 属性的元素
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        element.textContent = i18next.t(key);
    });
} 