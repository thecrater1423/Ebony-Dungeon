import random
import time
#Functions
def printwithdelay(text):
    delay=.1
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
    letters=list(word.lower())
    article ="a"
    vowel=["a","e","i","o","u"]
    if letters[0] in vowel:
        article+="n"
    return article
class Entity:
    def takehit(self,dmg):
        self.health-=dmg
        if self.health<=0:
            self.die()
    def heal(self,health):
        self.health+=health
        if self.health>self.maxhealth:
            self.health=self.maxhealth
    def die(self):
        print("die")
        
class Items:
    def __init__(self,name,tooltip):
        self.tooltip=tooltip
        self.name=name
    def printAttributes(self):
        printwithdelay("This item has no attributes")
    slot=None
class Mainhand(Items):
    slot="mainhand"
class Melee(Mainhand):
    def __init__(self,name,damage,tooltip,critpower,critchance):
        self.damage=damage
        self.name=name
        self.tooltip=tooltip
        self.critpower=critpower
        self.critchance=critchance
    def printAttributes(self):
        printwithdelay(f"Mainhand\nDamage> {self.damage}\nCrit Power> {self.critpower}\nCrit Chance> {self.critchance}\n{self.tooltip}")
class Armor(Items):
    def __init__(self,name,defense,tooltip):
        self.defense=defense
        self.name=name
        self.tooltip=tooltip
    def printAttributes(self):
        printwithdelay(f"Defense> {self.defense}\n{self.tooltip}")
class Helmet(Armor):
    def printAttributes(self):
        printwithdelay(f"Helmet\nDefense> {self.defense}\n{self.tooltip}")
    slot="helmet"
class Chestplate(Armor):
    def printAttributes(self):
        printwithdelay(f"Chestplate\nDefense> {self.defense}\n{self.tooltip}")
    slot="chestplate"
class Pants(Armor):
    def printAttributes(self):
        printwithdelay(f"Pants\nDefense> {self.defense}\n{self.tooltip}")
    slot="pants"
class Boot(Armor):
    def printAttributes(self):
        printwithdelay(f"Boots\nDefense> {self.defense}\n{self.tooltip}")
    slot="boots"
