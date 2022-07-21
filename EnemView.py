import pygame
import json
from PIL import Image,ImageDraw
FPS = 30
WIDTH,HEIGHT = 800,600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
BLACK = (0,0,0)
FONT = "Humongous of Eternity St.ttf"

def draw_circle(Percent,screen,color,x,y,radius=20):
    None
    pil_size = radius
    pil_image = Image.new("RGBA", (pil_size, pil_size))
    pil_draw = ImageDraw.Draw(pil_image)
    Angle= 270+360*Percent
    pil_draw.pieslice((0, 0, pil_size - 1, pil_size - 1), 270, Angle, fill=color)
    # - convert into PyGame image -
    mode = pil_image.mode
    size = pil_image.size
    data = pil_image.tobytes()
    image = pygame.image.fromstring(data, size, mode)
    #image_rect = image.get_rect(center=screen.get_rect().center)
    screen.blit(image, (x,y) )  # <- display image

class EnemyView:
    def __init__(self,screen,parent):
        self.screen = screen
        self.parent = parent
        self.Data = self.loadEnemyData()['data']
        #print(self.Data)
        self.left = parent.left
        self.width = parent.get_size()[0]
        self.contentwidth = 0
        self.top = parent.top
        self.height = parent.get_size()[1]
        self.enemies = []
        #print(self.Data['Enemy'])  # ['name']
        for i in self.Data:#['Enemy']:
            #print(i)
            self.enemies.append(Enemy(self,i))
            self.contentwidth+=self.enemies[len(self.enemies)-1].width

    def loadEnemyData(self):
        with open("EnemyData.json", "r") as file2read:
            Data = json.load(file2read)
        return Data

    def calcEnemyWeaponData(self,damage,stagger,attackspeed,cleavelimit,armordamage,vsChaos,vsSkaven,vsInfantry,vsArmor,vsBerserk,vsMonster):
        for enemy in self.enemies:
            enemy.calc_stats(damage,stagger,attackspeed,cleavelimit,armordamage,vsChaos,vsSkaven,vsInfantry,vsArmor,vsBerserk,vsMonster)

    def draw(self):
        for i in range(len(self.enemies)):
            self.enemies[i].draw(i)

class Enemy:
    def __init__(self,parent,data):
        self.parent = parent
        self.data = data
        self.width = self.parent.width/7.0
        self.height = self.parent.height-20 #20 = Scrollbarheight
        if self.data['image'] != None:
            self.image = pygame.image.load("Images\\"+self.data['image']).convert()
        else:
            self.image = pygame.image.load("Images\\default.png").convert()
        self.image = pygame.transform.scale(self.image,(round(self.width),round(self.height)))
        self.name = self.data['name']
        self.hp = None
        self.mass = None

    def calc_stats(self,damage,stagger,attackspeed,cleavelimit,armordamage,vsChaos,vsSkaven,vsInfantry,vsArmor,vsBerserk,vsMonster):
        None
        #print(self.data)
        self.hp = self.data['hp'] #difficultylvl['values'][0]['hp']
        if self.data['type'] == "Armored" or self.data['type'] == "Super Armor" :
            damage *= (1+vsArmor/100)
            armordamage *= (1+vsArmor/100)
        if self.data['type'] == "Infantry":
            damage *= (1+vsInfantry/100)
            armordamage *= (1 + vsInfantry/100)
        if self.data['race'] == "Skaven":
            damage *= (1+vsSkaven/100)
            armordamage *= (1 + vsSkaven/100)
        if self.data['race'] == "Chaos":
            damage *= (1+vsChaos/100)
            armordamage *= (1 + vsChaos/100)
        if self.data['type'] == "Monsters":
            damage *= (1 + vsMonster / 100)
            armordamage *= (1 + vsMonster / 100)
        if self.data['type'] == "Berserkers":
            damage *= (1 + vsBerserk / 100)
            armordamage *= (1 + vsBerserk / 100)

        damage = round(damage * 4) / 4
        armordamage = round(armordamage * 4) / 4 #damage always get's rounded to 0.25 increment

        self.mass = self.data['hp']# difficultylvl['values'][0]['mass']
        self.normalhit = 1-(max((self.hp-damage),0)/self.hp)
        self.armorhit = 1-(max((self.hp-armordamage),0)/self.hp)
        self.stagger = 1 -(max((self.mass - stagger),0) / self.mass)
        #print(self.normalhit,self.hp,damage)
        # Hier kommen dann die Berechnungen hin wie groß die Balken auf den Charakteren werden

    def draw(self,enemynumber):
        font = pygame.font.Font(FONT, 10)
        label = font.render(self.name, 1, (255,255,255) )
        self.parent.screen.blit(self.image, (self.parent.parent.relativeleft+self.width*enemynumber,self.parent.top))  # -self.r/2
        self.parent.screen.blit(label, (round(self.parent.parent.relativeleft+self.width*enemynumber+self.width/20*2),round(self.parent.top+self.height/20*1)))
        if(self.hp != None):
            #NormalHit
            draw_circle((self.normalhit),self.parent.screen,(255,0,0),
                        self.parent.parent.relativeleft + self.width * enemynumber + self.width / 20 * 1,
                        self.parent.top + self.height/20*18,
                        round(self.width / 20 * 5/4*3))
            # ArmorHit
            draw_circle((self.armorhit),self.parent.screen,(0,255,0),
                        self.parent.parent.relativeleft + self.width * enemynumber + self.width / 20 * 5,
                        self.parent.top + self.height/20*18,
                        round(self.width / 20 * 5/4*3))
            # HP Headshot
            draw_circle((self.normalhit*1.5), self.parent.screen, (255, 100, 0),
                        self.parent.parent.relativeleft + self.width * enemynumber + self.width / 20 * 1,
                        self.parent.top + self.height / 20 * 16,
                        round(self.width / 20 * 5 / 4 * 3))
            # Armor Headshot
            draw_circle((self.armorhit*1.5), self.parent.screen, (0, 255, 150),
                        self.parent.parent.relativeleft + self.width * enemynumber + self.width / 20 * 5,
                        self.parent.top + self.height / 20 * 16,
                        round(self.width / 20 * 5 / 4 * 3))
            # Stagger
            draw_circle((self.stagger), self.parent.screen, (255, 255, 0),
                        self.parent.parent.relativeleft + self.width * enemynumber + self.width / 20 * 5,
                        self.parent.top + self.height / 20 * 14,
                        round(self.width / 20 * 5 / 4 * 3))