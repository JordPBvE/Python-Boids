from enum import Enum


# Define different (mutually exclusive) modes for the app:
class FrameModes(Enum):
    MODE_DEFAULT = 0
    MODE_FOLLOW_MOUSE = 1
    MODE_DEBUG = 2
    MODE_BUILD = 3
    MODE_BUILD_POLYGON = 4
