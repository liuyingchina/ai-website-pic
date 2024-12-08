import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    UPLOAD_FOLDER = os.path.join(basedir, 'app/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size 
    
    # 阿里云API配置
    DASHSCOPE_API_KEY = os.environ.get('DASHSCOPE_API_KEY', 'your-api-key-here')
    DASHSCOPE_API_URL = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/album/gen_potrait'
    
    # 写真风格映射
    STYLE_MAPPING = {
        # 证件照和商务系列
        'idcard_male': 'f_idcard_male',          # 证件照男
        'idcard_female': 'f_idcard_female',      # 证件照女
        'business_male': 'f_business_male',      # 商务写真男
        'business_female': 'f_business_female',  # 商务写真女
        
        # 四季主题系列
        'spring_garden': 'm_springflower_female',    # 春日花园
        'summer_sports': 'f_summersport_female',     # 夏日运动
        'autumn_impression': 'f_autumnleaf_female',  # 秋日印象
        'winter_chinese': 'm_winterchinese_female',  # 冬日国风
        
        # 特色风格系列
        'hongkong_retro': 'f_hongkongvintage_female',  # 港风复古
        'light_portrait': 'f_lightportray_female'      # 轻写真
    }