class Player(Entity):
    health=100
    maxhealth=100
    items=[]
    money=0
    currentfloor=0
    slots={"mainhand":Melee("Sledgehammer",25,"Quite heavy, but it can pack a punch.",2.5,.07),
           "helmet":Helmet("Hardhat",3,"Unless you are dueling a bunch of falling rocks, this might not do much."),
           "chestplate":Chestplate("Reflective Vest",2,"Unless you are battling drunk drivers this may not do much."),
           "pants":Pants("Work Pants",2,"Unless you are attempting to look the least flattering, this may not do much."),
           "boots":Boot("Nike Kicks",1,"A lot more stylish than they are protective.")}
    def defense(self):
        defense=self.slots["helmet"].defense+self.slots["chestplate"].defense+self.slots["pants"].defense+self.slots["boots"].defense
        return defense
    def die(self):
        printwithdelay("You have died.")
        quit()
    def choose(self,options):
        choice=input("Actions >")
        if choice.lower() in ["stats","health","money","floor"]:
            printwithdelay(f"Health> {self.health}\nMax Health> {self.maxhealth}\nMoney> {self.money}\nCurrent Floor> {self.currentfloor}")
            self.choose(options)
        elif choice.lower()in ["items","item","inventory"]:
            printwithdelay("Items:")
            for item in self.items:
                printwithdelay(item.name)
            printwithdelay(f"Equipped:\nMainhand> {self.slots['mainhand'].name}\nHelmet> {self.slots['helmet'].name}\nChestplate> {self.slots['chestplate'].name}\nPants> {self.slots['pants'].name}\nBoots> {self.slots['boots'].name}")
            self.InventoryMenu()
            self.choose(options)
        elif choice.lower() in options:
            event=options[choice.lower()]
            event.run()
        else:
            printwithdelay(f"{choice} is not a valid action")
            self.choose(options)
    def InventoryMenu(self):
        choice=input("Inventory >")
        if choice.lower()=="back":
            return
        try:
            command,parameter=choice.lower().split(' ',1)
        except ValueError:
            if choice.lower not in ["equip","unequip","use","inspect"]:
                printwithdelay(f"{choice} is not a valid action")
                self.InventoryMenu()
            printwithdelay(f"Incorrect Usage, Try:{choice} [item]")
            self.InventoryMenu()
            command,parameter=choice.lower().split(' ',1)
        else:
            if command=="equip":
                self.equipItem(parameter)
            elif command=="unequip":
                self.unequipItem(parameter)
            elif command=="use":
                print("")
            elif command=="inspect":
                self.inspectItem(parameter)
            else:
                printwithdelay(f"{command} is not a valid action")
                self.InventoryMenu()
        
    def inspectItem(self,parameter):
        item=checkList(parameter,self.items)
        if item is not None:
            item.printAttributes()
            return
        item,_=checkDict(parameter,self.slots)
        try:
            if item.name == "Nothing":
                printwithdelay(f"You stare into space for several moments contemplating nothing")
                return
        finally:
            if item is not None:
                item.printAttributes()
                return
            else:
                printwithdelay(f"{parameter} is not a valid item")
                return
        
    def unequipItem(self,parameter):
        item,slot=checkDict(parameter,self.slots)
        try:
            if item.name == "Nothing":
                printwithdelay(f"{parameter} is not a valid item.")
                return
        finally:
            if item is None:
                printwithdelay(f"{parameter} is not equipped.")
                return
            self.items.append(item)
            self.slots[slot]=Items("Nothing","Nothing Equipped")
            printwithdelay(f"You Unequipped your {item.name}")
    def equipItem(self,parameter):
        item=checkList(parameter,self.items)
        if item is None:
            printwithdelay(f"{parameter} is not a valid item")
            return
        if item.slot is None:
            printwithdelay(f"{parameter} is not equippable.")
            return
        if self.slots[item.slot] !=Items("Nothing","Nothing Equipped"):
            self.items.append(self.slots[item.slot])
        self.slots[item.slot]=item
        self.items.remove(item)
        article=appropriatearticle(item.name)
        printwithdelay(f"You Equipped {article} {item.name}!")

    def pickup(self,item):
        self.items.append(item)
        article=appropriatearticle(item.name)
        printwithdelay(f"You Picked up {article} {item.name}!")
    def pickupList(self,items):
        for item in items:
            self.pickup(item)
                
            
class Game:
    player=Player()
    def openingsequence(self):
        printwithdelay("Welcome to the Ebony Dungeon")
        printwithdelay("You can make choices to get further into the dungeon, but beware of the danger")
        self.__entrance()
    def __entrance(self):
        printwithdelay("You stand at the entrance to a deep dungeon")
        options={"enter":EntranceEvent(self.player),"go":EntranceEvent(self.player),"proceed":EntranceEvent(self.player)}
        self.player.choose(options)
        
