from timeit import default_timer as timer
import pygame.freetype


class MessageDisplay:
    """Helper class for handling messages that should be shown to the user.

    Class instance attributes:
    font: pygame.freetype.SysFont -- the font of the displayed messages
    font_size: int -- the font size (in pixels) of the displayed messages
    font_color: (int, int, int) -- the RGB color of the displayed messages
    msg_height: float -- factor between 0 and 1 that determines the height
    at which messages are displayed (where 0 is the top and 1 is the bottom)
    message
    message: str -- the message that should be displayed
    dispatch_start: default_timer -- a timer that keeps track of when a message
    started displaying
    show: bool -- whether the message should be displayed
    """

    def __init__(
        self,
        font=None,
        font_size=24,
        font_color=(255, 255, 255),
        msg_height=0.5,
    ):
        self.font_size = font_size
        self.font_color = font_color
        if font is None:
            self.font = pygame.freetype.SysFont("Arial", font_size)
        else:
            self.font = font
        self.msg_height = msg_height
        self.message = ""
        self.dispatch_start = timer()
        self.show = True

    def word_wrap(self, screen, text, font, color):
        """Render message to screen with word wrap.

        Slightly modified from the pygame documentation here
        pygame.org/docs/ref/freetype.html#pygame.freetype.Font.render_to
        """
        font.origin = True
        words = text.split(" ")
        width, height = screen.get_size()
        width *= 0.8
        line_spacing = font.get_sized_height() + 2
        x, y = 0.2 * screen.get_width(), self.msg_height * screen.get_height()
        line_words = ""
        for word in words:
            line_words += word + " "
            bounds = font.get_rect(line_words)
            if x + bounds.x + bounds.width >= width:
                rx = 0.5 * screen.get_width() - 0.5 * bounds.width
                font.render_to(screen, (rx, y), None, color)
                x, y = 0.2 * screen.get_width(), y + line_spacing
                line_words = ""
        rx = 0.5 * screen.get_width() - 0.5 * bounds.width
        font.render_to(screen, (rx, y), None, color)

    def show_message(self, msg, time_sec=3):
        """Set a message to be shown to the screen."""
        self.message = msg
        self.dispatch_start = timer() + time_sec
        self.show = True

    def render_message(self, screen):
        """Render a message to the screen (called every frame)"""
        if self.show:
            if self.dispatch_start - timer() < 0:
                self.show = False
            # only wrap if text doesn't fit neatly on the screen
            full_rectangle = self.font.get_rect(self.message)
            if full_rectangle.width > 0.8 * screen.get_width():
                self.word_wrap(screen, self.message,
                               self.font, self.font_color)
            else:
                x, y = (
                    0.5 * screen.get_width() - 0.5 * full_rectangle.width,
                    self.msg_height * screen.get_height(),
                )
                self.font.render_to(screen, (x, y),
                                    self.message, self.font_color)
