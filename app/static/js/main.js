document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const styleButtons = document.querySelectorAll('[data-style]');
    const processingStatus = document.getElementById('processing-status');
    
    let selectedStyle = null;
    
    // 处理风格选择
    styleButtons.forEach(button => {
        button.addEventListener('click', function() {
            selectedStyle = this.dataset.style;
            // 更新UI显示选中状态
            styleButtons.forEach(btn => btn.classList.remove('border-purple-500'));
            this.classList.add('border-purple-500');
        });
    });
    
    // 处理图片上传和生成
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!selectedStyle) {
            alert('请选择写真风格');
            return;
        }
        
        const formData = new FormData(this);
        formData.append('style', selectedStyle);
        
        try {
            processingStatus.classList.remove('hidden');
            
            const response = await fetch('/api/generate', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.task_id) {
                // 开始轮询任务状态
                pollGenerationStatus(result.task_id);
            }
            
        } catch (error) {
            console.error('生成失败:', error);
            alert('生成失败，请重试');
        }
    });
    
    // 轮询生成状态
    async function pollGenerationStatus(taskId) {
        try {
            const response = await fetch(`/api/status/${taskId}`);
            const result = await response.json();
            
            if (result.status === 'completed') {
                processingStatus.classList.add('hidden');
                // 显示生成结果
                displayResults(result.images);
            } else if (result.status === 'processing') {
                // 继续轮询
                setTimeout(() => pollGenerationStatus(taskId), 2000);
            }
        } catch (error) {
            console.error('状态检查失败:', error);
        }
    }
}); 