import pygame

# from pokequiz.constants import WHITE, BLACK
from pokequiz.constants import BLACK, WHITE

COLOR_INACTIVE = pygame.Color("lightskyblue3")
COLOR_ACTIVE = pygame.Color("dodgerblue2")


class Button:
    # Modified from https://stackoverflow.com/questions/63762922/whats-the-most-convenient-way-to-add-buttons-in-pygame-with-text
    def __init__(self, size, text, pos, bgColor=WHITE, textColor=BLACK, center_text=False, selected=False):
        self.pos = pos
        self.size = size
        self.text = text
        self.center_text = center_text
        self.selected = selected
        self.bgColor = bgColor if self.selected else textColor
        self.textColor = textColor if self.selected else bgColor
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.size[1])

    def render(self, window):
        self.textSurf = self.font.render(f"{self.text}", True, self.textColor)
        self.button = pygame.Surface((self.size[0], self.size[1])).convert()
        self.button.fill(self.bgColor)

        window.blit(self.button, (self.pos[0], self.pos[1]))
        if self.center_text:
            text_width, _ = self.textSurf.get_size()
            text_position = (self.pos[0] + (self.size[0] - text_width) // 2, self.pos[1] + 2)
        else:
            text_position = (self.pos[0] + 1, self.pos[1] + 5)
        window.blit(self.textSurf, text_position)

    def clicked(self, events):
        mousePos = pygame.mouse.get_pos()  #  get the mouse position
        for event in events:
            if self.button.get_rect(topleft=self.pos).collidepoint(mousePos[0], mousePos[1]):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True
        return False

    def flip(self):
        self.bgColor, self.textColor = self.textColor, self.bgColor
        self.selected = not self.selected

    def deselect(self):
        if self.selected:
            self.flip()

    def is_selected(self):
        return self.selected


class ButtonImage:
    def __init__(self, size, text, image, pos, selected=False, border_width=5):
        self.border_width = border_width
        self.border_pos = pos
        self.border_size = size
        self.pos = (pos[0] + self.border_width, pos[1] + self.border_width)
        self.size = (size[0] - 2 * self.border_width, size[1] - 2 * self.border_width)
        self.text = text
        self.selected = selected

        self.button = pygame.image.load(image)
        self.button = pygame.transform.scale(self.button, self.size)

    def render(self, window):
        window.blit(self.button, self.pos)
        if self.selected:
            pygame.draw.rect(
                window,
                COLOR_ACTIVE,
                (self.border_pos[0], self.border_pos[1], self.border_size[0], self.border_size[1]),
                self.border_width,
            )

    def clicked(self, events):
        mousePos = pygame.mouse.get_pos()  #  get the mouse position
        for event in events:
            if self.button.get_rect(topleft=self.pos).collidepoint(mousePos[0], mousePos[1]):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True
        return False

    def flip(self):
        self.selected = not self.selected

    def deselect(self):
        if self.selected:
            self.flip()

    def is_selected(self):
        return self.selected


class InputBox:
    # Modified from https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame
    def __init__(self, x, y, w, h, initial_value="", auto_active=False, always_active=False):
        self.minimum_width = w
        self.rect = pygame.Rect(x, y, self.minimum_width, h)
        self.active = auto_active or always_active
        self.always_active = always_active
        self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        self.initial_value = initial_value
        self.reset()
        self.text_height = h - 5
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.text_height)
        self.update()
        # self.txt_surface = FONT.render(text, True, self.color)

    def reset(self):
        self.text = self.initial_value
        self.update()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if not self.always_active:
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    current_text = self.text
                    self.reset()
                    return current_text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.update()
        return None

    def update(self):
        self.txt_surface = self.font.render(self.text, True, self.color)
        # Resize the box if the text is too long.
        width = max(self.minimum_width, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def update_and_draw(self, WIN):
        self.update()
        self.draw(WIN)

    def get_value(self):
        return self.text


class InputBoxWithLabel(InputBox):
    def __init__(
        self, x, y, w, h, label="", initial_value="", auto_active=False, always_active=False, text_color=BLACK
    ):
        self.label = label
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.h)
        self.label_image = self.font.render(self.label, True, text_color)
        horizontal_buffer = 5
        input_box_x = self.x + self.label_image.get_width() + horizontal_buffer
        input_box_y = self.y
        super().__init__(
            input_box_x,
            input_box_y,
            w,
            h,
            initial_value=initial_value,
            auto_active=auto_active,
            always_active=always_active,
        )

    def draw(self, WIN):
        WIN.blit(self.label_image, (self.x, self.y))
        super().draw(WIN)


class InfoBox:
    def __init__(self, size, text, pos, bgColor=WHITE, textColor=BLACK, center_text=False):
        self.pos = pos
        self.size = size
        self.text = text
        self.center_text = center_text
        self.bgColor = bgColor
        self.textColor = textColor
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.size[1])

    def render(self, window):
        self.textSurf = self.font.render(f"{self.text}", True, self.textColor)
        self.button = pygame.Surface((self.size[0], self.size[1])).convert()
        self.button.fill(self.bgColor)

        window.blit(self.button, (self.pos[0], self.pos[1]))
        if self.center_text:
            text_width, _ = self.textSurf.get_size()
            text_position = (self.pos[0] + (self.size[0] - text_width) // 2, self.pos[1] + 2)
        else:
            text_position = (self.pos[0] + 1, self.pos[1] + 5)
        window.blit(self.textSurf, text_position)
