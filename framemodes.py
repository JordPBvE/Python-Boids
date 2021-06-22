from enum import Enum


class FrameModes(Enum):
    """Defines different (mutually exclusive) modes for the app."""

    MODE_DEFAULT = 0
    MODE_FOLLOW_MOUSE = 1
    MODE_DEBUG = 2
    MODE_BUILD = 3
    MODE_BUILD_POLYGON = 4
