// API 配置  
// const API_BASE_URL = 'https:192.168.0.5:8443';  

// 获取用户名的辅助函数  
function getUsername() {  
    return localStorage.getItem('username');  
}  

// 添加用户名到请求体的辅助函数  
function addUsernameToBody(body = {}) {  
    const username = getUsername();  
    if (username) {  
        return { ...body, username };  
    }  
    return body;  
}  

// API 请求函数  
const api = {  
    async getAllStages() {  
        const response = await fetch(`/get_all_stages`, {  
            method: 'POST',  // 改为 POST 以支持在 body 中传递用户名  
            headers: {  
                'Content-Type': 'application/json'  
            },  
            body: JSON.stringify(addUsernameToBody())  
        });  
        return await response.json();  
    },  

    async loadHistory() {  
        const response = await fetch(`/load_history`, {  
            method: 'POST',  
            headers: {  
                'Content-Type': 'application/json'  
            },  
            body: JSON.stringify(addUsernameToBody())  
        });  
        return await response.json();  
    },  

    async setStage(stage) {  
        const response = await fetch(`/set_stage`, {  
            method: 'POST',  
            headers: {  
                'Content-Type': 'application/json'  
            },  
            body: JSON.stringify(addUsernameToBody({ stage }))  
        });  
        return await response.json();  
    },  

    async loadStageContent(stage) {  
        if (!stage || typeof stage !== 'string') {  
            console.error('Invalid stage parameter:', stage);  
            return {  
                success: false,  
                error: 'Invalid stage parameter'  
            };  
        }  
        
        try {  
            const username = getUsername();  
            const url = `/get_stage?stage=${encodeURIComponent(stage)}${username ? `&username=${encodeURIComponent(username)}` : ''}`;  
            console.log('Requesting URL:', url);  
            
            const response = await fetch(url);  
            return await response.json();  
        } catch (error) {  
            console.error('Failed to load stage content:', error);  
            return {  
                success: false,  
                error: 'Failed to load stage content'  
            };  
        }  
    },  

    async saveGuideContent(content) {  
        const response = await fetch(`/save_guide_content`, {  
            method: 'POST',  
            headers: {  
                'Content-Type': 'application/json'  
            },  
            body: JSON.stringify(addUsernameToBody({ content }))  
        });  
        return await response.json();  
    },  

    async sendChatMessage(message) {  
        try {  
            const response = await fetch('/chat', {  
                method: 'POST',  
                headers: {  
                    'Content-Type': 'application/json',  
                },  
                body: JSON.stringify(addUsernameToBody({ message })),  
            });  

            const data = await response.json();  
            
            if (!data.success) {  
                throw new Error(data.error || '发送消息失败');  
            }  

            return {  
                response: data.data.response,  
                history: data.data.history,  
                currentStage: data.data.current_stage,  
                currentTask: data.data.current_task,  
                stageChanged: data.data.stage_changed  
            };  
        } catch (error) {  
            console.error('Chat API Error:', error);  
            throw error;  
        }  
    },  
    
    // 新增：设置用户名的方法  
    async setUsername(username) {  
        try {  
            const response = await fetch('/set_username', {  
                method: 'POST',  
                headers: {  
                    'Content-Type': 'application/json',  
                },  
                body: JSON.stringify({ username })  
            });  

            if (!response.ok) {  
                throw new Error('Failed to set username');  
            }  

            return await response.json();  
        } catch (error) {  
            console.error('API Error:', error);  
            throw error;  
        }  
    },  

    // 获取当前用户信息  
    async getCurrentUser() {  
        try {  
            const response = await fetch('/get_current_user');  
            if (!response.ok) {  
                throw new Error('Failed to get current user');  
            }  
            return await response.json();  
        } catch (error) {  
            console.error('API Error:', error);  
            throw error;  
        }  
    },  

    async logoutUser(username) {  
        try {  
            const response = await fetch(`/logout_user`, {  
                method: 'POST',  
                headers: {  
                    'Content-Type': 'application/json'  
                },  
                body: JSON.stringify({ username })  
            });  
            return await response.json();  
        } catch (error) {  
            console.error('Error logging out user:', error);  
            throw error;  
        }  
    },

    // 新增语音相关的 API 方法  
    async transcribeAudio(audioBlob, username = null) {  
        const formData = new FormData();  
        formData.append('file', audioBlob, 'audio.webm');  
        formData.append('model', 'whisper-1');  
        if (username) {  
            formData.append('username', username);  
        }  

        const response = await fetch(`/api/transcribe`, {  
            method: 'POST',  
            body: formData  
        });  

        if (!response.ok) {  
            throw new Error('Transcription failed');  
        }  

        return await response.json();  
    },  

    async textToSpeech(text, options = {}, username = null) {  
        const defaultOptions = {  
            voice: 'alloy',  
            model: 'tts-1',  
            speed: 1.0  
        };  

        const payload = {  
            text,  
            ...defaultOptions,  
            ...options  
        };  

        if (username) {  
            payload.username = username;  
        }  

        const response = await fetch(`/api/tts`, {  
            method: 'POST',  
            headers: {  
                'Content-Type': 'application/json'  
            },  
            body: JSON.stringify(payload)  
        });  

        if (!response.ok) {  
            throw new Error('TTS request failed');  
        }  

        return await response.blob();  
    },
};