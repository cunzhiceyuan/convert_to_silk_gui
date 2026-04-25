
# 🎵 音频转 Silk 工具

一个带图形界面的音频格式转换工具，可将常见音频文件（MP3、WAV、FLAC、AAC、OGG、M4A、OPUS、WMA）转换为tx **Silk** 格式（`.silk`），适用于vx的、QQ 等场景。

![GUI界面预览](screenshots/gui.png)  <!-- 如果你有截图，可以放这里 -->

## ✨ 功能特点

- 支持批量添加文件或整个文件夹
- 图形界面，操作简单
- 自动跳过不支持的文件类型
- 转换过程实时显示日志
- 自动清理临时 PCM 文件
- 转换完成后可选择打包为独立 `.exe` 文件（无需 Python 环境）

## 📦 系统要求

- **Windows / macOS / Linux**（本工具基于 Python，跨平台）
- 已安装 **Python 3.8 或更高版本**
- 已安装 **FFmpeg**（用于音频解码）

## 🛠 安装与配置

### 1. 安装 Python 依赖

```bash
pip install pilk
```

> `tkinter` 和 `subprocess` 是 Python 标准库，无需额外安装。

### 2. 安装 FFmpeg

FFmpeg 用于将各种音频格式解码为 PCM。请根据你的操作系统安装：

- **Windows**：  
  下载 [ffmpeg-release-full.7z](https://www.gyan.dev/ffmpeg/builds/)，解压后将 `bin/ffmpeg.exe` 所在目录添加到系统 PATH，或者直接将该 `.exe` 放在与脚本相同的文件夹下。

- **macOS**（使用 Homebrew）：  
  ```bash
  brew install ffmpeg
  ```

- **Linux**（Ubuntu/Debian）：  
  ```bash
  sudo apt install ffmpeg
  ```

验证安装：在终端输入 `ffmpeg -version`，应显示版本信息。

## 🚀 运行程序

将下方代码保存为 `convert_to_silk_gui.py`，然后在终端中执行：

```bash
python convert_to_silk_gui.py
```

> 如果你还没下载代码，可以直接复制 [这里](convert_to_silk_gui.py) 的完整脚本。

## 🖱 图形界面使用说明

1. **添加音频文件**  
   - 点击「添加文件」选择一个或多个音频文件  
   - 点击「添加文件夹」自动导入文件夹内所有支持的音频（包括子文件夹）

2. **选择输出文件夹**  
   - 点击「浏览」选择转换后的 `.silk` 文件保存位置

3. **开始转换**  
   - 点击「开始转换」，程序将依次处理每个文件  
   - 转换日志会实时显示在下方文本框中  
   - 每个文件转换成功后会在输出文件夹生成同名的 `.silk` 文件

4. **清空列表**  
   - 点击「清空列表」移除所有已添加的文件

> ⚠️ 注意：转换过程中界面不会卡死，但请不要重复点击「开始转换」。

## 📦 打包为独立 EXE（可选）

如果你想得到一个无需安装 Python 就能运行的 `.exe` 文件，可以按以下步骤操作：

### 1. 安装 PyInstaller

```bash
pip install pyinstaller
```

### 2. 准备 FFmpeg 可执行文件

将 `ffmpeg.exe` 放在与脚本相同的目录下（**重要**：打包时会一起打包进去）。

### 3. 执行打包命令

```bash
pyinstaller --onefile --windowed --add-data "ffmpeg.exe;." --hidden-import pilk convert_to_silk_gui.py
```

打包完成后，在 `dist` 文件夹中找到 `convert_to_silk_gui.exe`，可以直接双击运行。

> 如果你想要更小的体积，可以尝试 `--upx-dir` 参数压缩，但不是必须。

## ❓ 常见问题

### Q1: 运行时报错 `No module named 'pilk'`
**A:** 请先执行 `pip install pilk`。

### Q2: 转换时提示 `未找到 ffmpeg`
**A:** 确保 FFmpeg 已正确安装并加入 PATH，或者将 `ffmpeg.exe` 放在与脚本相同的目录下。

### Q3: 转换出的 `.silk` 文件无法在vx的中播放？
**A:** vx的 Silk 格式有严格参数要求：单声道、24000 Hz 采样率、tx专用版本。本工具已默认使用这些参数，通常可正常播放。如果仍有问题，请检查源文件是否为有效音频。

### Q4: 程序运行时闪退？
**A:** 请尝试在命令行中运行，查看具体报错信息。常见原因是缺少依赖或 FFmpeg 未找到。

### Q5: 代码中的临时文件会残留吗？
**A:** 不会。每个文件转换完成后，自动删除生成的 `.pcm` 临时文件。但如果程序异常终止，临时文件可能残留于系统临时目录（可通过系统清理工具删除）。

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 🤝 贡献

欢迎提交 Issue 或 Pull Request。

