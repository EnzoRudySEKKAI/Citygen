class Button:

    def __init__(self, image, pos, text_input, font, second_pos=(0, 0)):

        # Button background image
        self.image = image

        # Button position on the surface
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.x_second_pos = second_pos[0]
        self.y_second_pos = second_pos[1]

        self.center = (self.x_second_pos + self.x_pos, self.y_second_pos + self.y_pos)
        # Text font
        self.font = font

        # Text color inside the button
        self.base_color = (0, 70, 66)
        self.hovering_color = "White"

        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        if self.image is None:
            self.image = self.text

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.rect_ = self.image.get_rect(center=self.center)  # Used to compare

        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.rendered = False

    def check_for_click(self, position):
        return position[0] in range(self.rect_.left, self.rect_.right) and position[1] in \
               range(self.rect_.top, self.rect_.bottom)

    def render(self, screen, position):

        if position[0] in range(self.rect_.left, self.rect_.right) and position[1] in \
                range(self.rect_.top, self.rect_.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

        if not self.rendered:
            if self.image is not None:
                screen.blit(self.image, self.rect)
            screen.blit(self.text, self.text_rect)
        self.rendered = True
