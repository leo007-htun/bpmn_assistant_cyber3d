from enum import Enum


class OpenAIModels(Enum):
    GPT_4_1_MINI = "gpt-4.1-mini"
    GPT_4_1 = "gpt-4.1"
    O4_MINI = "o4-mini"
    GPT_4_1_NANO = "gpt-4.1-nano"


class AnthropicModels(Enum):
    SONNET_4 = "claude-sonnet-4-20250514"
    OPUS_4 = "claude-opus-4-20250514"


class GoogleModels(Enum):
    GEMINI_2_5_FLASH = "gemini/gemini-2.5-flash-preview-04-17"
    GEMINI_2_5_PRO = "gemini/gemini-2.5-pro-preview-03-25"


class FireworksAIModels(Enum):
    LLAMA_4_MAVERICK = (
        "fireworks_ai/accounts/fireworks/models/llama4-maverick-instruct-basic"
    )
    QWEN_3_235B = "fireworks_ai/accounts/fireworks/models/qwen3-235b-a22b"
    DEEPSEEK_V3 = "fireworks_ai/accounts/fireworks/models/deepseek-v3"
    DEEPSEEK_R1 = "fireworks_ai/accounts/fireworks/models/deepseek-r1"
