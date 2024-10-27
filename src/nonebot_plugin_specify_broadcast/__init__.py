from nonebot.plugin import PluginMetadata
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="群聊广播插件",
    description="允许超级用户向多个群聊广播消息，支持文字、图片和@。",
    usage="""
    指令：
    1. 广播：发送广播消息到多个群聊。
    示例：
    **广播** <消息内容>
    """,
    type="application",
    homepage="https://github.com/F1Justin/nonebot-plugin-specify-broadcast",  # 请将此替换为实际的项目主页链接
    config=Config,
    supported_adapters={"~onebot.v11"},
)

import asyncio
from nonebot import on_command, require
from nonebot.adapters.onebot.v11 import Bot, Event, Message, GroupMessageEvent, MessageSegment
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg, Arg, ArgPlainText
from nonebot.typing import T_State
from nonebot.log import logger
from datetime import datetime, timedelta
from .config import Config

# 使用 require 确保插件先加载
require("nonebot_plugin_apscheduler")

# 在确保插件加载后再导入 scheduler
from nonebot_plugin_apscheduler import scheduler


# 读取配置的广播群聊
config = Config()

# 定义广播指令，只有超级用户（管理员）可以使用
broadcast = on_command("**广播**", permission=SUPERUSER, priority=5, block=True)

# 定义广播的状态
@broadcast.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State, arg: Message = CommandArg()):
    await broadcast.send("请发送需要广播的内容（文字或图片），15秒内无响应自动取消。")
    
    # 设置一个超时任务，15秒后自动取消
    run_date = datetime.now() + timedelta(seconds=15)
    state['cancel_task'] = scheduler.add_job(
        lambda: asyncio.create_task(broadcast.finish("操作超时，已取消广播。")),
        "date",
        run_date=run_date
    )

# 接收广播内容
@broadcast.got("content", prompt="请发送需要广播的内容：")
async def handle_content(bot: Bot, event: Event, state: T_State, content: Message = Arg()):
    # 检查广播消息格式，只允许文字和图片
    if not any(isinstance(segment, MessageSegment) for segment in content):
        await broadcast.finish("只支持文字和图片广播。")
    
    # 取消之前的超时任务
    cancel_task = state.get('cancel_task')
    if cancel_task:
        cancel_task.remove()

    # 保存广播内容
    state["broadcast_content"] = content

    # 设置新的超时任务，确认环节超时为 15 秒
    run_date = datetime.now() + timedelta(seconds=15)
    state['confirm_cancel_task'] = scheduler.add_job(
        lambda: asyncio.create_task(broadcast.finish("确认超时，已取消广播。")),
        "date",
        run_date=run_date
    )

    # 二次确认
    await broadcast.send("请确认是否广播此消息？回复“确认”继续，回复其他内容取消。")

# 确认广播
@broadcast.got("confirm", prompt="请确认是否广播此消息？")
async def handle_confirm(bot: Bot, event: Event, state: T_State, confirm: str = ArgPlainText()):
    # 取消确认环节的超时任务
    confirm_cancel_task = state.get('confirm_cancel_task')
    if confirm_cancel_task:
        confirm_cancel_task.remove()

    # 如果用户没有确认，则取消广播操作
    if confirm != "确认":
        await broadcast.finish("已取消广播操作。")

    # 获取广播内容
    broadcast_content = state["broadcast_content"]

    # 获取当前对话的群聊 ID（如果是群聊）
    current_group_id = None
    if isinstance(event, GroupMessageEvent):
        current_group_id = event.group_id

    # 控制并发数量，防止过快发送导致风控
    semaphore = asyncio.Semaphore(5)  # 限制并发数量为 5

    # 用于记录成功和失败的群聊
    success_results = []
    failure_results = []

    async def send_message(group_id):
        async with semaphore:
            if group_id == current_group_id:
                logger.info(f"跳过当前群聊 {group_id} 的广播")
                return f"群 {group_id}: 跳过（当前群聊）"

            try:
                # 发送消息
                await bot.send_group_msg(group_id=group_id, message=broadcast_content)
                return f"群 {group_id}: 发送成功"
            except Exception as e:
                logger.error(f"向群 {group_id} 发送消息失败: {e}")
                return f"群 {group_id}: 发送失败（{str(e)}）"

    # 并发发送消息
    tasks = [send_message(group_id) for group_id in config.parsed_broadcast_groups]
    results = await asyncio.gather(*tasks)

    # 将成功和失败的结果分开
    for result in results:
        if "发送成功" in result:
            success_results.append(result)
        elif "发送失败" in result:
            failure_results.append(result)

    # 发送合并后的结果给管理员
    success_message = f"广播成功的群聊：\n" + "\n".join(success_results) if success_results else "没有成功的广播。"
    failure_message = f"广播失败的群聊：\n" + "\n".join(failure_results) if failure_results else "没有失败的广播。"

    await broadcast.send(f"广播完成！\n\n{success_message}\n\n{failure_message}")

    await broadcast.finish()
