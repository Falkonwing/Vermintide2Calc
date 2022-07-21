import pygame
import Widgets
import json
from EnemView import *

FPS = 30
WIDTH,HEIGHT = 800,600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
BLACK = (0,0,0)
FONT = "Humongous of Eternity St.ttf"

def loadHeroData():
    with open("HeroData.json", "r") as file2read:
        Data = json.load(file2read)
    return Data

class Weapon:
    def __init__(self,Weapondata):
        self.damage = Weapondata[0]['damage']
        self.stagger = Weapondata[0]['stagger']
        self.attackspeed = Weapondata[0]['speed']
        self.cleave = Weapondata[0]['cleave']
        self.armorDamage = Weapondata[0]['armordamage']
        self.ranged = Weapondata[0]['ranged']


    def loadWeaponData(self,Weapondata):
        self.damage = Weapondata[0]['damage']
        self.stagger = Weapondata[0]['stagger']
        self.attackspeed = Weapondata[0]['speed']
        self.cleave = Weapondata[0]['cleave']
        self.armorDamage = Weapondata[0]['armordamage']
        self.ranged = Weapondata[0]['ranged']

class scalingfactor:
    def __init__(self,Text,screen,left,top,min=0,max=99):
        self.value = 0.0
        self.text = Text
        self.screen = screen
        self.left = left
        self.top = top
        self.calc_values()
        self.min = min
        self.max = max

    def calc_values(self):
        self.font = pygame.font.Font(FONT, 10)
        [self.textwidth,self.textheight] = self.font.size(self.text) #[0]
        self.valuewidth = self.font.size("10000")[0] #1000 wird hier als maximalwert angegeben
        self.digitwidth = self.font.size("0")[0]
        self.buttonleft = self.left+self.textwidth+self.valuewidth
        self.buttonheight = round(self.textheight/2)
        self.buttonwidth = round(self.valuewidth/2)
        self.bar_up_image = pygame.image.load("images\\up.png").convert()
        self.bar_down_image = pygame.image.load("images\\down.png").convert()
        self.bar_up_image = pygame.transform.scale(self.bar_up_image, (round(self.buttonwidth), round(self.buttonheight)))
        self.bar_down_image = pygame.transform.scale(self.bar_down_image, (round(self.buttonwidth), round(self.buttonheight)))
        self.bar_upbutton_pos = (self.buttonleft,self.top)
        self.bar_downbutton_pos = (self.buttonleft, self.top+self.buttonheight)

    def update(self):
        mx, my = pygame.mouse.get_pos()
        #up button was pressed
        if self.buttonleft < mx and mx < self.buttonleft + self.buttonwidth and self.top < my and my < self.top + self.buttonheight and self.value < self.max:
            self.value += 1.0
        #down button was pressed
        if self.buttonleft < mx and mx < self.buttonleft + self.buttonwidth and self.top+ self.buttonheight < my and my < self.top + self.buttonheight+ self.buttonheight and self.value > self.min:
            self.value -= 1.0

    def draw(self):
        label = self.font.render(self.text, 1, (255, 255, 255))
        self.screen.blit(label, (round(self.left), round(self.top)))
        label = self.font.render(str(self.value), 1, (255, 255, 255))
        self.screen.blit(label, (round(self.left+self.textwidth+self.digitwidth), round(self.top)))
        self.screen.blit(self.bar_up_image, self.bar_upbutton_pos)
        self.screen.blit(self.bar_down_image, self.bar_downbutton_pos)



