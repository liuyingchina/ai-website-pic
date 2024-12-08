import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# 创建日志目录（使用绝对路径）
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置日志文件
log_file = os.path.join(log_dir, 'app.log')
file_handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)

# 同时输出到控制台
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
console_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('应用启动')

from app import routes 