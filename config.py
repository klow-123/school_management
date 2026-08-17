# config.py
import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',        # 你的MySQL用户名
    'password': '123456',  # 你的MySQL密码
    'database': 'school_management',
    'charset': 'utf8mb4'
}

def get_db_connection():
    """获取数据库连接"""
    return pymysql.connect(**DB_CONFIG)