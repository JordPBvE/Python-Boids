from timeit import default_timer as timer
import pygame.freetype


class MessageDisplay:
    # Class for handling messages that should be shown to the user.
    def __init__(self):
        self.font_size = 24
        self.font_color = (255, 255, 255)
        self.font = pygame.freetype.SysFont("Arial", self.font_size)
        self.message = "The boids say hi!"
        self.dispatch_start = timer()
        self.dispatch_time_seconds = 3
        self.show = True

    # Slightly adjusted from the pygame documentation here:
    # https://www.pygame.org/docs/ref/freetype.html#pygame.freetype.Font.render_to
    def word_wrap(self, surface, text, font, color):
        font.origin = True
        words = text.split(" ")
        width, height = surface.get_size()
        width *= 0.8
        line_spacing = font.get_sized_height() + 2
        x, y = 0.2 * surface.get_width(), 0.5 * surface.get_height()
        space = font.get_rect(" ")
        for word in words:
            bounds = font.get_rect(word)
            if x + bounds.width + bounds.x >= width:
                x, y = 0.2 * surface.get_width(), y + line_spacing
            if x + bounds.width + bounds.x >= width:
                raise ValueError("word too wide for the surface")
            if y + bounds.height - bounds.y >= height:
                raise ValueError("text to long for the surface")
            font.render_to(surface, (x, y), None, color)
            x += bounds.width + space.width

    # Set a message to be shown to the screen
    # (only for when a new message should be
    # presented to the user)
    def show_message(self, msg):
        self.message = msg
        self.dispatch_start = timer()
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
                    0.5 * screen.get_height(),
                )
                self.font.render_to(screen, (x, y), self.message, self.font_color)
            if timer() - self.dispatch_start > self.dispatch_time_seconds:
                self.show = False
