"""
String Multiline Translator Nodes
Author: eddy
"""

import logging
import time
import json
import requests
from typing import Tuple, Optional

try:
    from .config import TRANSLATOR_CONFIG, USER_AGENT, PROXY_CONFIG, OPENROUTER_CONFIG, SYSTEM_PROMPT
except ImportError:
    from config import TRANSLATOR_CONFIG, USER_AGENT, PROXY_CONFIG, OPENROUTER_CONFIG, SYSTEM_PROMPT

TRANSLATOR_AVAILABLE = True

def call_openrouter_api(text: str, api_key: str, mode: str = "audio_description") -> Tuple[str, str]:
    """
    Call OpenRouter API to generate audio descriptions
    """
    if not api_key or not api_key.strip():
        return "Error: API key is required", mode

    try:
        headers = {
            "Authorization": f"Bearer {api_key.strip()}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://comfyui.local",
            "X-Title": "ComfyUI MMAudio Description Generator"
        }

        # Use user input directly as audio description request
        user_prompt = text

        data = {
            "model": OPENROUTER_CONFIG["model"],
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "max_tokens": OPENROUTER_CONFIG["max_tokens"],
            "temperature": OPENROUTER_CONFIG["temperature"]
        }

        response = requests.post(
            f"{OPENROUTER_CONFIG['base_url']}/chat/completions",
            headers=headers,
            json=data,
            timeout=OPENROUTER_CONFIG["timeout"]
        )

        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                audio_description = result["choices"][0]["message"]["content"].strip()
                return audio_description, "MMAudio"
            else:
                return f"API Response Error: No choices in response", mode
        elif response.status_code == 401:
            return f"Authentication Error: Invalid API key", mode
        elif response.status_code == 429:
            return f"Rate limit exceeded. Please try again later.", mode
        else:
            logging.error(f"OpenRouter API error: {response.status_code} - {response.text}")
            return f"API Error {response.status_code}: {response.text}", mode

    except requests.exceptions.Timeout:
        return f"Request timeout after {OPENROUTER_CONFIG['timeout']} seconds", mode
    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}", mode
    except Exception as e:
        logging.error(f"OpenRouter API call failed: {e}")
        return f"Unexpected error: {str(e)}", mode

# Audio description mode mapping
AUDIO_MODES = {
    "音频描述": "audio_description",
    "背景音乐": "background_music",
    "环境音效": "ambient_sound",
    "人声配音": "voice_narration",
    "特殊音效": "special_effects",
    "成人内容": "adult_content"
}

class StringMultiline:
    """Basic multiline string node"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "default": "", 
                    "multiline": True,
                    "dynamicPrompts": False
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "execute"
    CATEGORY = "文本处理/String Processing"
    DESCRIPTION = "Multiline string input node / 多行字符串输入节点"
    
    def execute(self, text: str) -> Tuple[str]:
        return (text,)

class StringMultilineTranslator:
    """MMAudio audio description generation node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "dynamicPrompts": False,
                    "tooltip": "Input audio content description / 输入音频内容描述，如：钢琴音乐、下雨声、女性说话等"
                }),
                "openrouter_api_key": ("STRING", {
                    "default": "",
                    "tooltip": "OpenRouter API Key (sk-or-v1-...) / OpenRouter API密钥"
                }),
                "audio_mode": (list(AUDIO_MODES.keys()), {
                    "default": "音频描述"
                }),
                "enable_generation": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Enable audio description generation / 启用音频描述生成"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("original_text", "audio_description", "mode")
    FUNCTION = "execute"
    CATEGORY = "音频处理/Audio Processing"
    DESCRIPTION = "MMAudio audio description generator / MMAudio专用音频描述生成节点，支持背景音乐、环境音效、人声配音等"
    
    def __init__(self):
        self.last_request_time = 0
    
    def execute(self, text: str, openrouter_api_key: str, audio_mode: str, enable_generation: bool) -> Tuple[str, str, str]:
        original_text = text
        audio_description = text
        mode = audio_mode

        if enable_generation and text.strip():
            try:
                # Check API key
                if not openrouter_api_key or not openrouter_api_key.strip():
                    audio_description = "Error: OpenRouter API key is required"
                    return (original_text, audio_description, mode)

                # Check text length
                if len(text) > TRANSLATOR_CONFIG["max_text_length"]:
                    audio_description = f"Text too long, exceeds {TRANSLATOR_CONFIG['max_text_length']} character limit"
                    return (original_text, audio_description, mode)

                # Control request frequency
                current_time = time.time()
                time_since_last = current_time - self.last_request_time
                if time_since_last < TRANSLATOR_CONFIG["request_interval"]:
                    time.sleep(TRANSLATOR_CONFIG["request_interval"] - time_since_last)

                # Generate audio description
                audio_description, detected_mode = call_openrouter_api(text, openrouter_api_key, "audio_description")
                self.last_request_time = time.time()

                logging.info(f"Audio description generated for mode: {audio_mode}")

            except Exception as e:
                logging.error(f"Audio description generation failed: {e}")
                audio_description = f"Generation failed: {str(e)}"

        elif enable_generation and not text.strip():
            audio_description = "Please input text content for audio description generation"

        return (original_text, audio_description, mode)
    


