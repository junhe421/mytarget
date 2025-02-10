# 我的T - 目标管理悬浮窗 (MyTarget)

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.5-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![GitHub issues](https://img.shields.io/github/issues/junhe421/mytarget)](https://github.com/junhe421/mytarget/issues)
[![GitHub stars](https://img.shields.io/github/stars/junhe421/mytarget)](https://github.com/junhe421/mytarget/stargazers)

一个简洁优雅的目标管理悬浮窗应用，帮助你高效管理和追踪本周、本月、本年的目标。

[功能特点](#-功能特点) •
[系统要求](#-系统要求) •
[快速开始](#-快速开始) •
[使用指南](#-使用指南) •
[开发指南](#-开发指南) •
[更新日志](#-更新日志)

[📖 在线文档](https://github.com/junhe421/mytarget/wiki) •
[🐛 问题反馈](https://github.com/junhe421/mytarget/issues) •
[💬 讨论](https://github.com/junhe421/mytarget/discussions)

</div>

## ✨ 功能特点

- 🎯 可拖动的悬浮窗口，随时置顶显示
- 📅 按周/月/年分类管理目标
- 🎨 深色/浅色主题切换，自适应你的使用习惯
- 🌐 中英文界面切换
- 🔔 目标优先级管理（高🔴/中🟡/低🟢）
- 📊 直观的进度统计和进度条显示
- 💾 本地数据自动保存，无需手动操作
- 🎈 智能最小化（5秒无操作自动切换为横幅模式）
- ✨ 励志语录滚动显示，激发前进动力

## 💻 系统要求

• 操作系统
  - Windows 10/11 (64位)
  - 分辨率：1280x720 或更高

• 硬件要求
  - CPU：1.6GHz 或更快
  - 内存：2GB RAM
  - 硬盘空间：50MB 可用空间

• 软件环境
  - Python 3.8 或更高版本
  - pip（Python包管理器）
  - 网络连接（用于安装依赖）

## 🚀 快速开始

```bash
# 克隆项目
git clone https://github.com/junhe421/mytarget.git

# 进入项目目录
cd mytarget

# 安装依赖
pip install -r requirements.txt

# 运行程序
python main.py
# 或者直接运行
start.bat
```

## 🎮 使用指南

### 基本操作
- **添加目标**：
  1. 选择时间范围（本周/本月/本年）
  2. 选择优先级（🔴高/🟡中/🟢低）
  3. 在输入框输入目标内容
  4. 点击"添加"按钮

- **管理目标**：
  - ✅ 点击目标前的复选框标记完成状态
  - 📝 右键点击目标可以编辑或删除
  - 🔄 拖动目标可以调整顺序

- **窗口操作**：
  - 🖱️ 拖动顶部蓝色区域移动位置
  - 🌓 点击主题按钮切换深色/浅色主题
  - 🌐 点击语言按钮切换中英文界面

### 智能横幅模式
- 5秒无操作自动切换为横幅模式
- 显示待办事项数量和励志语录
- 双击横幅可恢复完整窗口
- 右键点击可编辑励志语录

## 💻 开发指南

### 项目结构
```
mytarget/
├── main.py              # 主程序
├── start.bat            # 启动脚本
├── requirements.txt     # 项目依赖
├── data/               # 数据文件
│   ├── goals.json     # 目标数据
│   ├── quotes.json    # 励志语录
│   └── settings.json  # 主题设置
├── assets/            # 资源文件
│   └── mytarget.ico  # 程序图标
└── docs/             # 文档
    ├── user_guide.txt  # 使用指南
    └── version_info.txt  # 版本信息
```

### 开发环境设置
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装开发依赖
pip install -r requirements.txt
```

### 代码规范
- 使用Python的PEP 8编码规范
- 使用类型注解增加代码可读性
- 保持良好的注释习惯
- 提交前运行测试用例

## 🔧 数据管理

### 数据存储位置
所有数据文件默认存储在程序所在目录：
- 目标数据：`goals.json`
- 励志语录：`quotes.json`
- 主题设置：`settings.json`

### 数据备份
建议定期备份以下文件：
- `goals.json`（包含所有目标数据）
- `quotes.json`（包含自定义励志语录）

## 👨‍💻 作者信息

- 作者：A先生
- QQ交流：3956582704
- GitHub：[@junhe421](https://github.com/junhe421)
- 邮箱：[junhe421@gmail.com](mailto:junhe421@gmail.com)

## ⚠️ 注意事项

1. 请确保程序对当前目录有写入权限
2. 建议定期备份数据文件
3. 如遇问题，请查看 `app.log` 日志文件
4. 使用过程中如有建议或遇到问题：
   - 提交 [Issue](https://github.com/junhe421/mytarget/issues)
   - 在 [Discussions](https://github.com/junhe421/mytarget/discussions) 中讨论
   - 通过 QQ 或邮件联系作者

## 🤝 贡献指南

欢迎贡献代码，提交问题和建议！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 📝 开源协议

本项目基于 [MIT 协议](LICENSE.txt) 开源，欢迎使用和贡献。

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

### 特别感谢
- 所有提交 Issue 和 PR 的贡献者
- 所有在 Discussions 中提供建议的用户
- 所有参与测试和反馈的用户

## 🌐 相关链接

- 项目主页：[https://github.com/junhe421/mytarget](https://github.com/junhe421/mytarget)
- 功能建议：[https://github.com/junhe421/mytarget/discussions](https://github.com/junhe421/mytarget/discussions)
- 开发文档：[https://github.com/junhe421/mytarget/wiki](https://github.com/junhe421/mytarget/wiki)
- [Python](https://python.org)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [PyInstaller](https://www.pyinstaller.org) 