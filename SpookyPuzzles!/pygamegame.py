'''pygamegame.py
created by Lukas Peraza
 for 15-112 F15 Pygame Optional Lecture, 11/11/15
use this code in your term project if you want
- you might want to move the pygame.display.flip() to your redrawAll function,
    in case you don't need to update the entire display every frame (then you
    should use pygame.display.update(Rect) instead)
'''

import pygame


class PygameGame(object):

    def init(self):
        pass

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        pass

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=600, height=400, fps=12, title="Spooky Puzzles!"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()
        exit()


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()
"""Explanation
This framework treats the application you make as a class. You can run your app by creating an instance of said class, and running it. Each display window is then an instance of your pygameGame class.
Inside the class, we have the meat of our code. We see helper function that gives us a lot of functionality, which not only includes init, mousepressed, timerFired, keypressed and redrawall, but also things like mouseDrag and mouseReleased. Note that you want to write code in the init method to initialize elements in your game. We don't want to touch the __init__ to set up your game settings, which we can do by simply making an instance of the class.
The run method holds all the code has all the stuff we've talked about in previous sections, and that's what gives us all these functionalities.
The purpose of this framework is to give an easy way to code your game in a neat manner without having to worry about how it works behind the scene. With this framework, you shouldn't need to touch the run function at all. In fact, you can keep the framework in a separate file and use the class to build games, defining only the functions you need. For example:
import pygame
import pygamegame #the framework

class myProject(pygamegame.PygameGame):
    def init(self):
        self.message = "World Helo"
    def mousepressed(self, x, y):
        print(self.message)

#creating and running the game
game = myProject()
game.run()"""