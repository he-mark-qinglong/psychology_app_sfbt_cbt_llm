// 初始化函数  
async function initialize() {  
    try {  
        console.log('Starting initialization...');  
        
        async function regetAllstages(){
            const stageData = await api.getAllStages();  
            if (stageData.success) {  
                // 将stages对象转换为数组并按index排序  
                const sortedStages = Object.entries(stageData.data.stages)  
                .map(([stageId, stageInfo]) => ({  
                    id: stageId,  
                    ...stageInfo  
                }))  
                .sort((a, b) => (a.index || 0) - (b.index || 0)); 
                stageData.data.stages = sortedStages
                
                ui.updateStagesList(stageData.data.stages, stageData.data.current_stage);  
                
                // 修改这部分逻辑  
                if (stageData.data.current_stage) {  
                    // 确保使用 current_stage 的 id  
                    const currentStageId = stageData.data.current_stage.id || stageData.data.current_stage;  
                    console.log('Loading content for stage:', stageData.data.current_stage); // 调试日志  
                    
                    const stageContent = await api.loadStageContent(currentStageId);  
                    if (stageContent.success) {  
                        const guideContent = document.getElementById('stage-guide-content');  
                        if (guideContent && stageContent.data.stage_info) {  
                            guideContent.value = stageContent.data.stage_info.description || '';  
                        }  
                    }  
                }  
            }  
        }  
        regetAllstages()
        
        const historyData = await api.loadHistory();  
        if (historyData.success && historyData.data.history) {  
            const chatMessages = document.getElementById('chat-messages');  
            chatMessages.innerHTML = '';  
            
            for (const message of historyData.data.history) {  
                ui.addMessage(message.content, message.role === 'user');  
            }  
        }  
        
        document.addEventListener("stageChange", async (event)=>{
            regetAllstages();
            // const { stage, task } = event.detail;  
    
            // // 现在你可以使用 stage 数据  
            // console.log('New stage:', stage);  
            // console.log('New task:', task);  
            // console.log('stage changed from event:', stage)
            // ui.updateStagesList(stageData.data.stages,  stage );
        });

        console.log('Initialization completed successfully');  
    } catch (error) {  
        console.error('Initialization failed:', error);  
        ui.showError('Initialization failed, please try again');  
    }  
}  

// 在页面加载时更新用户名显示  
function updateUsernameDisplay() {  
    const currentUsername = localStorage.getItem('username');  
    const usernameElement = document.getElementById('current-username');  
    if (usernameElement) {  
        usernameElement.textContent = currentUsername || 'login required';  
    }  
}  
 

// 页面加载完成后初始化  
document.addEventListener('DOMContentLoaded', () => {  
    console.log('DOMContentLoaded event fired');  
    
    // 初始化应用  
    initialize().catch(error => {  
        console.error('Initialization failed:', error);  
    });  

    updateUsernameDisplay();
    // 初始化聊天管理器  
    const chatManager = new ChatManager();  
    
    // 设置事件监听器    
    const saveButton = document.getElementById('save-guide-btn');  

    if (saveButton) {  
        saveButton.addEventListener('click', saveGuideContent);  
    }  

    // 添加更换用户按钮事件监听  
    const changeUserBtn = document.getElementById('change-user-btn');  
    if (changeUserBtn) {  
        changeUserBtn.addEventListener('click', () => {  
            if (window.authManager) {  
                window.authManager.logout(); 
                updateUsernameDisplay(); 
            }  
        });  
    }  
});