def draw_infos(screen):
    x = WIDTH/20*1
    y = HEIGHT/40*23
    #print("X/Y",x,y)
    font=pygame.font.Font(FONT, 10)

    draw_circle(1, screen, (255, 0, 0),
                round(x-15),
                round(y+5),
                10)
    #pygame.draw.line(screen, (255, 0, 0), (x,y),(x+100,y),5)
    label = font.render("unarmored spot hit", 1, (255, 255, 255))
    screen.blit(label, (round(x),round(y)))

    draw_circle(1, screen, (255, 100, 0),
                round(x-15),
                round(y-5),
                10)
    #pygame.draw.line(screen, (255, 0, 0), (x,y),(x+100,y),5)
    label = font.render("unarmored spot headshot", 1, (255, 255, 255))
    screen.blit(label, (round(x),round(y-10)))

    #pygame.draw.line(screen, (0, 255, 0), (x+200, y), (x + 300, y), 5)
    draw_circle(1, screen, (0, 255, 0),
                round(x +150 - 15),
                round(y + 5),
                10)
    label = font.render("armored spot hit", 1, (255, 255, 255))
    screen.blit(label, (round(x+150),round(y)))

    #pygame.draw.line(screen, (0, 255, 0), (x+200, y), (x + 300, y), 5)
    draw_circle(1, screen, (0, 255, 150),
                round(x +200 - 15),
                round(y - 5),
                10)
    label = font.render("armored spot headshot", 1, (255, 255, 255))
    screen.blit(label, (round(x+200),round(y-10)))

    draw_circle(1, screen, (255, 255, 0),
                round(x +300 - 15),
                round(y + 5),
                10)
    #pygame.draw.line(screen, (255, 255, 0), (x+400, y), (x + 500, y), 5)
    label = font.render("stagger", 1, (255, 255, 255))
    screen.blit(label, (round(x+300),round(y)))


class list_choice_dependency:
    def __init__(self,Data):
        self.Data = Data
        self.herochoice = None
        self.weaponchoice = None
        self.attackchoice = None
        self.currenthero = None
        self.currentweapon = None
        self.currentattack = None
        self.weapontable = None
        #self.load_list('hero')
        #self.load_list('weapon')
        #self.load_list('attack')
    def set_herochoice(self,Listbox):
        self.herochoice = Listbox
        self.currenthero = Listbox.selectedelement
    def set_weaponchoice(self, Listbox):
        self.weaponchoice = Listbox
        self.currentweapon = Listbox.selectedelement
    def set_attackchoice(self, Listbox):
        self.attackchoice = Listbox
        self.currentattack = Listbox.selectedelement
    def set_weapontable(self,weapontable):
        self.weapontable = weapontable
    def update(self):
        if self.currenthero != self.herochoice.selectedelement:
            self.weaponchoice.emptylist()
            self.attackchoice.emptylist()
            self.load_list('weapon')
            self.load_list('attack')
            self.currenthero = self.herochoice.selectedelement
        if self.currentweapon != self.weaponchoice.selectedelement:
            self.attackchoice.emptylist()
            self.load_list('attack')
            if self.weapontable != None:
                self.weapontable.update()
            self.currentweapon = self.weaponchoice.selectedelement
    def load_list(self,choice_type):
        if choice_type == 'hero':
            listofHeroes = [item['name'] for item in self.Data]
            self.write_list(self.herochoice, listofHeroes)
            return listofHeroes
        elif choice_type == 'weapon':
            for hero in self.Data:
                if hero['name'] == self.herochoice.selectedelement:
                    listofWeapons = [item['name'] for item in hero['weapons']]
                    self.write_list(self.weaponchoice, listofWeapons)
                    return listofWeapons
        elif choice_type == 'attack':
            for hero in self.Data:
                for weapon in hero['weapons']:
                    if weapon['name'] == self.weaponchoice.selectedelement:
                        listofAttacks = [item['name'] for item in weapon['attacks']]
                        self.write_list(self.attackchoice, listofAttacks)
                        return listofAttacks
        elif choice_type == 'attack_value':
            for hero in self.Data:
                for weapon in hero['weapons']:
                    if weapon['name'] == self.weaponchoice.selectedelement:
                        for attack in weapon['attacks']:
                            if attack['name'] == self.attackchoice.selectedelement:
                                AttackValues = attack['values']
                                return AttackValues
    def write_list(self,choicelist,data):
        for item in data:
            choicelist.addlistelement(item)


