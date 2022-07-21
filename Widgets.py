import pygame

FONT = "Humongous of Eternity St.ttf"


class Frame:
    def __init__(self,screen,parent,offset_x,offset_y,size_w_percent,size_h_percent,color=(255,255,255), border = None):
        self.screen = screen
        self.parent = parent
        self.left = offset_x/100* self.parent.get_size()[0]
        self.relativeleft = self.left
        self.width = size_w_percent/100 * self.parent.get_size()[0]
        self.top = offset_y/100* self.parent.get_size()[1]
        self.height = size_h_percent/100 * self.parent.get_size()[1]
        self.border = border
        self.color = color
        self.contentwidth = self.width
        self.content = []
        #print("Frame left:",self.left)
        #print("Frame width:", self.width)
        #print("Frame top:", self.top)
        #print("Frame height:", self.height)
    def addcontent(self,content):
        self.content.append(content)
        self.calc_contentwidth()
    def calc_contentwidth(self):
        self.contentwidth = 0
        for i in self.content:
            self.contentwidth += i.contentwidth
    def get_size(self):
        return (self.width,self.height,self.contentwidth)
    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.left, self.top, self.width, self.height))

class Listbox:
    def __init__(self,screen,parent,offset_x,offset_y,size_w_percent,size_h_percent):
        self.screen = screen
        self.parent = parent
        self.left = offset_x/100* self.parent.get_size()[0]
        self.width = size_w_percent/100 * self.parent.get_size()[0]
        self.top = offset_y/100* self.parent.get_size()[1]
        self.height = size_h_percent/100 * self.parent.get_size()[1]
        self.listelements = []
        self.selectedelement = None
        self.islist_open_status = 0
        #print("creating Listbox @",self.left,self.top,self.width,self.height)

    def emptylist(self):
        self.listelements = []
        self.selectedelement = None

    def addlistelement(self,element):
        self.listelements.append(element)
        if(self.selectedelement == None):
            self.selectedelement = self.listelements[0]

    def update(self):
        mx, my = pygame.mouse.get_pos()
        justselected = False
        # Die Liste ist bereits offen
        if self.islist_open_status == 1 and self.left < mx and mx < self.left + self.width and self.top < my and my < self.top + self.height*len(self.listelements):
            for i in range(len(self.listelements)):
                if self.top+(self.height/ 20 * 1)+(self.height*i) < my and my < self.top+(self.height/ 20 * 1)+(self.height*(i+1)):
                    #print('clicked Element ',i)
                    self.selectedelement = self.listelements[i]
                    self.islist_open_status = 0
                    justselected = True
        else:
            # Es wurde außerhalb der Liste geklickt -> schließen
            self.islist_open_status = 0
        # Die Liste soll geöffnet werden
        if justselected == False and self.islist_open_status == 0 and self.left < mx and mx < self.left+self.width and self.top < my and my < self.top+self.height:
            self.islist_open_status = 1


    def draw(self):
        pygame.draw.rect(self.screen, (255,255,255), (self.left, self.top, self.width, self.height),2,0,0,0,0,0)
        if(self.selectedelement != None):
            font = pygame.font.Font(FONT, 10)
            label = font.render(self.selectedelement, 1, (255, 255, 255))
            self.parent.screen.blit(label, (round(self.left + self.width/20 * 1),round(self.top + self.height / 20 * 1)))

    def draw_openlist(self):
        if self.islist_open_status == 1:
            pygame.draw.rect(self.screen, (0, 0, 0), (self.left, self.top, self.width, self.height*len(self.listelements)) )
            pygame.draw.rect(self.screen, (255, 255, 255), (self.left, self.top, self.width, self.height * len(self.listelements)), 2)
            if (len(self.listelements) > 0):
                font = pygame.font.Font(FONT, 10)
                for i in range(len(self.listelements)):
                    label = font.render(self.listelements[i], 1, (255, 255, 255))
                    self.parent.screen.blit(label,( round(self.left + self.width / 20 * 1),
                                                    round(self.top+(self.height/ 20 * 1)+(self.height*i) )))


class Widget_Handler:
    def __init__(self):
        self.widgets = []

    def add(self,Element):
        self.widgets.append(Element)

    def draw(self):
        for widget in self.widgets:
            widget.draw()

    def openlist(self):
        openlist = None
        for widget in self.widgets:
            if hasattr(widget, 'islist_open_status'):
                if widget.islist_open_status == 1:
                    openlist = widget
        for widget in self.widgets:
            if hasattr(widget, 'update'): #prüft ob das widget Object die update-methode hat
                if openlist == None or openlist == widget:
                    widget.update()
                    #print("Widget soll geöffnet werden")

    def drawopenlist(self):
        for widget in self.widgets:
            if hasattr(widget, 'draw_openlist'): #prüft ob das widget Object die update-methode hat
                widget.draw_openlist()



