import random
import time

#Functions
def printwithdelay(text,delay):
    print(text)
    time.sleep(delay)
def checkList(parameter,list):
    for item in list:
        if item.name.lower()==parameter:
            return item
    return None
def checkDict(parameter,dict):
    for slot in dict:
        if dict[slot].name.lower()==parameter:
            return dict[slot],slot
    return None,None
def appropriatearticle(word):
    firstletter,_=word.lower().split(maxsplit=1)
    article ="a"
    vowel=["a","e","i","o","u"]
    if firstletter in vowel:
        article+="n"
    return article
class Entity:
    def takehit(self,dmg):
        self.health-=dmg
        if self.health<0:
            self.die()
    def die(self):
        print("die")
        
class Items:
    def __init__(self,name,tooltip):
        self.tooltip=tooltip
        self.name=name
    def printAttributes(self):
        printwithdelay("This item has no attributes",.5)
    slot=None
class Mainhand(Items):
    def printAttributes(self):
        printwithdelay(f"Mainhand\nDamage> {self.damage}\n{self.tooltip}",.5)
    slot="mainhand"
class Melee(Mainhand):
    def __init__(self,name,damage,tooltip):
        self.damage=damage
        self.name=name
        self.tooltip=tooltip
class Armor(Items):
    def __init__(self,name,defense,tooltip):
        self.defense=defense
        self.name=name
        self.tooltip=tooltip
    def printAttributes(self):
        printwithdelay(f"Defense> {self.defense}\n{self.tooltip}",.5)
class Helmet(Armor):
    def printAttributes(self):
        printwithdelay(f"Helmet\nDefense> {self.defense}\n{self.tooltip}",.5)
    slot="helmet"
class Chestplate(Armor):
    def printAttributes(self):
        printwithdelay(f"Chestplate\nDefense> {self.defense}\n{self.tooltip}",.5)
    slot="chestplate"
class Pants(Armor):
    def printAttributes(self):
        printwithdelay(f"Pants\nDefense> {self.defense}\n{self.tooltip}",.5)
    slot="pants"
class Boot(Armor):
    def printAttributes(self):
        printwithdelay(f"Boots\nDefense> {self.defense}\n{self.tooltip}",.5)
    slot="boots"
class Player(Entity):
    health=100
    maxhealth=100
    items=[]
    money=0
    currentfloor=0
    slots={"mainhand":Melee("Sledgehammer",10,"Quite heavy, but it can pack a punch."),
           "helmet":Helmet("Hardhat",2,"Unless you are dueling a bunch of falling rocks, this might not do much."),
           "chestplate":Chestplate("Reflective Vest",1,"Unless you are battling drunk drivers this may not do much."),
           "pants":Pants("Work Pants",1,"Unless you are attempting to look the least flattering, this may not do much."),
           "boots":Boot("Nike Kicks",50,"Strangely very protective, must be the fact that they aren't creased.")}
    def die(self):
        quit()
    def choose(self,options):
        choice=input("Actions >")
        if choice.lower()=="stats":
            printwithdelay(f"Health> {self.health}\nMax Health> {self.maxhealth}\nMoney> {self.money}\nCurrent Floor> {self.currentfloor}",.5)
            self.choose(options)
        elif choice.lower()=="items":
            printwithdelay("Items:",.2)
            for item in self.items:
                printwithdelay(item.name,.2)
            printwithdelay(f"Equipped:\nMainhand> {self.slots['mainhand'].name}\nHelmet> {self.slots['helmet'].name}\nChestplate> {self.slots['chestplate'].name}\nPants> {self.slots['pants'].name}\nBoots> {self.slots['boots'].name}",.2)
            self.InventoryMenu()
            self.choose(options)
        elif choice.lower() in options:
            event=options [choice]
            event.run(self)
        else:
            printwithdelay(f"{choice} is not a valid action",.5)
            self.choose(options)
    def InventoryMenu(self):
        choice=input("Inventory >")
        if choice.lower()=="back":
            return
        command,parameter=choice.lower().split(' ',1)
        if command=="equip":
            self.equipItem(parameter)
        elif command=="unequip":
            self.unequipItem(parameter)
        elif command=="use":
            print("")
        elif command=="inspect":
            self.inspectItem(parameter)
        else:
            printwithdelay(f"{command} is not a valid action",.5)
            self.InventoryMenu()
    def inspectItem(self,parameter):
        item=checkList(parameter,self.items)
        if item is not None:
            item.printAttributes()
            return
        item,slot=checkDict(parameter,self.slots)
        if item.name == "Nothing":
            printwithdelay(f"You stare into space for several moments contemplating nothing",.5)
            return            
        if item is not None:
            item.printAttributes()
        else:
            printwithdelay(f"{parameter} is not a valid item",.5)
            return
    def unequipItem(self,parameter):
        item,slot=checkDict(parameter,self.slots)
        if item.name == "Nothing":
            printwithdelay(f"{parameter} is not a valid item.",.5)
            return
        if item is None:
            printwithdelay(f"{parameter} is not equipped.",.5)
            return
        self.items.append(self.slots[slot])
        self.slots[slot]=Items("Nothing","Nothing Equipped")
    def equipItem(self,parameter):
        item=checkList(parameter,self.items)
        if item is None:
            printwithdelay(f"{parameter} is not a valid item",.5)
            return
        if item.slot is None:
            printwithdelay(f"{parameter} is not equippable.",.5)
            return
        if self.slots[item.slot] !=Items("Nothing","Nothing Equipped"):
            self.items.append(self.slots[item.slot])
        self.slots[item.slot]=item
        self.items.remove(item)
    def pickup(self,item):
        self.items.append(item)
        firstletter,_=item.name.lower().split(maxsplit=1)
        article ="a"
        vowel=["a","e","i","o","u"]
        if firstletter in vowel:
            article+="n"
        printwithdelay(f"You Picked up {article} {item.name}!",.3)
    def pickupList(self,items):
        for item in items:
            self.pickup(item)
                
            
class Game:
    player=Player()
    def openingsequence(self):
        printwithdelay("Welcome to the Ebony Dungeon",.5)
        printwithdelay("You can make choices to get further into the dungeon, but beware of the danger",.5)
        self.__entrance()
    def __entrance(self):
        printwithdelay("You stand at the entrance to a deep dungeon",.5)
        self.player.pickupList([Melee("Gold Broadsword",17,f"It may be fancy, but it gets the job done."),Melee("DIAMOND BROADSWORD",25,f"It may be super fucking cool, but it deserves to be praised.")])
        entranceEvent=EntranceEvent(self.player)
        options={"enter":entranceEvent,"go":entranceEvent,"proceed":entranceEvent}
        self.player.choose(options)
        
class Encounter:
    def EnterRoom(self,player):
        rng=random.uniform(1.2**player.currentfloor-2*1.03**-player.currentfloor,1.2**player.currentfloor+2*1.03**-player.currentfloor)
        if rng<1:
            rng=1
        miniEncounterNumber=round(rng)
    def miniEncounter(self,player):
        print("")
        
class Event:
    encounter=Encounter()
    player=Player()
    def __init__(self,player):
        self.player=player
    def run(self):
        return
class EntranceEvent(Event):
    def run(self):
        self.player.currentfloor+=1
        self.encounter.player.EnterRoom()
        
class Enemy(Entity):
    def spawn():
        print("")


        
game=Game()
game.openingsequence()

