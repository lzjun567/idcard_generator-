# 身份证图片构造器 idcard_generator

> 【仅做研究使用，请遵守当地法律法规，法律后果自负】

身份证图片生成工具，填入信息，选择一张头像图片，即可生成黑白和彩色身份证图片。

支持自动抠图（纯色背景），也可以手动抠图后再上传。在线抠图工具：[burner.bonanza.com](https://burner.bonanza.com/) · [稿定抠图](https://www.gaoding.com/koutu)

---

## 网页版（推荐）

本项目已重构为网页版，无需安装桌面程序，直接在浏览器中操作。

### 快速启动

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动服务
python app.py

# 3. 浏览器访问
http://localhost:5000
```

### 功能特性

- **随机填充**：一键生成随机姓名、出生日期、身份证号等信息
- **拖拽上传**：支持拖拽或点击上传头像，实时本地预览
- **自动抠图**：自动去除纯色背景，无需手动处理
- **双版本输出**：同时生成彩色版和黑白版，支持一键下载
- **响应式设计**：支持手机、平板、桌面等各类设备

### 接口说明

| 方法 | 路由 | 说明 |
|------|------|------|
| GET | `/` | 主页面 |
| GET | `/api/random` | 随机生成一套证件信息（JSON） |
| POST | `/api/generate` | 提交表单+头像，返回 Base64 图片 |

---

## 桌面版（旧版）

原 Tkinter 桌面程序仍可正常使用。

### 直接下载可执行程序

- Windows 版：[idcard_generator_win64.exe](https://github.com/bzsome/idcard_generator/releases/download/v1.1.0/idcard_generator_win64_1.1.0.exe)
- macOS 版：[idcard_generator_macos.zip](https://github.com/bzsome/idcard_generator/releases/download/v1.1.0/idcard_generator_macos_1.1.0.zip)（启动约需 70s，支持 macOS 11）

### 源码运行

```bash
pip install idcard_generator -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
python main.py
```

### 打包桌面程序

```bash
# 安装 PyInstaller
pip install pyinstaller

# macOS 打包
pyinstaller main.spec

# Windows 打包
pyinstaller -i asserts/ico.ico --windowed --clean --noconfirm --onefile --add-data "asserts;asserts" main.py

# Windows 打包（保留控制台日志）
pyinstaller -i asserts/ico.ico -c --clean --noconfirm --onefile --add-data "asserts;asserts" main.py
```

---

## 运行效果图

**网页版主界面**

> 浏览器直接操作，无需安装

**桌面版主界面（Windows）**

<img src="./docs/images/example_01.png" width="50%" alt="程序运行图 Windows" />

**桌面版主界面（macOS）**

<img src="./docs/images/example_macos.png" width="50%" alt="程序运行图 macOS" />

**生成结果示例**

<img src="./docs/images/result_color.png" width="50%" alt="生成结果图" />

---

## 软件依赖

```
flask        # 网页版服务框架
numpy        # 图像数组处理
pillow       # 图像绘制与合成
opencv       # 自动抠图
```

---

## 更新记录

- **网页版重构**：基于 Flask 实现浏览器操作，无需安装桌面程序
- 自动改变头像大小
- 自动从纯色背景中抠图
- 随机生成身份信息（姓名、出生日期、身份证号）
- 固定依赖版本（防止高版本不兼容）
- 生成图片时显示处理弹窗

---

## 参照标准

**正面**：左上角为国徽，用红色油墨印刷；其右侧为证件名称"中华人民共和国居民身份证"，分上下两排排列，其中上排的"中华人民共和国"为 4 号宋体字，下排的"居民身份证"为 2 号宋体字；"签发机关"、"有效期限"为 6 号加粗黑体字；签发机关登记项采用"xx 市公安局"；有效期限采用"xxxx.xx-xxxx.xx.xx"格式，使用 5 号黑体字印刷，全部用黑色油墨印刷。

**背面**："姓名"、"性别"、"民族"、"出生年月日"、"住址"、"公民身份号码"为 6 号黑体字，用蓝色油墨印刷；登记项目中的姓名项用 5 号黑体字印刷；其他项目则用小 5 号黑体字印刷；出生年月日方正黑体简体字符大小：姓名＋号码（11 点）其他（9 点）字符间距（AV）：号码（50）字符行距：住址（12 点）；身份证号码字体 OCR-B 10 BT 文字华文细黑。
