# MMAudio Description Generator for ComfyUI

A ComfyUI custom node that converts text descriptions into professional English audio descriptions optimized for MMAudio video dubbing workflows.

## Features

🎵 **MMAudio Description Generator** - Convert any text to professional audio descriptions
🔗 **WanVideo Bridge** - Seamlessly connect WanVideoTextEncode to MMAudio
🎛️ **Preview Generator** - Test and preview text conversions in real-time
🌐 **Bilingual UI** - English/Chinese interface for global users
🎯 **Multiple Audio Modes** - Background music, ambient effects, voice dubbing, special effects

## Installation

1. Clone to your ComfyUI custom_nodes directory:
```bash
git clone https://github.com/your-repo/string-multiline-translator.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Restart ComfyUI

## 节点说明

### String (Multiline)
- 基础的多行字符串输入节点
- 输出：原始文本

### String (Multiline + Translator)
- 支持谷歌翻译的多行字符串节点
- 输入：
  - `text`: 多行文本输入
  - `source_language`: 源语言（支持自动检测）
  - `target_language`: 目标语言
  - `enable_translation`: 是否启用翻译
- 输出：
  - `original_text`: 原始文本
  - `translated_text`: 翻译后的文本
  - `detected_language`: 检测到的源语言

### String Concatenate (Translator)
- 字符串连接节点，支持翻译连接后的结果
- 输入：
  - `string_a`: 第一个字符串
  - `string_b`: 第二个字符串
  - `delimiter`: 分隔符（默认换行）
  - `translate_result`: 是否翻译结果
  - `target_language`: 目标语言
- 输出：
  - `concatenated_text`: 连接后的文本
  - `translated_text`: 翻译后的文本

### String Replace (Translator)
- 字符串替换节点，支持翻译替换后的结果
- 输入：
  - `text`: 原始文本
  - `find`: 要查找的字符串
  - `replace`: 替换的字符串
  - `translate_result`: 是否翻译结果
  - `target_language`: 目标语言
- 输出：
  - `replaced_text`: 替换后的文本
  - `translated_text`: 翻译后的文本

## 支持的语言

支持50+种语言，包括：
- 中文（简体/繁体）
- 英语、日语、韩语
- 法语、德语、西班牙语、俄语
- 意大利语、葡萄牙语、阿拉伯语
- 泰语、越南语、印地语等

## 注意事项

1. 翻译功能需要网络连接
2. 首次使用可能需要下载语言模型
3. 如果翻译失败，会返回错误信息
4. 建议在翻译大量文本时适当控制频率，避免被限制

## 作者

eddy

## 许可证

MIT License
