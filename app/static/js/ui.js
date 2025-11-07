const ui = {  
    updateStagesList(stages, currentStage) {  
        console.log('going to setup currentStage======', currentStage)
        const statesList = document.getElementById('states-list');  
        if (!statesList) return;  
        
        statesList.innerHTML = '';  
        
        // 创建阶段列表  
        stages.forEach((stageInfo) => {  
            const div = document.createElement('div');  
            const isCurrentStage = currentStage && stageInfo.id === currentStage.id;  
            const stageName = stageInfo.name || stageInfo.id;  
            
            div.className = `flex items-center p-2 rounded-lg cursor-pointer hover:bg-gray-100 ${isCurrentStage ? 'bg-blue-100' : ''}`;  
            div.innerHTML = `  
                <div class="w-3 h-3 rounded-full ${isCurrentStage ? 'bg-blue-500' : 'bg-gray-300'} mr-2"  style="white-space: pre-wrap;"></div>  
                <span class="mr-2">${stageInfo.index || ''}</span>  
                <span>${stageName}</span>  
            `;  
            
            // 点击事件处理  
            div.addEventListener('click', async () => {  
                const response = await api.setStage(stageInfo.id);  
                if (response.success) {  
                    this.updateStagesList(stages, { id: stageInfo.id });  
                    
                    const stageContent = await api.loadStageContent(stageInfo.id);  
                    if (stageContent.success && stageContent.data.stage_info) {  
                        const guideContent = document.getElementById('stage-guide-content');  
                        if (guideContent) {  
                            str = stageContent.data.stage_info.description + "\nyou need to complete the following tasks:" 
                            console.log('stageContent.data.stage_info:', stageContent.data.stage_info.tasks)
                            for(const task of stageContent.data.stage_info.tasks){
                                console.log("task", task)
                                str += '\n' + task.prompt_template
                            }
                            guideContent.value =  str || '';  
                        }  
                    }  
                }  
            });  
            
            statesList.appendChild(div);  
        });  
        
        // 更新当前阶段显示  
        const currentStageDisplay = document.getElementById('current-stage-display');  
        if (currentStageDisplay) {  
            const currentStageName = currentStage ?   
                (stages.find(s => s.id === currentStage.id)?.name || currentStage.id) :   
                'not set';  
            currentStageDisplay.textContent = currentStageName;  
        }  
    },  
    
    addMessage(content, isUser) {  
        const chatMessages = document.getElementById('chat-messages');  
        if (!chatMessages) return;  
        
        const messageDiv = document.createElement('div');  
        messageDiv.className = `flex ${isUser ? 'justify-end' : 'justify-start'}`;  
        messageDiv.innerHTML = `  
            <div class="max-w-[60%] ${isUser ? 'bg-blue-500 text-white' : 'bg-gray-100'} rounded-lg px-3 py-2" style="white-space: pre-wrap;">${content.trim()}</div>`;  
        chatMessages.appendChild(messageDiv);  
        chatMessages.scrollTop = chatMessages.scrollHeight;  
    },  
    
    showError(message) {  
        const chatMessages = document.getElementById('chat-messages');  
        if (!chatMessages) return;  
        
        chatMessages.innerHTML = `  
            <div class="flex justify-center">  
                <div class="bg-red-100 text-red-700 px-4 py-2 rounded-lg">  
                    ${message}  
                </div>  
            </div>  
        `;  
    }  
};