class weapon_table:
    def __init__(self, SelectionObject,screen,left,top,width,height):
        self.SO = SelectionObject
        self.screen = screen
        self.Data = self.load_AttackStats()
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.imagesize_height = self.height / 10 * 2  # self.imagesize_width #
        self.imagesize_width = self.imagesize_height #self.width / 10*1
        self.icon_damage = self.loadImage("Images\\damage.png")
        self.icon_armordamage = self.loadImage("Images\\armordamage.png")
        self.icon_cleavelimit = self.loadImage("Images\\cleavelimit.png")
        self.icon_attackspeed = self.loadImage("Images\\attackspeed.png")
        self.font = pygame.font.Font(FONT, 10)
        self.row_height = round(self.font.size("Standardbeispiel!")[1])
        self.calcColumns()

    def calcColumns(self):
        self.column2left = self.left +self.width /40*15
        self.column3left = self.left +self.width /40*21
        self.column4left = self.left + self.width /40*27
        self.column5left = self.left + self.width /40*35
        self.column6left = self.left + self.width

    def loadImage(self,Path):
        img = pygame.image.load(Path).convert()
        img_resized = pygame.transform.scale(img, (round(self.imagesize_width), round(self.imagesize_height)))
        return img_resized

    def update(self):
        self.Data = self.load_AttackStats()

    def load_AttackStats(self):
        for hero in self.SO.Data:
            for weapon in hero['weapons']:
                if weapon['name'] == self.SO.weaponchoice.selectedelement:
                    return weapon['attacks']

    def drawcolumn(self,image,left,nextleft):
        pygame.draw.line(self.screen, (255, 255, 255), (left, self.top), (left, self.top + self.height))
        self.screen.blit(image,(round((left+nextleft-self.imagesize_width)/2) ,self.top))

    def drawrow(self,Data,top):
        margin = 5
        self.drawtext(Data['name'],self.left,top)
        self.drawtext(str(Data['values'][0]['damage']), self.left,top,self.column3left-margin)
        self.drawtext(str(Data['values'][0]['armordamage']), self.left, top, self.column4left-margin)
        self.drawtext(str(Data['values'][0]['cleave']), self.column4left+margin, top )
        self.drawtext(str(Data['values'][0]['stagger']), self.left, top, self.column5left-margin)
        self.drawtext(str(Data['values'][0]['speed']), self.left, top, self.column6left - margin)

    def drawtext(self,text,x,y,xto=None):
        label = self.font.render(text, 1, (255, 255, 255))
        if xto != None:
            x = xto-self.font.size(text)[0]
        self.screen.blit(label, (round(x), round(y)))

    def draw(self):
        self.drawcolumn(self.icon_damage,self.column2left,self.column3left)
        self.drawcolumn(self.icon_armordamage, self.column3left, self.column4left)
        self.drawcolumn(self.icon_cleavelimit, self.column4left, self.column5left)
        self.drawcolumn(self.icon_attackspeed, self.column5left, self.column6left)
        pygame.draw.line(self.screen, (255,255,255), (self.left, self.top+self.imagesize_height), (self.left+self.width, self.top+self.imagesize_height))
        currentheight = self.top+self.imagesize_height+5
        for Attack in self.Data:
            self.drawrow(Attack,currentheight)
            currentheight += self.row_height




def Check_Stagger_Dmg_Bonus(StaggerGrp,EnemyStaggerFactor,w_att):
    if w_att.ranged == 0:
        if StaggerGrp.currentactive.text == 'Bulwark':
            if EnemyStaggerFactor.value == 1:
                w_att.damage = w_att.damage * 1.2
                w_att.armorDamage = w_att.armorDamage * 1.2
            if EnemyStaggerFactor.value == 2:
                w_att.damage = w_att.damage * 1.4
                w_att.armorDamage = w_att.armorDamage * 1.4
        if StaggerGrp.currentactive.text == 'Mainstay':
            if EnemyStaggerFactor.value == 1:
                w_att.damage = w_att.damage * 1.4
                w_att.armorDamage = w_att.armorDamage * 1.4
            if EnemyStaggerFactor.value == 2:
                w_att.damage = w_att.damage * 1.6
                w_att.armorDamage = w_att.armorDamage * 1.6
        if StaggerGrp.currentactive.text == 'Smiter':
            if EnemyStaggerFactor.value == 0:
                w_att.damage = w_att.damage * 1.2
                w_att.armorDamage = w_att.armorDamage * 1.2
            if EnemyStaggerFactor.value == 1:
                w_att.damage = w_att.damage * 1.2
                w_att.armorDamage = w_att.armorDamage * 1.2
            if EnemyStaggerFactor.value == 2:
                w_att.damage = w_att.damage * 1.4
                w_att.armorDamage = w_att.armorDamage * 1.4
        if StaggerGrp.currentactive.text == 'Assassin':
            if EnemyStaggerFactor.value == 1:
                w_att.damage = w_att.damage * 1.2
                w_att.armorDamage = w_att.armorDamage * 1.2
            if EnemyStaggerFactor.value == 2:
                w_att.damage = w_att.damage * 1.4
                w_att.armorDamage = w_att.armorDamage * 1.4
    if StaggerGrp.currentactive.text == 'Enhanced Power':
        w_att.damage = w_att.damage * 1.075
        w_att.armorDamage = w_att.armorDamage * 1.075


