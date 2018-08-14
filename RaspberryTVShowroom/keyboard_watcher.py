from Queue import Queue
import pygame


class KeyboardWatcher:
    def __init__(self):
        self.key_pressed = Queue()
        pygame.init()
        # sets the window title
        pygame.display.set_caption(u'Keyboard events')

        # sets the window size
        pygame.display.set_mode((400, 400))

    def start(self):
        while True:
            # gets a single event from the event queue
            event = pygame.event.wait()

            # if the 'close' button of the window is pressed
            if event.type == pygame.QUIT:
                # stops the application
                break

            # captures the 'KEYDOWN' and 'KEYUP' events
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                # finalizes Pygame
                break
        self.key_pressed.put(True)

    def stop(self):
        pygame.quit()

