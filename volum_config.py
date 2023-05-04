import pygame
pygame.mixer.init()  # Иницилизация звука

class Sound():
    def __init__(self, sound, volume):
        self.sound = pygame.mixer.Sound(sound)
        self.volume = volume
        self.sound.set_volume(self.volume)
    def mute(self):
        self.sound.set_volume(0)
    def unmute(self):
        self.sound.set_volume(self.volume)
    def play(self):
        self.sound.play(loops=0, maxtime=0, fade_ms=0) #Звук

sounds = list()

sounds.append(Sound("sounds\laser-blast-descend.ogg", 0.1)) #0
sounds.append(Sound('sounds\\boom.ogg', 1)) #1
sounds.append(Sound('sounds\Shield.ogg', 0.2)) #2
sounds.append(Sound('sounds\Shield_Destroyed.ogg', 1)) #3
sounds.append(Sound('sounds\Shield Activated.ogg', 0.6)) #4
sounds.append(Sound('sounds\Health_Bonus.ogg', 0.6)) #5
sounds.append(Sound('sounds\Rocket_Bonus.ogg', 0.6)) #6
sounds.append(Sound('sounds\Armor_damage.ogg', 0.3)) #7



