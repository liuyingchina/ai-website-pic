import requests
from app import app
import os
import uuid
import base64

def generate_portrait(image_path, style):
    """调用阿里云API生成写真"""
    try:
        headers = {
            'Authorization': f'Bearer {app.config["DASHSCOPE_API_KEY"]}',
            'X-DashScope-Async': 'enable',
            'Content-Type': 'application/json'
        }
        
        api_style = app.config['STYLE_MAPPING'].get(style)
        if not api_style:
            app.logger.error(f"无效的风格类型: {style}")
            raise ValueError('不支持的风格类型')
        
        # 读取图片文件
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        # 构建请求数据
        data = {
            "model": "facechain-generation",
            "parameters": {
                "style": api_style,
                "size": "768*1024",
                "n": 4
            },
            "resources": [
                {
                    "resource_id": str(uuid.uuid4()),
                    "resource_type": "facelora",
                    "content": base64.b64encode(image_data).decode('utf-8')
                }
            ]
        }
        
        app.logger.info(f"开始调用阿里云API，风格: {api_style}, 图片路径: {image_path}")
        
        response = requests.post(
            app.config['DASHSCOPE_API_URL'],
            headers=headers,
            json=data
        )
        
        # 记录响应状态码
        app.logger.info(f"阿里云API响应状态码: {response.status_code}")
        
        response.raise_for_status()
        result = response.json()
        
        # 记录详细的响应结果
        app.logger.info(f"阿里云API调用成功，响应结果: {result}")
        
        return result
        
    except requests.exceptions.RequestException as e:
        app.logger.error(f"阿里云API调用失败: {str(e)}")
        if hasattr(e.response, 'json'):
            app.logger.error(f"错误详情: {e.response.json()}")
        raise
    except Exception as e:
        app.logger.error(f"生成写真过程中发生错误: {str(e)}")
        raise