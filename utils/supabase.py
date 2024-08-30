from supabase import create_client
import os
from dotenv import load_dotenv
class SupabaseClientSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if SupabaseClientSingleton._instance is None:
            # Supabase 项目 URL 和匿名用户公钥
            load_dotenv()
            SUPABASE_URL = os.getenv("SUPABASE_URL")
            SUPABASE_KEY = os.getenv("SUPABASE_KEY")
            # 创建 Supabase 客户端
            SupabaseClientSingleton._instance = create_client(SUPABASE_URL, SUPABASE_KEY)
        return SupabaseClientSingleton._instance