class radiobtn:
    def __init__(self,screen,text,x,y):
        self.screen = screen
        self.text = text
        self.font = pygame.font.Font(FONT, 10)
        self.x = x
        self.y = y
        self.checked = False
        self.radius = round(self.font.size(self.text)[1]/3)

    def update(self):
        mx, my = pygame.mouse.get_pos()
        if self.x < mx and mx < self.x + self.radius*2 and self.y < my and my < self.y + self.radius*2:
            if self.checked == False:
                self.checked = True
            else:
                self.checked = False

    def draw(self):
        pygame.draw.circle(self.screen, (255,255,255), (self.x+self.radius,self.y+self.radius), self.radius)
        label = self.font.render(self.text, 1, (255, 255, 255))
        self.screen.blit(label, (round(self.x + self.radius*2.5), round(self.y)))
        if self.checked == True:
            pygame.draw.circle(self.screen, (50, 50, 50), (self.x + self.radius, self.y + self.radius), self.radius*0.8)

class radiobtn_grp:
    def __init__(self):
        self.btns = []
        self.currentactive = None
    def add(self,btn):
        if len(self.btns) == 0:
            self.currentactive = btn
            self.currentactive.checked = True
        self.btns.append(btn)
    def update(self):
        for btn in self.btns:
            if btn.checked == True and btn != self.currentactive:
                self.currentactive.checked = False
                self.currentactive = btn



class Scrollbar:
    def __init__(self,screen, DecoratedObject):
        self.x_axis = 0
        self.change_x = 0
        self.screen = screen
        self.parentObject = DecoratedObject

        self.parent_width = DecoratedObject.get_size()[0]
        self.parent_height = DecoratedObject.get_size()[1]
        self.parent_contentwidth = DecoratedObject.get_size()[2]

        self.buttonedge = 20
        self.height = self.buttonedge #self.parent_height
        self.width = self.parent_width

        self.top = self.parentObject.top+self.parent_height-self.height
        self.left = self.parentObject.left

        bar_width = int((self.width - self.buttonedge*2) / (self.parent_contentwidth / (self.parent_width * 1.0))) #image_height/(SCREEN_HEIGHT * 1.0)

        self.bar_rect = pygame.Rect(self.left,self.top, bar_width,self.height)
        #Rect(left, top, width, height)
        self.bar_leftbutton_pos = (0,self.top)
        self.bar_rightbutton_pos = (self.left+self.width-self.buttonedge, self.top)
        self.bar_left = pygame.Rect(0, self.top, self.buttonedge,self.buttonedge)
        self.bar_right = pygame.Rect(self.left+self.width-self.buttonedge, self.top, self.buttonedge, self.buttonedge)

        self.bar_left_image = pygame.image.load("images\\left.png").convert()
        self.bar_right_image = pygame.image.load("images\\right.png").convert()

        self.on_bar = False
        self.mouse_diff = 0

    def update(self):
        self.x_axis += self.change_x
        if self.x_axis > 0:
            self.x_axis = 0
        elif (self.x_axis + self.parent_contentwidth) < self.parent_width:
            self.x_axis = self.parent_width - self.parent_contentwidth

        height_diff = self.parent_contentwidth - self.parent_width

        scroll_length = self.parent_width - self.bar_rect.width - 40
        bar_half_lenght = self.bar_rect.width / 2 + 20
        self.parentObject.relativeleft = self.parentObject.left+self.x_axis

        if self.on_bar:
            pos = pygame.mouse.get_pos()
            self.bar_rect.x = pos[0] - self.mouse_diff
            if self.bar_rect.left < 20:
                self.bar_rect.left = 20
            elif self.bar_rect.right > (self.parent_width - 20):
                self.bar_rect.right = self.parent_width - 20
            self.x_axis = int(height_diff / (scroll_length * 1.0) * (self.bar_rect.centerx - bar_half_lenght) * -1)
        else:
            self.bar_rect.centerx = scroll_length / (height_diff * 1.0) * (self.x_axis * -1) + bar_half_lenght


    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.bar_rect.collidepoint(pos):
                self.mouse_diff = pos[0] - self.bar_rect.x
                self.on_bar = True
            elif self.bar_left.collidepoint(pos):
                self.change_x = 5
            elif self.bar_right.collidepoint(pos):
                self.change_x = -5

        if event.type == pygame.MOUSEBUTTONUP:
            self.change_x = 0
            self.on_bar = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.change_x = 5
            elif event.key == pygame.K_RIGHT:
                self.change_x = -5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.change_x = 0
            elif event.key == pygame.K_RIGHT:
                self.change_x = 0

    def draw(self):
        pygame.draw.rect(self.screen, (50,50,50), self.bar_rect)
        self.screen.blit(self.bar_left_image, self.bar_leftbutton_pos)
        self.screen.blit(self.bar_right_image, self.bar_rightbutton_pos)




