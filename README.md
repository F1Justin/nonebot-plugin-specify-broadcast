<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="80" height="80" alt="NoneBotPluginLogo"></a>
  <img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText">
</div>

# nonebot-plugin-broadcast

✨ NoneBot 插件，用于广播消息到多个群组 ✨

[![license](https://img.shields.io/github/license/F1Justin/nonebot-plugin-broadcast.svg)](./LICENSE)
[![pypi](https://img.shields.io/pypi/v/nonebot-plugin-broadcast.svg)](https://pypi.python.org/pypi/nonebot-plugin-broadcast)
![python](https://img.shields.io/badge/python-3.9+-blue.svg)

## 📖 介绍

`nonebot-plugin-broadcast` 是一个用于 NoneBot 的插件，帮助你将消息广播到多个群组。该插件支持灵活的配置和自定义广播内容。

## 💿 安装

### 使用 nb-cli 安装

在 NoneBot2 项目的根目录下打开命令行，输入以下指令即可安装：

```bash
nb plugin install nonebot-plugin-broadcast
```

### 使用包管理器安装

在 NoneBot2 项目的插件目录下，打开命令行，根据你使用的包管理器，输入相应的安装命令：

#### pip

```bash
pip install nonebot-plugin-broadcast
```

安装后，打开 NoneBot2 项目根目录下的 `pyproject.toml` 文件，在 `[tool.nonebot]` 部分追加写入：

```toml
plugins = ["nonebot_plugin_broadcast"]
```

## ⚙️ 配置

在 NoneBot2 项目的 `.env.prod` 文件中添加下表中的必填配置：

| 配置项   | 必填 | 默认值 | 说明         |
|:--------:|:----:|:------:|:-------------|
| BROADCAST_GROUPS  | 是   | 无     | 格式：`BROADCAST_GROUPS=123456,114514,......`     |

## 🎉 使用

### 指令表

| 指令    | 权限 | 需要@ | 范围  | 说明         |
|:-------:|:----:|:-----:|:-----:|:-------------|
| **广播**   | 主人 | 否    | 群聊  | 开启广播流程     |

