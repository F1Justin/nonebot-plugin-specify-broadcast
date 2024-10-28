import os
from typing import Set
from nonebot import get_driver, logger, config as nb_config # 导入 nonebot 的 Config

driver = get_driver()
config = driver.config

class Config(nb_config.Config):  # 继承自 nonebot.config.Config
    broadcast_groups: Set[int] = set()


    def __init__(self):
         # 需要调用父类构造函数
        super().__init__()


        broadcast_groups_str = os.environ.get("BROADCAST_GROUPS") or str(getattr(config, "broadcast_groups", ""))

        if broadcast_groups_str:
            try:
                self.broadcast_groups = set(map(int, broadcast_groups_str.split(',')))
                logger.info(f"成功加载广播群组配置：{self.broadcast_groups}")
            except ValueError:
                logger.error("广播群组配置解析错误，请确保 BROADCAST_GROUPS 中只包含以逗号分隔的数字")