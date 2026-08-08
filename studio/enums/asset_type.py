from enum import Enum


class AssetType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    FONT = "font"
    TEMPLATE = "template"
    OTHER = "other"
