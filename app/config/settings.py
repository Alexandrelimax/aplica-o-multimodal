import os
from vertexai.preview.generative_models import HarmCategory, HarmBlockThreshold

PROG_LANGUAGES = ("html", "py", "java", "js", "ts", "cs", "c", "cpp", "go", "rb", "php", "kt", "rs", "scala", "pl", "dart", "swift", "clj", "erl", "m")

TXT_FILES = ['.md', '.txt']

MEDIA_SUPPORTED_TYPES = ["application/pdf", "image/jpeg", "image/png", "image/webp", "video/mp4", "video/mpeg","video/mov","video/avi","video/x-flv","video/mpg","video/webm", "video/wmv","video/3gpp" ]

GENERATION_CONFIG = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
}