'''
class Widg_Btn:
    def __init__(self,WIN,left,top,width,height,text = "",imagepath="",function = None):
        self.WIN = WIN
        self.XPos = left
        self.YPos = top
        self.width = width
        self.height = height
        self.text = text
        self.textangle = 0
        self.function = function
        self.visible = True
        if imagepath != "":
            self.Image = pygame.image.load(imagepath).convert_alpha()
            Imageratio = self.Image.get_height() / self.Image.get_width()
            self.Image = pygame.transform.scale(self.Image, (self.width - 5, math.floor(self.width*Imageratio) -5))
        else:
            self.Image = None

    def set_function(self,function):
        self.function = function

    def set_text(self,text):
        self.text = text

    def set_textangle(self,textangle):
        self.textangle = textangle

    def draw(self):
        pygame.draw.rect(self.WIN, DARKGREY, (self.XPos, self.YPos, self.width, self.height), 0, 1, 5, 5, 5, 5)  # Fill
        pygame.draw.rect(self.WIN, BLACK, (self.XPos, self.YPos, self.width, self.height), 2, 1, 5, 5, 5, 5)  # Border


        if self.text != "":
            font = pygame.font.Font(FONT, 10)
            textsize = font.size(self.text)[1]
            label = font.render(str(self.text), 1, WHITE)
            self.WIN.blit(label, (self.XPos,self.YPos))
        else:
            textsize = 0
        if self.Image != None:
            self.WIN.blit(self.Image, (self.XPos + 2,self.YPos + 2 + textsize))


    def set_visible(self,visible):
        self.visible = visible

    def wasiclicked(self):
        cp = pygame.mouse.get_pos()
        if ( self.visible == True and
            (cp[0] < self.XPos + self.width and cp[0] >= self.XPos and cp[1] < self.YPos + self.height and cp[1] >= self.YPos) # Rechteck
            ):
            return True
        return False

    def checkfunctioncall(self):
        if(self.wasiclicked()):
            self.function()


class Widg_alerthandler:
    def __init__(self,WIN):
        self.WIN = WIN
        self.alerts = []

    def draw(self):
        for alert in self.alerts:
            alert.draw()

    def check_buttonpresses(self):
        for alert in self.alerts:
            for btn in alert.buttons:
                btn.checkfunctioncall()

    def new_alert(self,text,btncount=2,ttl=None,function=None,function2=None):
        alert = Widg_Alert(self,text,btncount,ttl,function,function2)
        self.alerts.append(alert)
        return alert

    def del_alert(self,todel_alert):
        for alert in self.alerts:
            if alert is todel_alert:
                self.alerts.remove(alert)
                del alert
                del todel_alert



class Widg_Alert:
    def __init__(self,parent,text,btncount=2,ttl=None,function=None,function2=None):
        self.parent = parent
        self.width = math.floor(WIDTH/5)
        self.height = math.floor(HEIGHT/5)
        self.xpos = math.floor(WIDTH/2)-math.floor(self.width/2)
        self.ypos = math.floor(HEIGHT/2)-math.floor(self.height/2)
        self.text = text
        self.ttl = ttl
        self.buttons = []
        self.function=function
        self.function2=function2
        self.active = True
        if btncount == 1: # ist ein mit OK zu bestätigender Alert
            self.buttons.append(Widg_Btn(self.parent.WIN,self.xpos+math.floor(self.width/5*2),self.ypos+(self.height/10*9),math.floor(self.width/5),math.floor(self.height/10),text="OK",function=self.ok_function))
        if btncount == 2:
            self.buttons.append(Widg_Btn(self.parent.WIN,self.xpos+math.floor(self.width/5*1),self.ypos+(self.height/10*9),math.floor(self.width/5),math.floor(self.height/10),text="Yes",function=self.yes_function))
            self.buttons.append(Widg_Btn(self.parent.WIN, self.xpos + math.floor(self.width/5*3),self.ypos + (self.height/10*9), math.floor(self.width/5),math.floor(self.height/10), text="No", function=self.no_function))

    def draw(self):
        if self.active == True:
            pygame.draw.rect(self.parent.WIN, DARKGREY, (self.xpos, self.ypos, self.width, self.height), 0, 1, 5, 5, 5, 5)  # Fill
            pygame.draw.rect(self.parent.WIN, BLACK, (self.xpos, self.ypos, self.width, self.height), 2, 1, 5, 5, 5, 5)  # Border

            font = pygame.font.Font(FONT, 10)
            label = font.render(self.text, 1, WHITE)
            self.parent.WIN.blit(label, (self.xpos+self.width/10*1,self.ypos+self.height/10*1))

            for btn in self.buttons:
                btn.draw()

    def ok_function(self):
        if self.active == True:
            #print("OK was clicked!",self.function)
            if self.function != None:
                self.function()
            self.active = False
            self.parent.del_alert(self)

    def yes_function(self):
        if self.active == True:
            #print("Yes was clicked!",self.function)
            if self.function != None:
                self.function()
            self.active = False
            self.parent.del_alert(self)

    def no_function(self):
        if self.active == True:
            #print("No was clicked!",self.function2)
            if self.function2 != None:
                self.function2()
            self.active = False
            self.parent.del_alert(self)

'''