import logging
from typing import List
from pydantic_settings import BaseSettings

# 初始化 logger
logger = logging.getLogger(__name__)

class Config(BaseSettings):
    # 设置默认值为空字符串，这样在未配置时不会报错
    broadcast_groups: str = ""

    class Config:
        env_file = ".env.prod"
        env_file_encoding = "utf-8"
        extra = "allow"

    @property
    def parsed_broadcast_groups(self) -> List[int]:
        """
        将字符串解析为整数列表
        
        Returns:
            List[int]: 解析后的群组ID列表。如果解析失败或无配置，返回空列表。
        """
        if not self.broadcast_groups:
            logger.info("未配置广播群组，使用空列表作为默认值")
            return []

        try:
            # 过滤掉空字符串，并转换为整数
            group_ids = [
                int(group_id.strip())
                for group_id in self.broadcast_groups.split(',')
                if group_id.strip()
            ]
            
            # 去重
            group_ids = list(dict.fromkeys(group_ids))
            
            if group_ids:
                logger.info(f"成功加载广播群组配置：{group_ids}")
            else:
                logger.warning("广播群组配置为空")
            
            return group_ids
            
        except ValueError as e:
            logger.error(f"广播群组配置解析错误：{e}")
            logger.error(f"问题配置值: {self.broadcast_groups}")
            logger.error("请确保 BROADCAST_GROUPS 中只包含以逗号分隔的数字")
            return []

# 创建 Config 实例
config = Config()