def runMain():
    clock = pygame.time.Clock()
    run = True

    pygame.init()
    pygame.display.set_caption("Vermintide2BreakPointCalc")
    UI_Handler = Widgets.Widget_Handler()
    MonsterFrame = Widgets.Frame(WIN,WIN,0,60.0,100.0,40.0,BLACK)
    Enemies = EnemyView(WIN, MonsterFrame)
    MonsterFrame.addcontent(Enemies)
    HeroFrame = Widgets.Frame(WIN, WIN, 0, 0.0,100.0,60.0,(0,0,0))
    MonsterScroll = Widgets.Scrollbar(WIN,MonsterFrame)
    HeroData = loadHeroData()

    Choices = list_choice_dependency(HeroData)
    DifficultyChoice = Widgets.Listbox(WIN, HeroFrame, 75, 5, 20, 5)
    DifficultyChoice.addlistelement('legendary')
    HeroChoice = Widgets.Listbox(WIN,HeroFrame,5,5,20,5)
    WeaponChoice = Widgets.Listbox(WIN, HeroFrame, 5, 15, 20, 5)
    AttackChoice = Widgets.Listbox(WIN, HeroFrame, 5, 25, 20, 5)
    Choices.set_herochoice(HeroChoice)
    Choices.set_weaponchoice(WeaponChoice)
    Choices.set_attackchoice(AttackChoice)


    # Initiales Daten Laden
    Choices.load_list('hero')
    Choices.load_list('weapon')
    Choices.load_list('attack')

    AttackValues = Choices.load_list('attack_value')
    w_att = Weapon(AttackValues) # Central Element For Current Weaponstats

    Baseheight = HEIGHT / 40 * 16
    Selection_Bulwark = Widgets.radiobtn(WIN,'Bulwark',WIDTH / 20 * 3,Baseheight)
    Selection_Mainstay = Widgets.radiobtn(WIN, 'Mainstay', WIDTH / 20 * 5, Baseheight)
    Selection_EnhancedPower = Widgets.radiobtn(WIN, 'Enhanced Power', WIDTH / 20 * 7, Baseheight)
    Selection_Smiter = Widgets.radiobtn(WIN, 'Smiter', WIDTH / 20 * 10, Baseheight)
    Selection_Assassin = Widgets.radiobtn(WIN, 'Assassin', WIDTH / 20 * 12, Baseheight)
    EnemyStaggerFactor = scalingfactor('Enemy_StaggerLevel',WIN, WIDTH / 20 * 15, Baseheight,0,2)
    EnemyBleedStatus = Widgets.radiobtn(WIN, 'Enemy_Bleeding/Poisoned', WIDTH / 20 * 15, HEIGHT / 20 * 6)

    StaggerGrp = Widgets.radiobtn_grp()
    StaggerGrp.add(Selection_Bulwark)
    StaggerGrp.add(Selection_Mainstay)
    StaggerGrp.add(Selection_EnhancedPower)
    StaggerGrp.add(Selection_Smiter)
    StaggerGrp.add(Selection_Assassin)

    Check_Stagger_Dmg_Bonus(StaggerGrp,EnemyStaggerFactor,w_att)

    Baseheight = HEIGHT / 40 * 18
    Baseheight1 = HEIGHT / 40 * 20
    DmgBonus = scalingfactor("BonusPower", WIN, WIDTH / 20 * 3, Baseheight)
    DmgvsChaos = scalingfactor("vsChaos",WIN,  WIDTH/20*7,Baseheight)
    DmgvsSkaven = scalingfactor("vsSkaven", WIN, WIDTH / 20 * 7, Baseheight1)
    DmgvsInfantry = scalingfactor("vsInfantry",WIN,  WIDTH/20*11,Baseheight)
    DmgvsArmor = scalingfactor("vsArmor", WIN, WIDTH / 20 * 11, Baseheight1)
    DmgvsBerserker = scalingfactor("vsBerserker",WIN,  WIDTH/20*15,Baseheight)
    DmgvsMonster = scalingfactor("vsMonster", WIN, WIDTH / 20 * 15, Baseheight1)

    WeaponTable = weapon_table(Choices, WIN, WIDTH / 40 * 18, HEIGHT / 40 * 3,WIDTH / 20 * 10,HEIGHT / 20 * 5)
    Choices.set_weapontable(WeaponTable)

    Enemies.calcEnemyWeaponData(w_att.damage*(1+DmgBonus.value/100),w_att.stagger,w_att.attackspeed,w_att.cleave,w_att.armorDamage*(1+DmgBonus.value/100),DmgvsChaos.value,DmgvsSkaven.value,DmgvsInfantry.value,DmgvsArmor.value,DmgvsBerserker.value,DmgvsMonster.value)

    UI_Handler.add(HeroFrame)
    UI_Handler.add(HeroChoice)
    UI_Handler.add(DifficultyChoice)
    UI_Handler.add(MonsterFrame)
    UI_Handler.add(MonsterScroll)
    #UI_Handler.add(ClassChoice)
    UI_Handler.add(WeaponChoice)
    UI_Handler.add(AttackChoice)
    # // Scalingfactors //
    UI_Handler.add(DmgvsChaos)
    UI_Handler.add(DmgvsSkaven)
    UI_Handler.add(DmgvsInfantry)
    UI_Handler.add(DmgvsArmor)
    UI_Handler.add(DmgvsBerserker)
    UI_Handler.add(DmgvsMonster)
    UI_Handler.add(DmgBonus)
    UI_Handler.add(Selection_Bulwark)
    UI_Handler.add(Selection_Mainstay)
    UI_Handler.add(Selection_EnhancedPower)
    UI_Handler.add(Selection_Smiter)
    UI_Handler.add(Selection_Assassin)
    UI_Handler.add(EnemyStaggerFactor)
    UI_Handler.add(WeaponTable)
    #UI_Handler.add(EnemyBleedStatus)

    while run:
        clock.tick(FPS)
        mx,my = pygame.mouse.get_pos() # Aktuelle X&Y Koordinate für Mauszeiger
        for event in pygame.event.get():
            MonsterScroll.event_handler(event)
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN: #Mousebutton gedrückt
                if event.button == 1: #linke Maustaste
                    None
                    UI_Handler.openlist()
                elif event.button == 2: #mittlere Maustase
                    None
                elif event.button == 3: #rechte Maustaste
                    None
                else:
                    print("Input not recognized!")
            elif event.type == pygame.MOUSEBUTTONUP: #Mousebutton losgelassen
                None
        # -------------------------------- gehört irgendwann in ne Klasse ------ Abhängigkeiten unter Listboxen
        for hero in HeroData:
            for weapon in hero['weapons']:
                if weapon['name'] == WeaponChoice.selectedelement:
                    for attack in weapon['attacks']:
                        # print(attack)
                        # print(attack.keys())
                        if attack['name'] == AttackChoice.selectedelement:
                            AttackValues = attack['values']
        #print(AttackValues)
        w_att.loadWeaponData(AttackValues)
        Check_Stagger_Dmg_Bonus(StaggerGrp, EnemyStaggerFactor, w_att)
        Enemies.calcEnemyWeaponData(w_att.damage * (1 + DmgBonus.value / 100), w_att.stagger, w_att.attackspeed,
                                    w_att.cleave, w_att.armorDamage * (1 + DmgBonus.value / 100), DmgvsChaos.value,
                                    DmgvsSkaven.value, DmgvsInfantry.value, DmgvsArmor.value, DmgvsBerserker.value,
                                    DmgvsMonster.value)

        StaggerGrp.update()
        Choices.update()
        MonsterScroll.update()
        WIN.fill(BLACK)

        UI_Handler.draw()
        Enemies.draw()
        UI_Handler.drawopenlist()
        draw_infos(WIN)
        pygame.display.update()

if __name__ == '__main__':
    runMain()