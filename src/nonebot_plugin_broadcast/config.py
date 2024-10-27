# config.py
import logging
from pydantic_settings import BaseSettings
from typing import List

# 初始化 logger
logger = logging.getLogger(__name__)

class Config(BaseSettings):
    broadcast_groups: str  # 对应 .env 文件中的 BROADCAST_GROUPS

    class Config:
        env_file = ".env.prod"  # 或 .env，取决于你的实际文件名
        env_file_encoding = "utf-8"
        extra = "allow"

    @property
    def parsed_broadcast_groups(self) -> List[int]:
        """将字符串解析为整数列表"""
        if self.broadcast_groups:
            try:
                return [int(group_id.strip()) for group_id in self.broadcast_groups.split(',')]
            except ValueError as e:
                logger.error(f"广播群组配置错误：{e}，请检查 .env 文件中的 BROADCAST_GROUPS 配置")
                return []
        return []

# 创建 Config 实例，使其只在模块导入时运行一次
config = Config()