class StringConcatenateTranslator:
    """Audio description combiner node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string_a": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "First audio element description / 第一个音频元素描述"
                }),
                "string_b": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Second audio element description / 第二个音频元素描述"
                }),
                "openrouter_api_key": ("STRING", {
                    "default": "",
                    "tooltip": "OpenRouter API Key (sk-or-v1-...) / OpenRouter API密钥"
                }),
                "delimiter": ("STRING", {
                    "default": " with ",
                    "multiline": False,
                    "tooltip": "Delimiter (with, and, plus, etc.) / 连接符，如：with, and, plus等"
                }),
                "generate_description": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Generate audio description for combined content / 是否为连接后的内容生成音频描述"
                }),
                "audio_mode": (list(AUDIO_MODES.keys()), {
                    "default": "音频描述"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("concatenated_text", "audio_description")
    FUNCTION = "execute"
    CATEGORY = "音频处理/Audio Processing"
    DESCRIPTION = "Combine multiple audio element descriptions / 连接多个音频元素描述，生成组合音频描述"
    
    def __init__(self):
        pass
    
    def execute(self, string_a: str, string_b: str, openrouter_api_key: str, delimiter: str, generate_description: bool, audio_mode: str) -> Tuple[str, str]:
        # Concatenate strings
        concatenated = delimiter.join([string_a, string_b])
        audio_description = concatenated

        # Generate audio description if enabled
        if generate_description and concatenated.strip():
            try:
                if not openrouter_api_key or not openrouter_api_key.strip():
                    audio_description = "Error: OpenRouter API key is required"
                else:
                    audio_description, _ = call_openrouter_api(concatenated, openrouter_api_key, "audio_description")
            except Exception as e:
                logging.error(f"Audio description generation failed: {e}")
                audio_description = f"Generation failed: {str(e)}"
        elif generate_description and not concatenated.strip():
            audio_description = "Please input text content for audio description generation"

        return (concatenated, audio_description)

class StringReplaceTranslator:
    """Audio description replacer node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Original audio description text / 原始音频描述文本"
                }),
                "find": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "Audio element to replace / 要替换的音频元素"
                }),
                "replace": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "Replacement audio element / 替换为的音频元素"
                }),
                "openrouter_api_key": ("STRING", {
                    "default": "",
                    "tooltip": "OpenRouter API Key (sk-or-v1-...) / OpenRouter API密钥"
                }),
                "generate_description": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Generate audio description for replaced content / 是否为替换后的内容生成音频描述"
                }),
                "audio_mode": (list(AUDIO_MODES.keys()), {
                    "default": "音频描述"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("replaced_text", "audio_description")
    FUNCTION = "execute"
    CATEGORY = "音频处理/Audio Processing"
    DESCRIPTION = "Replace elements in audio descriptions / 替换音频描述中的元素，生成新的音频描述"
    
    def __init__(self):
        pass
    
    def execute(self, text: str, find: str, replace: str, openrouter_api_key: str, generate_description: bool, audio_mode: str) -> Tuple[str, str]:
        # Execute replacement
        replaced_text = text.replace(find, replace)
        audio_description = replaced_text

        # Generate audio description if enabled
        if generate_description and replaced_text.strip():
            try:
                if not openrouter_api_key or not openrouter_api_key.strip():
                    audio_description = "Error: OpenRouter API key is required"
                else:
                    audio_description, _ = call_openrouter_api(replaced_text, openrouter_api_key, "audio_description")
            except Exception as e:
                logging.error(f"Audio description generation failed: {e}")
                audio_description = f"Generation failed: {str(e)}"
        elif generate_description and not replaced_text.strip():
            audio_description = "Please input text content for audio description generation"

        return (replaced_text, audio_description)

# Node mapping
class WanVideoToMMAudioBridge:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "wan_text_embeds": ("WANVIDEOTEXTEMBEDS", {"tooltip": "Text embeddings from WanVideoTextEncode / WanVideoTextEncode的文本嵌入"}),
                "openrouter_api_key": ("STRING", {
                    "default": "",
                    "tooltip": "OpenRouter API Key (sk-or-v1-...) / OpenRouter API密钥"
                }),
                "audio_mode": (list(AUDIO_MODES.keys()), {"default": "音频描述"}),
                "enable_generation": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("original_text", "audio_description", "mode")
    FUNCTION = "bridge_to_mmaudio"
    CATEGORY = "音频处理/Audio Processing"
    DESCRIPTION = "Bridge WanVideoTextEncode output to MMAudio format / 将WanVideoTextEncode输出桥接到MMAudio格式"

    def bridge_to_mmaudio(self, wan_text_embeds, openrouter_api_key, audio_mode="音频描述", enable_generation=True):
        try:
            original_text = ""

            # Extract actual text content from WanVideo embeddings
            if isinstance(wan_text_embeds, dict):
                # Try to extract text from various possible fields
                if "text" in wan_text_embeds:
                    original_text = str(wan_text_embeds["text"])
                elif "prompt" in wan_text_embeds:
                    original_text = str(wan_text_embeds["prompt"])
                elif "positive_prompt" in wan_text_embeds:
                    original_text = str(wan_text_embeds["positive_prompt"])
                elif "prompt_embeds" in wan_text_embeds:
                    # If only embeddings available, use a generic description
                    original_text = "Video scene with visual elements requiring audio description"
                elif "positive_prompt_embeds" in wan_text_embeds:
                    original_text = "Positive video scene requiring audio enhancement"
                else:
                    # Fallback: try to extract any string values from the dict
                    text_values = []
                    for key, value in wan_text_embeds.items():
                        if isinstance(value, str) and len(value.strip()) > 0:
                            text_values.append(value.strip())
                    if text_values:
                        original_text = " ".join(text_values[:3])  # Use first 3 text values
                    else:
                        original_text = "WanVideo content requiring audio description"
            elif isinstance(wan_text_embeds, str):
                original_text = wan_text_embeds
            else:
                original_text = str(wan_text_embeds)

            # Clean up the text
            original_text = original_text.strip()
            if not original_text:
                original_text = "Video content requiring audio description"

            if not enable_generation:
                return (original_text, original_text, audio_mode)

            if not openrouter_api_key or not openrouter_api_key.strip():
                return (original_text, "Error: OpenRouter API key is required", audio_mode)

            mode_key = AUDIO_MODES.get(audio_mode, "audio_description")

            try:
                audio_description, detected_mode = call_openrouter_api(original_text, openrouter_api_key, mode_key)
                return (original_text, audio_description, detected_mode)
            except Exception as api_error:
                print(f"API call failed: {api_error}")
                return (original_text, f"API Error: {str(api_error)}", audio_mode)

        except Exception as e:
            error_msg = f"Bridge Error: {str(e)}"
            print(error_msg)
            return ("Error", error_msg, audio_mode)

class MMAudioPreviewGenerator:
    """MMAudio preview and testing node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Input text for MMAudio description preview / 输入文本进行MMAudio描述预览"
                }),
                "openrouter_api_key": ("STRING", {
                    "default": "",
                    "tooltip": "OpenRouter API Key (sk-or-v1-...) / OpenRouter API密钥"
                }),
                "audio_mode": (list(AUDIO_MODES.keys()), {
                    "default": "音频描述"
                }),
                "enable_generation": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Enable audio description generation / 启用音频描述生成"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("original_text", "audio_description", "mode")
    FUNCTION = "preview_generate"
    CATEGORY = "音频处理/Audio Processing"
    DESCRIPTION = "Preview and test MMAudio descriptions / 预览和测试MMAudio描述生成"

    def __init__(self):
        self.last_request_time = 0

    def preview_generate(self, text: str, openrouter_api_key: str, audio_mode: str, enable_generation: bool) -> tuple[str, str, str]:
        original_text = text.strip()
        audio_description = original_text
        mode = audio_mode

        if not original_text:
            return ("", "Please input text for preview / 请输入要预览的文本", mode)

        if enable_generation:
            try:
                # Check API key
                if not openrouter_api_key or not openrouter_api_key.strip():
                    audio_description = "Error: OpenRouter API key is required"
                    return (original_text, audio_description, mode)

                # Check text length
                if len(text) > TRANSLATOR_CONFIG["max_text_length"]:
                    audio_description = f"Text too long, exceeds {TRANSLATOR_CONFIG['max_text_length']} character limit"
                    return (original_text, audio_description, mode)

                # Control request frequency
                import time
                current_time = time.time()
                time_since_last = current_time - self.last_request_time
                if time_since_last < TRANSLATOR_CONFIG["request_interval"]:
                    time.sleep(TRANSLATOR_CONFIG["request_interval"] - time_since_last)

                # Generate audio description
                audio_description, detected_mode = call_openrouter_api(text, openrouter_api_key, "audio_description")
                self.last_request_time = time.time()

                logging.info(f"Preview audio description generated for mode: {audio_mode}")
                mode = detected_mode

            except Exception as e:
                logging.error(f"Preview audio description generation failed: {e}")
                audio_description = f"Generation failed: {str(e)}"

        return (original_text, audio_description, mode)

NODE_CLASS_MAPPINGS = {
    "StringMultiline": StringMultiline,
    "StringMultilineTranslator": StringMultilineTranslator,
    "StringConcatenateTranslator": StringConcatenateTranslator,
    "StringReplaceTranslator": StringReplaceTranslator,
    "WanVideoToMMAudioBridge": WanVideoToMMAudioBridge,
    "MMAudioPreviewGenerator": MMAudioPreviewGenerator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringMultiline": "String (Multiline)",
    "StringMultilineTranslator": "MMAudio Description Generator",
    "StringConcatenateTranslator": "Audio Description Combiner",
    "StringReplaceTranslator": "Audio Description Replacer",
    "WanVideoToMMAudioBridge": "WanVideo to MMAudio Bridge",
    "MMAudioPreviewGenerator": "MMAudio Preview Generator",
}
