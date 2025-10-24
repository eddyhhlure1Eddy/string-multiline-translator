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
git clone https://github.com/eddyhhlure1Eddy/string-multiline-translator.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Restart ComfyUI

## Quick Start

### 1. Basic Usage
- Add **"MMAudio Description Generator"** node
- Input your text description (Chinese/English)
- Enter your OpenRouter API key
- Get professional English audio descriptions

### 2. WanVideo Integration
- Connect **WanVideoTextEncode** → **WanVideo to MMAudio Bridge** → **MMAudio**
- Automatic text extraction and conversion
- Seamless workflow integration

### 3. Preview & Testing
- Use **"MMAudio Preview Generator"** for testing
- Real-time preview of different audio modes
- Perfect for workflow development

## API Configuration

Get your OpenRouter API key from: https://openrouter.ai/

Enter the API key directly in the node interface - no configuration files needed!

## Example Output

```
Input: "东方女性穿着旗袍走在中式楼梯上，地板发出高跟鞋的声音"
Output: "Elegant Chinese woman in qipao walking on traditional stairs, heels clicking softly on wooden floor"
```

## Node Types

### MMAudio Description Generator
- **Input**: Multiline text (Chinese/English)
- **Output**: Professional English audio description (5-15 words)
- **Modes**: Audio description, background music, ambient effects, voice dubbing, special effects

### WanVideo to MMAudio Bridge
- **Input**: WanVideoTextEncode embeddings
- **Output**: MMAudio-compatible audio descriptions
- **Purpose**: Seamless integration between WanVideo and MMAudio workflows

### MMAudio Preview Generator
- **Input**: Text for testing
- **Output**: Real-time preview of audio descriptions
- **Purpose**: Development and testing of audio descriptions

### Audio Description Combiner
- **Input**: Multiple audio elements
- **Output**: Combined audio description
- **Purpose**: Merge multiple audio sources

### Audio Description Replacer
- **Input**: Original text + replacement elements
- **Output**: Updated audio description
- **Purpose**: Modify existing audio descriptions

## Requirements

- ComfyUI
- OpenRouter API key (get from https://openrouter.ai/)
- requests library

## Workflow Integration

```
Text Input → MMAudio Description Generator → MMAudio Node → Audio Output
     ↓
WanVideoTextEncode → WanVideo to MMAudio Bridge → MMAudio Node → Audio Output
```

## Supported Audio Modes

- **音频描述** (Audio Description) - Complete scene description
- **背景音乐** (Background Music) - Musical elements focus
- **环境音效** (Ambient Effects) - Environmental sounds
- **人声配音** (Voice Dubbing) - Human voice elements
- **特殊音效** (Special Effects) - Unique sound effects
- **成人内容** (Adult Content) - Mature content descriptions

## Author

Created by eddy

## License

Apache License 2.0
