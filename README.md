# Polymarket Arbitrage Bot

## 项目简介

本项目是一个用于Polymarket平台的套利机器人，支持自动化市场查询、余额检测、自动交易等功能。通过配置API密钥和相关参数，机器人可自动执行套利策略，帮助用户在Polymarket市场中实现收益最大化。

## 主要功能
- 市场行情自动查询
- 账户余额自动检测
- 策略化自动交易
- API密钥安全管理
- 灵活的参数配置

## 环境准备
1. 克隆本仓库：
   ```bash
   git clone https://github.com/JLBcode-code/polymarket-arb.git
   cd polymarket-arb
   ```
2. 创建并激活Python虚拟环境（推荐Python 3.8+）：
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # PowerShell
   # 或
   .\venv\Scripts\activate.bat  # CMD
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
4. 配置环境变量：
   - 复制.env.example为.env，并填写实际API密钥等信息。
   ```bash
   copy .env.example .env  # Windows
   # 或手动复制
   ```

## 启动方式

```bash
python -m src.strategy_bot
```

或直接运行主策略文件：

```bash
python src/strategy_bot.py
```

## 注意事项
- 请勿将.env文件上传到公共仓库，保护好API密钥等敏感信息。
- 仅供学习和研究使用，风险自负。

---
如有问题欢迎提交Issue或PR。
