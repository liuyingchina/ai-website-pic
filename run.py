from app import app

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',  # 允许外部访问
        port=5000,       # 设置端口号
        debug=True       # 开启调试模式
    ) 