import os #Dosya düzenleme kütüphanesi
import pygame


os.environ['SDL_VIDEO_WINDOW_POS'] = "500,200"


TITLE = "Never Enough"
WIDTH = 500
HEIGHT = 650
FPS = 60

klasor = os.path.dirname(__file__)
resimKlasoru = os.path.join(klasor,"resimler")

fisek = pygame.image.load(os.path.join(resimKlasoru,"dene.png"))
platform = pygame.image.load(os.path.join(resimKlasoru,"platform.jpg"))

arka_plan = pygame.image.load(os.path.join(resimKlasoru,"arkaplan.png"))

ates = pygame.image.load(os.path.join(resimKlasoru,"ates.png"))
bomba = pygame.image.load(os.path.join(resimKlasoru,"bomba.png"))

