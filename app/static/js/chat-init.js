console.log('chat-init.js loading...'); // 添加调试日志

// 处理聊天页面特定的初始化
document.addEventListener('DOMContentLoaded', async () => {
    console.log('DOM Content Loaded in chat-init.js'); // 添加调试日志
    
    try {
        // 检查必要的全局对象
        if (!window.ChatManager) {
            throw new Error('ChatManager is not defined');
        }
        
        // 初始化聊天管理器
        console.log('Initializing chat manager...'); // 添加调试日志
        window.chatManager = new ChatManager();
        
        // 加载阶段数据
        console.log('Loading stage data...'); // 添加调试日志
        await loadStageData();
        
        // 加载历史记录
        console.log('Loading chat history...'); // 添加调试日志
        await loadChatHistory();
        
    } catch (error) {
        console.error('Chat initialization failed:', error);
        if (window.ui) {
            ui.showError(i18n.t('初始化失败'));
        } else {
            console.error('UI module not loaded!');
        }
    }
}); 