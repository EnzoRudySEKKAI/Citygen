class InputBox:

    def __init__(self, pygame, name, description_text, x, y):

        self.pygame = pygame

        self.name = name
        self.description_text = description_text  # Text to show before the input box

        self.x = x
        self.y = y

        self.input_rect = pygame.Rect(x, y, 100, 50)  # Input rectangle
        self.input_rect.center = (x, y)

        self.text = ''

        self.has_user_clicked = False

    def handle_event(self, event):

        if event.type == self.pygame.MOUSEBUTTONDOWN:
            self.has_user_clicked = self.input_rect.collidepoint(event.pos)
        if event.type == self.pygame.KEYDOWN:
            if self.has_user_clicked:
                if event.key == self.pygame.K_RETURN:
                    self.text = ''
                elif event.key == self.pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, surface, font):

        input_text = font.render(self.description_text, True, (0, 70, 66))
        # Description text should be before the input box so we do (-45)
        input_text_rect = input_text.get_rect(center=(self.x, self.y - 45))
        surface.blit(input_text, input_text_rect)

        self.pygame.draw.rect(surface, (238, 238, 238), self.input_rect, 4)

        input_text_surface = font.render(self.text, True, "Black")
        surface.blit(input_text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
