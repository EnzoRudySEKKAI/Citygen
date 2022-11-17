import os.path
import random
import sys

import pygame

from city import City
from display.button import Button
from display.input_box import InputBox
from populate.district import DISTRICTS_TYPE

# Load all assets
FULL_PATH = os.path.abspath(__file__ + "/../../")
ASSETS_FOLDER = os.path.join(FULL_PATH, "display", "assets")
BACKGROUND = pygame.image.load(os.path.join(ASSETS_FOLDER, "background.png"))
BUTTON_BG = pygame.image.load(os.path.join(ASSETS_FOLDER, "button_bg.png"))
BUTTON_BG2 = pygame.image.load(os.path.join(ASSETS_FOLDER, "button_bg2.png"))
FONT_PATH = os.path.join(ASSETS_FOLDER, "font.ttf")

# Setup pygame
pygame.init()
CLOCK = pygame.time.Clock()

# Surface where we show generation
SURF_WIDTH = 720
SURF_HEIGHT = 720
SURF = pygame.Surface((SURF_WIDTH, SURF_HEIGHT))
# Menu surface
MENU_SURF_WIDTH = SURF_WIDTH
MENU_SURF_HEIGHT = SURF_HEIGHT / 9
MENU_SURF = pygame.Surface((MENU_SURF_WIDTH, MENU_SURF_HEIGHT))
MENU_SURF.fill("White")
# Merge of the two surfaces
MAIN_SURF = pygame.display.set_mode((SURF_WIDTH, SURF_HEIGHT))
pygame.display.set_caption("Procedural City Generation")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 70, 66)

# City generation params
NB_BUILDINGS = 10000  # Set to 10000 by default
NB_DISTRICTS = 4  # Set to 4 by default
CITY_WIDTH = 800  # Set to 800 by default
CITY_HEIGHT = 800  # Set to 800 by default


