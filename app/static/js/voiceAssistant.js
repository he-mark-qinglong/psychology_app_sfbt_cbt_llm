class OpenAIVoiceAssistant {  
    constructor() {  
        this.mediaRecorder = null;  
        this.audioChunks = [];  
        this.isRecording = false;  
        this.silenceTimer = null;  
        this.recordingTimer = null;  
        this.audioContext = null;  
        this.analyser = null;  
        this.active = true;  

        // 配置参数  
        this.MAX_RECORDING_TIME = 60000;  
        this.SILENCE_THRESHOLD = 15;  
        this.SILENCE_DURATION = 1500;  

        this.setupEventListeners();  
    }  

    setupEventListeners() {  
        const voiceButton = document.getElementById('voice-toggle');  
        voiceButton?.addEventListener('click', () => {  
            if (this.isRecording) {  
                this.stopRecording();  
            } else {  
                this.startRecording();  
            }  
        });  
    }  

    async startRecording() {  
        if (this.isRecording) return;  
        
        try {  
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });  
            this.mediaRecorder = new MediaRecorder(stream);  
            this.audioChunks = [];  
            this.isRecording = true;  

            this.setupAudioAnalysis(stream);  
            this.updateUI(true);  

            this.mediaRecorder.ondataavailable = (event) => {  
                this.audioChunks.push(event.data);  
            };  

            this.mediaRecorder.onstop = async () => {  
                if (this.audioChunks.length > 0) {  
                    const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });  
                    await this.handleAudioTranscription(audioBlob);  
                }  
            };  

            this.mediaRecorder.start();  
            this.startRecordingTimers();  

        } catch (error) {  
            console.error('Recording failed:', error);  
            this.showError('failed to access microphone');  
        }  
    }  

    async handleAudioTranscription(audioBlob) {  
        this.showRecordingFeedback('transcribing...');  
        
        try {  
            const transcriptionResult = await api.transcribeAudio(audioBlob);  
            
            if (transcriptionResult.success && transcriptionResult.data.text) {  
                await this.handleTranscriptionResponse(transcriptionResult.data);  
            }  
        } catch (error) {  
            console.error('Transcription failed:', error);  
            this.showError('voice to text failed');  
        } finally {  
            this.showRecordingFeedback('');  
        }  
    }  

    async handleTranscriptionResponse(data) {  
        ui.addMessage(data.text, true);  

        try {  
            const chatResponse = await api.sendChatMessage(data.text);  
            
            if (chatResponse) {  
                ui.addMessage(chatResponse.response, false);  
                
                if (this.active) {  
                    await this.handleTextToSpeech(chatResponse.response);  
                }  

                this.updateChatState(chatResponse);  
            }  
        } catch (error) {  
            console.error('Chat processing failed:', error);  
            this.showError('chat processing failed');  
        }  
    }  

    async handleTextToSpeech(text) {  
        try {  
            const audioBlob = await api.textToSpeech(text);  
            await this.playAudio(audioBlob);  
        } catch (error) {  
            console.error('TTS failed:', error);  
            this.showError('voice to text failed');  
        }  
    }  

    async playAudio(audioBlob) {  
        const audioUrl = URL.createObjectURL(audioBlob);  
        const audio = new Audio(audioUrl);  
        
        audio.onended = () => {  
            URL.revokeObjectURL(audioUrl);  
        };  

        await audio.play();  
    }  

    updateChatState(chatResponse) {  
        if (window.chatManager) {  
            window.chatManager.handleStageChange(  
                chatResponse.currentStage,  
                chatResponse.currentTask  
            );  

            if (chatResponse.history) {  
                window.chatManager.updateChatHistory(chatResponse.history);  
            }  
        }  
    }  

    // ... (其他现有方法保持不变)  

    updateUI(isRecording) {  
        const voiceButton = document.getElementById('voice-toggle');  
        if (voiceButton) {  
            voiceButton.classList.toggle('active', isRecording);  
        }  
        this.showRecordingFeedback(isRecording ? 'recording...' : '');  
    }  

    startRecordingTimers() {  
        this.recordingTimer = setTimeout(() => {  
            if (this.isRecording) {  
                this.stopRecording();  
            }  
        }, this.MAX_RECORDING_TIME);  
    }  
}  

// 创建全局实例  
window.voiceAssistant = new OpenAIVoiceAssistant();  

// 初始化事件监听  
document.addEventListener('DOMContentLoaded', () => {  
    const voiceToggle = document.getElementById('voice-toggle');  
    voiceToggle?.addEventListener('dblclick', () => {  
        window.voiceAssistant.toggleActive();  
    });  
});  