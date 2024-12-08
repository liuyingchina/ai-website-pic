import os
from flask import render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from app import app
from app.utils import generate_portrait
import requests

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/studio')
def studio():
    return render_template('studio.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件上传'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # 这里后续添加AI处理逻辑
        
        return jsonify({
            'message': '上传成功',
            'filename': filename
        })
    
    return jsonify({'error': '不支持的文件类型'}), 400 

@app.route('/api/generate', methods=['POST'])
def generate_ai_portrait():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件上传'}), 400
    
    file = request.files['file']
    style = request.form.get('style')
    
    if not style or style not in app.config['STYLE_MAPPING']:
        return jsonify({'error': '无效的风格选择'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            app.logger.info(f"开始生成写真，风格: {style}")
            result = generate_portrait(filepath, style)
            
            return jsonify({
                'message': '生成成功',
                'task_id': result.get('task_id'),
                'status': 'processing',
                'images': result.get('images', [])  # 添加生成的图片URL
            })
            
        except Exception as e:
            app.logger.error(f"生成失败: {str(e)}")
            return jsonify({'error': str(e)}), 500
        
    return jsonify({'error': '不支持的文件类型'}), 400

@app.route('/api/status/<task_id>', methods=['GET'])
def check_generation_status(task_id):
    """检查生成任务状态"""
    try:
        app.logger.info(f"检查任务状态: {task_id}")
        
        # 这里实现检查阿里云API任务状态的逻辑
        # 假设这里调用阿里云的状态检查API
        response = requests.get(
            f"{app.config['DASHSCOPE_API_URL']}/tasks/{task_id}",
            headers={'Authorization': f'Bearer {app.config["DASHSCOPE_API_KEY"]}'}
        )
        
        app.logger.info(f"状态检查响应状态码: {response.status_code}")
        
        result = response.json()
        app.logger.info(f"任务状态检查结果: {result}")
        
        return jsonify({
            'status': result.get('status', 'processing'),
            'images': result.get('images', [])
        })
        
    except Exception as e:
        app.logger.error(f"检查任务状态失败: {str(e)}")
        return jsonify({'error': str(e)}), 500 