class Encounter:
    def __init__(self,randomencounternumber,player):
        self.randomEncounterNumber=randomencounternumber
        self.player=player
    def createMeleeMonster(self,player):
        attributes={"Strong":{"strength":2,"vigor":1.25,"Intellect":1,"Decisiveness":1},
                    "Puny":{"strength":.5,"vigor":.75,"Intellect":1,"Decisiveness":1},
                    "Bulky":{"strength":1,"vigor":1.5,"Intellect":1,"Decisiveness":1},
                    "Large":{"strength":1,"vigor":2.25,"Intellect":1,"Decisiveness":1},
                    "Gargantuan":{"strength":1,"vigor":3,"Intellect":1,"Decisiveness":1},
                    "Skillful":{"strength":1,"vigor":1,"Intellect":1.5,"Decisiveness":2.5},
                    "Wise":{"strength":1,"vigor":1,"Intellect":2.5,"Decisiveness":1.5},
                    "Foolish":{"strength":1,"vigor":1,"Intellect":.5,"Decisiveness":.75},
                    "Gruntish":{"strength":1.5,"vigor":2,"Intellect":.5,"Decisiveness":.5},
                    "Average":{"strength":1,"vigor":1,"Intellect":1,"Decisiveness":1}}
        attribute,stats=random.choice(list(attributes.items()))
        monsters=["Goblin","Zombie","Ninja","Pirate","Henchman"]
        items={"weapons":["Sword","Scimitar","Waraxe","Shortsword","Longsword"],
               "helmets":["Greathelm","Helmet","Viking Helmet","Knight Helmet","Visor"],
               "chestplates":["Breastplate","Chestplate","Vest","Overarmor"],
               "pants":["Pantaloons","Knight Leggings"],
               "boots":["Combat Boots","Leather Boots"]}
        monsterName=attribute+" " +random.choice(monsters)
        randomoffset=random.uniform(-1,1)
        monsterWeaponName=monsterName+"'s "+random.choice(items["weapons"])
        monsterHelmetName=monsterName+"'s "+random.choice(items["helmets"])
        monsterChestplateName=monsterName+"'s "+random.choice(items["chestplates"])
        monsterPantsName=monsterName+"'s "+random.choice(items["pants"])
        monsterBootsName=monsterName+"'s "+random.choice(items["boots"])
        monsterItemTooltip=f"This once belonged to a {monsterName}"
        damage=round(stats["strength"]*11*1.2**player.currentfloor+2*randomoffset)
        defense=round(stats["vigor"]*.5*1.2**player.currentfloor+2*randomoffset)
        health=round(stats["vigor"]*50*1.2**player.currentfloor+5*round(randomoffset))
        critchance=round(stats["Intellect"]*(1/100)*1.2**player.currentfloor+randomoffset*stats["Intellect"]*(1/400)*1.2**player.currentfloor,2)
        critpower=round(stats["Decisiveness"]*.25*1.2**player.currentfloor+1+.25*abs(randomoffset),2)
        monster=Enemy(monsterName,health,
                      Melee(monsterWeaponName,damage,monsterItemTooltip,critpower,critchance),
                      Helmet(monsterHelmetName,defense,monsterItemTooltip),
                      Chestplate(monsterChestplateName,defense,monsterItemTooltip),
                      Pants(monsterPantsName,defense,monsterItemTooltip),
                      Boot(monsterBootsName,defense,monsterItemTooltip))
        return monster
    def beginEncounter(self,currentEncounter):
        currentMonster=self.createMeleeMonster(self.player)
        printwithdelay(f"You stumble into a {currentMonster.name}({currentMonster.health}/{currentMonster.maxhealth})!")
        options={"attack":AttackEvent(self.player,currentMonster,currentEncounter),"hit":AttackEvent(self.player,currentMonster,currentEncounter)}
        self.player.choose(options)
    def enemyRetalite(self,monster,currentEncounter):
        rng=random.uniform(0,1)
        dmg=round(monster.weapon.damage-self.player.defense())
        if dmg<1:
            dmg=1
        critdmg=round((monster.weapon.damage*monster.weapon.critpower)-self.player.defense())
        if critdmg<1:
            critdmg=1
        if rng<=monster.weapon.critchance:
            printwithdelay(f"The {monster.name} performed a crit on you dealing {critdmg} damage!")
            self.player.takehit(critdmg)
            options={"attack":AttackEvent(self.player,monster,currentEncounter),"hit":AttackEvent(self.player,monster,currentEncounter)}
            self.player.choose(options)
        printwithdelay(f"The {monster.name} attacked you dealing {dmg} damage!")   
        self.player.takehit(dmg)
        options={"attack":AttackEvent(self.player,monster,currentEncounter),"hit":AttackEvent(self.player,monster,currentEncounter)}
        self.player.choose(options)
    def monsterItems(self,monster):
        rng=random.uniform(0,1)
        if rng>.5:
            return
        items=[monster.weapon,monster.helmet,monster.chestplate,monster.pants,monster.boots]
        reward=random.choice(items)
        self.player.pickup(reward)
    def monsterDeath(self,monster):
        printwithdelay(f"You have successfully slain the {monster.name}!")
        self.randomEncounterNumber-=1
        self.monsterItems(monster)
        printwithdelay("You come to find a door before you.")
        options={"go":EnterRoom(self.player,self.randomEncounterNumber),"proceed":EnterRoom(self.player,self.randomEncounterNumber),"enter":EnterRoom(self.player,self.randomEncounterNumber)}
        self.player.choose(options)
            
