// chat.js  

class ChatManager {  
    constructor() {  
        this.messageInput = document.getElementById('message-input');  
        this.setupEventListeners();  
    }  

    setupEventListeners() {  
        // 设置发送消息的事件监听  
        const sendButton = document.getElementById('send-button');
        console.log('sendButton addEventListener ', sendButton)  
        if (sendButton) {  
            sendButton.addEventListener('click', () => this.sendMessage());  
        }  

        // 设置输入框回车发送  
        this.messageInput?.addEventListener('keypress', (e) => {  
            if (e.key === 'Enter' && !e.shiftKey) {  
                e.preventDefault();  
                this.sendMessage();  
            }  
        });  
    }  

    async sendMessage() {  
        console.log('sendMessage')
        const content = this.messageInput.value.trim();  
        
        if (!content) return;  

        // 清空输入框  
        this.messageInput.value = '';  
        
        // 显示用户消息  
        ui.addMessage(content, true);  
        
        try {  
            // 调用新的聊天API  
            const response = await api.sendChatMessage(content);  
            
            if (response) {  
                // 显示助手回复  
                ui.addMessage(response.response, false);  
                // 如果语音助手处于激活状态，播放响应  
                // if (window.voiceAssistant && window.voiceAssistant.active) {  
                //     window.voiceAssistant.speakResponse(response.response);  
                // }  
                // 如果阶段发生变化，更新UI  
                // if (response.stageChanged) {  
                console.log('currentStage is ', response.currentStage)
                this.handleStageChange(response.currentStage, response.currentTask);  
                // }  
                
                // 如果需要更新历史记录  
                if (response.history) {  
                    this.updateChatHistory(response.history);  
                }  
            }  
        } catch (error) {  
            console.error('Failed to send message:', error);  
            ui.showError('Failed to send message, please try again');  
        }  
    }  

    handleStageChange(newStage, newTask) {  
        // 更新阶段显示  
        const stageDisplay = document.querySelector('.current-stage');  
        if (stageDisplay) {  
            stageDisplay.textContent = `current stage: ${newStage}`;  
        }  

        // 更新任务显示  
        const taskDisplay = document.querySelector('.current-task');  
        if (taskDisplay) {  
            taskDisplay.textContent = `current task: ${newTask}`;  
        }  

        // 触发阶段变化事件  
        const event = new CustomEvent('stageChange', {  
            detail: { stage: newStage, task: newTask }  
        });  
        document.dispatchEvent(event);  
    }  

    updateChatHistory(history) {  
        // 清空现有消息  
        const messageContainer = document.querySelector('.message-container');  
        if (messageContainer) {  
            messageContainer.innerHTML = '';  
            
            // 重新添加所有历史消息  
            history.forEach(msg => {  
                ui.addMessage(msg.content, msg.role === 'user');  
            });  
        }  
    }  
}  

// 保存指导内容的功能  
async function saveGuideContent() {  
    const content = document.getElementById('stage-guide-content')?.value;  
    if (!content) return;  

    try {  
        const response = await api.saveGuideContent(content);  
        if (response.success) {  
            ui.showNotification('guide content saved successfully');  
        }  
    } catch (error) {  
        console.error('Failed to save guide content:', error);  
        ui.showError('Failed to save guide content');  
    }  
}  

