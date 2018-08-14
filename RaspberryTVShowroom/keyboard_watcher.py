from Queue import Queue
import pygame
from threading import Thread
from logging import getLogger


class KeyboardWatcher:
    def __init__(self):
        self._logger = getLogger("raspberry.videoplayer")
        self.key_pressed = Queue()
        self._thread = Thread()
        pygame.init()
        # sets the window title
        pygame.display.set_caption(u'Keyboard events')

        # sets the window size
        pygame.display.set_mode((400, 400))

    def start(self):

        self._thread = Thread(target=self._run)

    def _run(self):
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