class Event:
    def __init__(self,player):
        self.player=player
    def encounterNumber(self,player):
        rng=random.uniform(1.2**player.currentfloor-2*1.03**-player.currentfloor,1.2**player.currentfloor+2*1.03**-player.currentfloor)
        if rng<1:
            rng=1
        miniEncounterNumber=round(rng)
        return miniEncounterNumber
    def run(self):
        return
class EntranceEvent(Event):
    def run(self):
        self.player.currentfloor+=1
        printwithdelay(f"You have entered floor {self.player.currentfloor}")
        self.miniEncounterNumber=self.encounterNumber(self.player)
        self.currentEncounter=Encounter(self.miniEncounterNumber,self.player)
        self.currentEncounter.beginEncounter(self.currentEncounter)
class EnterRoom(Event):
    def __init__(self,player,miniEncouterNumber):
        self.player=player
        self.miniEncounterNumber=miniEncouterNumber
    def run(self):
        if self.miniEncounterNumber==0:
            printwithdelay("Before you is a staircase that decends deeper into the dungeon.")
            options={"enter":EntranceEvent(self.player),"go":EntranceEvent(self.player),"proceed":EntranceEvent(self.player)}
            self.player.choose(options)
        self.currentEncounter=Encounter(self.miniEncounterNumber,self.player)
        self.currentEncounter.beginEncounter(self.currentEncounter)
        
class AttackEvent(Event):
    def __init__(self,player,monster,currentEncounter):
        self.player=player
        self.monster=monster
        self.currentEncounter=currentEncounter
    def run(self):
        rng=random.uniform(0,1)
        dmg=round(self.player.slots["mainhand"].damage-self.monster.defense())
        if dmg<1:
            dmg=1
        critdmg=round((self.player.slots["mainhand"].damage*self.player.slots["mainhand"].critpower)-self.monster.defense())
        if critdmg<1:
            critdmg=1
        if rng<=self.player.slots["mainhand"].critchance:
            printwithdelay(f"You preformed a crit on the {self.monster.name} dealing {critdmg} damage!")
            self.monster.takehit(critdmg,self.currentEncounter)
            printwithdelay(f"({self.monster.health}/{self.monster.maxhealth})")
            self.currentEncounter.enemyRetalite(self.monster,self.currentEncounter)
        printwithdelay(f"You attacked the {self.monster.name} dealing {dmg} damage!")    
        self.monster.takehit(dmg,self.currentEncounter)
        printwithdelay(f"({self.monster.health}/{self.monster.maxhealth})")
        self.currentEncounter.enemyRetalite(self.monster,self.currentEncounter)
        

class Enemy(Entity):
    def __init__(self,name,health,weapon,helmet,chestplate,pants,boots):
        self.health=health
        self.maxhealth=health
        self.name=name
        self.weapon=weapon
        self.helmet=helmet
        self.chestplate=chestplate
        self.pants=pants
        self.boots=boots
    def defense(self):
        defense=self.helmet.defense+self.chestplate.defense+self.pants.defense+self.boots.defense
        return defense
    def takehit(self,dmg,encounter):
        self.health-=dmg
        if self.health<=0:
            encounter.monsterDeath(self)
        
game=Game()
game.openingsequence()

