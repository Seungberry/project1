import pymysql
from datetime import datetime

class LegalDB:
    def __init__(self):
        # 建议使用连接池优化性能
        self.config = {
            "host": "127.0.0.1",
            "user": "root",
            "password": "root123",
            "database": "legal_bot_db",
            "charset": "utf8mb4"
        }

    def save_chat_log(self, user_id, category, role, content):
        """存储对话日志"""
        conn = pymysql.connect(**self.config)
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO chat_logs (user_id, category, role, content) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (user_id, category, role, content))
            conn.commit()
        finally:
            conn.close()

    def get_history(self, user_id, category, limit=10):
        """获取最近的历史记录用于上下文"""
        conn = pymysql.connect(**self.config)
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = "SELECT role, content FROM chat_logs WHERE user_id=%s AND category=%s ORDER BY created_at DESC LIMIT %s"
                cursor.execute(sql, (user_id, category, limit))
                return cursor.fetchall()[::-1] # 恢复正序
        finally:
            conn.close()