from timeit import default_timer as timer
import pygame.freetype


class MessageDisplay:
    # Class for handling messages that should be shown to the user.
    def __init__(self):
        self.font_size = 24
        self.font_color = (255, 255, 255)
        self.font = pygame.freetype.SysFont("Arial", self.font_size)
        self.message_height = 0.5
        self.message = ""
        self.dispatch_start = timer()
        self.show = True

    # Slightly adjusted from the pygame documentation here:
    # https://www.pygame.org/docs/ref/freetype.html#pygame.freetype.Font.render_to
    def word_wrap(self, screen, text, font, color):
        font.origin = True
        words = text.split(" ")
        width, height = screen.get_size()
        width *= 0.8
        line_spacing = font.get_sized_height() + 2
        x, y = 0.2 * screen.get_width(), self.message_height * screen.get_height()
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

    # Set a message to be shown to the screen
    # (only for when a new message should be
    # presented to the user)
    def show_message(self, msg, time_sec=3):
        self.message = msg
        self.dispatch_start = timer() + time_sec
        self.show = True

    # Render a message to the screen
    # (should be called every frame)
    def render_message(self, screen):
        if self.show:
            # only wrap if text doesn't fit
            full_rect = self.font.get_rect(self.message)
            if full_rect.width > 0.8 * screen.get_width():
                self.word_wrap(screen, self.message, self.font, self.font_color)
            else:
                x, y = (
                    0.5 * screen.get_width() - 0.5 * full_rect.width,
                    self.message_height * screen.get_height(),
                )
                self.font.render_to(screen, (x, y), self.message, self.font_color)
            if self.dispatch_start - timer() < 0:
                self.show = False