def draw_city(buildings, axes, thickness):
    global MAIN_SURF
    MAIN_SURF = pygame.display.set_mode((SURF_WIDTH, SURF_HEIGHT + MENU_SURF_HEIGHT))

    # Fill background with white
    SURF.fill(WHITE)

    drawn_axes = drawn_buildings = False

    buttons = create_buttons("generation")
    save_button, zoom_in_button, zoom_out_button = buttons[0], buttons[1], buttons[2]

    while True:

        handle_events()

        mouse_pos = pygame.mouse.get_pos()

        # Render all buttons
        for button in [save_button, zoom_in_button, zoom_out_button]:
            button.render(MENU_SURF, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if save_button.check_for_click(mouse_pos) and drawn_buildings and drawn_axes:
                    save_image()
                if zoom_in_button.check_for_click(mouse_pos) and drawn_buildings and drawn_axes:
                    zoomed_screen = pygame.transform.scale(SURF, (SURF_WIDTH + 50, SURF_HEIGHT + 50))
                    SURF.fill("White")
                    SURF.blit(zoomed_screen, (0, 0))
                if zoom_out_button.check_for_click(mouse_pos) and drawn_buildings and drawn_axes:
                    zoomed_screen = pygame.transform.scale(SURF.convert_alpha(), (SURF_WIDTH - 50, SURF_HEIGHT - 50))
                    SURF.fill("White")
                    SURF.blit(zoomed_screen, (0, 0))

        # Update the surface again
        MAIN_SURF.blit(SURF, (0, 0))
        MAIN_SURF.blit(MENU_SURF, (0, SURF_HEIGHT))

        if drawn_axes and drawn_buildings:
            continue
        drawn_axes = draw_axes(axes, thickness)
        drawn_buildings = draw_buildings(buildings)

        print("City generation is done, press S to save the image or Q to leave.")


def draw_axes(axes, thickness):
    for axe in axes:
        MAIN_SURF.blit(MENU_SURF, (0, SURF_HEIGHT))
        MAIN_SURF.blit(SURF, (0, 0))

        handle_events()

        color = BLACK
        thickness_to_use = thickness + 2 if axe.is_major_axis else thickness

        pygame.draw.line(SURF, color, (axe.start_pos.x, axe.start_pos.y), (axe.end_pos.x, axe.end_pos.y),
                         width=thickness_to_use)
    return True


def draw_buildings(buildings):
    for building in buildings:
        MAIN_SURF.blit(MENU_SURF, (0, SURF_HEIGHT))
        MAIN_SURF.blit(SURF, (0, 0))
        handle_events()

        if building.bat_size > 0:
            polygon_coords = building.polygon.exterior.coords
            pygame.draw.polygon(SURF, building.type["Color"], list(polygon_coords[:-1]), 0)
    return True


def options():
    inputs_boxes = [
        InputBox(pygame, "nb_buildings", "Number of buildings", SURF_WIDTH / 2, 215),
        InputBox(pygame, "nb_districts", "Number of districts", SURF_WIDTH / 2, 335),
        InputBox(pygame, "city_width", "City width", SURF_WIDTH / 2, 455),
        InputBox(pygame, "city_height", "City height", SURF_WIDTH / 2, 575)
    ]

    while True:

        # Options setup
        mouse_pos = pygame.mouse.get_pos()
        SURF.blit(BACKGROUND, (0, 0))

        options_text = get_font(35).render("Please fill the fields below.", True, GREEN)
        options_rect = options_text.get_rect(center=(SURF_WIDTH / 2, 100))
        SURF.blit(options_text, options_rect)

        options_back = Button(image=None, pos=(SURF_WIDTH / 2, 640), text_input="BACK",
                              font=get_font(45))
        options_back.render(SURF, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if options_back.check_for_click(mouse_pos):
                    if process_user_inputs(inputs_boxes):
                        run_menu()

            for input_box in inputs_boxes:
                input_box.handle_event(event)

        for input_box in inputs_boxes:
            input_box.draw(SURF, get_font(30))

        MAIN_SURF.blit(SURF, (0, 0))
        MAIN_SURF.blit(MENU_SURF, (0, SURF_HEIGHT))

        pygame.display.update()


def run_menu():
    while True:

        SURF.blit(BACKGROUND, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(60).render("CITY GENERATOR", True, GREEN)
        menu_rect = menu_text.get_rect(center=(SURF_WIDTH / 2, 150))

        SURF.blit(menu_text, menu_rect)

        buttons = create_buttons("main")
        generate_button, options_button, quit_button = buttons[0], buttons[1], buttons[2]

        for button in [generate_button, options_button, quit_button]:
            button.render(SURF, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if generate_button.check_for_click(mouse_pos):
                    city = generate_city()
                    draw_city(city.get_buildings(), city.get_axes_list(), 1)
                if options_button.check_for_click(mouse_pos):
                    options()
                if quit_button.check_for_click(mouse_pos):
                    pygame.quit()
                    sys.exit()

        MAIN_SURF.blit(MENU_SURF, (0, SURF_HEIGHT))
        MAIN_SURF.blit(SURF, (0, 0))

        pygame.display.update()


def create_buttons(menu_type):
    if menu_type == "main":
        return [
            Button(image=BUTTON_BG, pos=(SURF_WIDTH / 2, 300),
                   text_input="GENERATE", font=get_font(40)
                   ),
            Button(image=BUTTON_BG, pos=(SURF_WIDTH / 2, 450),
                   text_input="OPTIONS", font=get_font(40)
                   ),
            Button(image=BUTTON_BG, pos=(SURF_WIDTH / 2, 600),
                   text_input="QUIT", font=get_font(40)
                   )
        ]
    if menu_type == "generation":
        return [
            Button(image=BUTTON_BG2,
                   pos=(MENU_SURF_WIDTH / 2 - 160, MENU_SURF_HEIGHT - 40),
                   text_input="SAVE", font=get_font(35),
                   second_pos=(0, SURF_HEIGHT)
                   ),
            Button(image=BUTTON_BG2,
                   pos=(MENU_SURF_WIDTH / 2, MENU_SURF_HEIGHT - 40),
                   text_input="Zoom-in", font=get_font(35),
                   second_pos=(0, SURF_HEIGHT)
                   ),
            Button(image=BUTTON_BG2,
                   pos=(MENU_SURF_WIDTH / 2 + 160, MENU_SURF_HEIGHT - 40),
                   text_input="Zoom-out", font=get_font(35),
                   second_pos=(0, SURF_HEIGHT)
                   )
        ]


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_s:
                save_image()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()


def generate_city():
    city = City(NB_DISTRICTS, CITY_WIDTH, CITY_HEIGHT, NB_BUILDINGS, DISTRICTS_TYPE)

    city.create_major_axes()

    for district in city.districts:
        city.create_district_axes(district)
        city.populate(district)
    city.generate_special_building(0.5)

    return city


def process_user_inputs(input_boxes):
    global NB_BUILDINGS, NB_DISTRICTS, CITY_WIDTH, CITY_HEIGHT
    global SURF_HEIGHT, SURF_WIDTH, SURF, MAIN_SURF

    for input_box in input_boxes:
        try:
            input_text = input_box.text
            if not input_text:
                continue
            if input_box.name == "nb_buildings":
                NB_BUILDINGS = int(input_text)
            if input_box.name == "nb_districts":
                NB_DISTRICTS = int(input_text)
            if input_box.name == "city_width":
                CITY_WIDTH = int(input_text)
            if input_box.name == "city_height":
                CITY_HEIGHT = int(input_text)
        except:
            print("Error in one of your inputs (int)")
            return False
    return True


def get_font(size):
    return pygame.font.Font(FONT_PATH, size)


def save_image():
    filename = input("Enter file name :")
    if not filename:
        filename = str(random.randint(1, 100))

    filename = f"{FULL_PATH}/generated_cities/{filename.strip()}.png"  # Remove white spaces
    pygame.image.save(SURF, filename)
    print("Image saved. Press Q to leave.")
