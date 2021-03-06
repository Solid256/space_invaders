import pygame.font


class Button:
    """The class for the button object."""
    def __init__(self, ai_settings, screen, position_y, text_color, msg):
        """Initialize button attributes."""
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.msg_image = None
        self.msg_image_rect = None
        self.ai_settings = ai_settings
        self.position_y = position_y

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (0, 0, 0)
        self.text_color = text_color
        self.font = pygame.font.Font("fonts/BPdotsPlusBold.otf", 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.centery = position_y

        # The button message needed to be prepped only once.
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.centerx = self.rect.centerx
        self.msg_image_rect.centery = self.position_y

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
