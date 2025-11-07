class AuthManager {  
    constructor() {  
        this.modal = document.getElementById('username-modal');  
        this.usernameInput = document.getElementById('username-input');  
        this.confirmButton = document.getElementById('confirm-username');  
        this.errorText = document.getElementById('username-error');  
        
        this.init();  
    }  

    init() {  
        this.checkExistingUser();  
        this.setupEventListeners();  
    }  

    checkExistingUser() {  
        if (!localStorage.getItem('username')) {  
            this.showModal();  
        }  
    }  

    setupEventListeners() {  
        this.confirmButton?.addEventListener('click', () => this.handleUsernameSubmit());  
        this.usernameInput?.addEventListener('input', () => this.hideError());  
    }  

    showModal() {  
        this.modal?.classList.remove('hidden');  
    }  

    hideModal() {  
        this.modal?.classList.add('hidden');  
    }  

    showError() {  
        this.errorText?.classList.remove('hidden');  
    }  

    hideError() {  
        this.errorText?.classList.add('hidden');  
    }  

    async handleUsernameSubmit() {  
        const username = this.usernameInput?.value.trim();  
        //没有考虑异常处理的，比如特殊字符。
        if (!username || username.length < 2) {  
            this.showError();  
            return;  
        }  

        try {  
            const response = await api.setUsername(username);  
            if (response.success) {  
                localStorage.setItem('username', username);  
                this.hideModal();  
                // 方式1：直接刷新当前页面  
                window.location.reload();  
                
                // 或者方式2：重新导航到chat页面  
                // window.location.href = '/';  // 假设chat.html是根路径  
                
                // 如果chat.html有特定路径，则使用具体路径  
                // window.location.href = '/chat.html';
            } else {  
                this.showError();  
            }  
        } catch (error) {  
            console.error('Failed to set username:', error);  
            this.showError();  
        }  
    }  

    static getCurrentUsername() {  
        return localStorage.getItem('username');  
    }  
    async logout() {  
        // 获取当前用户并注销  
        const currentUsername = localStorage.getItem('username');  
        if (currentUsername) {  
            await api.logoutUser(currentUsername);  
            localStorage.removeItem('username'); // 清除本地存储的用户名  
        }  
        localStorage.removeItem('username');  
        window.location.reload(); // 刷新页面以显示登录框  
    }  
}  

// 创建全局实例  
window.authManager = new AuthManager();  

export default AuthManager;