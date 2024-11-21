import pygame
from main import main 
from constants import *

def draw_button(window, text, x, y, width, height, is_hovered):
    """Draws a button with a transparent border and centered text."""
    border_color = (255, 255, 255) if not is_hovered else (200, 200, 200) 

    pygame.draw.rect(window, border_color, (x, y, width, height), width=3, border_radius=10)

    text_surface = FONT.render(text, True, (255, 255, 255))
    window.blit(
        text_surface,
        (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2),  
    )


def menu():
    """Displays the main menu with options for Freeplay, Adventure Mode, and Quit."""
    run = True
    clock = pygame.time.Clock()

    button_width, button_height = 500, 100
    button_gap = 40  
    total_height = (button_height * 3) + (button_gap * 2)  
    start_y = HEIGHT - total_height - 120 
    start_x = (WIDTH - button_width) // 2

    freeplay_y = start_y
    adventure_y = freeplay_y + button_height + button_gap
    quit_y = adventure_y + button_height + button_gap

    while run:
        try:
            WIN.blit(MENU_IMAGE, (0, 0))  

            mouse_x, mouse_y = pygame.mouse.get_pos()

            freeplay_hover = start_x <= mouse_x <= start_x + button_width and freeplay_y <= mouse_y <= freeplay_y + button_height
            adventure_hover = start_x <= mouse_x <= start_x + button_width and adventure_y <= mouse_y <= adventure_y + button_height
            quit_hover = start_x <= mouse_x <= start_x + button_width and quit_y <= mouse_y <= quit_y + button_height

            draw_button(WIN, "Freeplay", start_x, freeplay_y, button_width, button_height, freeplay_hover)
            draw_button(WIN, "Adventure Mode", start_x, adventure_y, button_width, button_height, adventure_hover)
            draw_button(WIN, "Quit", start_x, quit_y, button_width, button_height, quit_hover)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    if freeplay_hover:
                        result = main() 
                        if result == "quit":
                            run = False
                    elif adventure_hover:
                        print("Adventure mode coming soon!")  
                    elif quit_hover:
                        run = False

            pygame.display.update()
            clock.tick(60)

        except pygame.error:
            run = False

    pygame.quit()
    exit()  


if __name__ == "__main__":
    menu()
