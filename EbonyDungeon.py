import random
import os.path
import time
import json
#Functions
def playerDataDecompress(file):
    saveFile=open(file,"r")
    savedata=json.loads(saveFile.read())
    saveFile.close()
    playerdata=(savedata["health"],savedata["maxhealth"],playerItemDataDecompress(savedata["items"]),savedata["money"],savedata["scrap"],savedata["currentfloor"],playerSlotsDataDecompress(savedata["slots"]))
    return playerdata
def playerItemDataDecompress(itemData):
    itemTypes={"Items":Items,"Quantity":Quantity,"Melee":Melee,"Armor":Armor}
    decompressedItems=[]
    for item in itemData:
        decompressedItem=itemTypes[item["type"]](item["data"])
        decompressedItems.append(decompressedItem)
    return decompressedItems
def playerSlotsDataDecompress(slotsData):
    itemTypes={"Items":Items,"Quantity":Quantity,"Melee":Melee,"Armor":Armor}
    decompressedSlots={}
    for key in slotsData:
        decompressedItem=itemTypes[slotsData[key]["type"]](slotsData[key]["data"])
        decompressedSlots[key]=decompressedItem
    return decompressedSlots
def weightRandDict(dict):
    rng=random.uniform(0,1)
    previouschance=0
    for weight,output in dict:
        if previouschance<rng<weight+previouschance:
            return output
        previouschance=weight+previouschance
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
    def __init__(self,data):
        name,tooltip=data
        self.name=name
        self.tooltip=tooltip
    def printAttributes(self):
        printwithdelay("This item has no attributes")
    slot=None
    def compress(self):
        return {"type":"Items","data":(self.name,self.tooltip)}
class Quantity(Items):
    def __init__(self,data):
        name,tooltip,quantity,function,basevalue=data
        self.name=name
        self.tooltip=tooltip
        self.quantity=quantity
        self.function=function
        self.value=basevalue
        self.scrap=basevalue/3
    slot=None
    def compress(self):
        return {"type":"Quantity","data":(self.name,self.tooltip,self.quantity,self.function,self.value)}
    def printAttributes(self):
        printwithdelay(f"Quantity> {self.quantity}\nScrap Value (per {self.name})> {self.scrap}\nMoney Value (per {self.name})> {self.value}\n{self.tooltip}")
class Mainhand(Items):
    slot="mainhand"
class Melee(Mainhand):
    def __init__(self,data):
        name,damage,tooltip,critpower,critchance=data
        self.damage=damage
        self.name=name
        self.tooltip=tooltip
        self.critpower=critpower
        self.critchance=critchance
        self.scrap=round((damage**2)/25)
        self.value=round(((damage**2)/25)*3)
    def compress(self):
        return {"type":"Melee","data":(self.name,self.damage,self.tooltip,self.critpower,self.critchance)}
    def printAttributes(self):
        printwithdelay(f"Mainhand\nDamage> {self.damage}\nCrit Power> {self.critpower}\nCrit Chance> {self.critchance}\nScrap Value> {self.scrap}\nMoney Value> {self.value}\n{self.tooltip}")
class Armor(Items):
    def __init__(self,data):
        name,defense,tooltip=data
        self.defense=defense
        self.name=name
        self.tooltip=tooltip
        self.scrap=round(defense**2/25)
        self.value=round(((1.25**2)/25)*3)
    def compress(self):
        return {"type":"Armor","data":(self.name,self.defense,self.tooltip)}
    def printAttributes(self):
        printwithdelay(f"Defense> {self.defense}\nScrap Value> {self.scrap}\nMoney Value> {self.value}\n{self.tooltip}")
class Helmet(Armor):
    def printAttributes(self):
        printwithdelay(f"Helmet\nDefense> {self.defense}\nScrap Value> {self.scrap}\nMoney Value> {self.value}\n{self.tooltip}")
    slot="helmet"
class Chestplate(Armor):
    def printAttributes(self):
        printwithdelay(f"Chestplate\nDefense> {self.defense}\nScrap Value> {self.scrap}\nMoney Value> {self.value}\n{self.tooltip}")
    slot="chestplate"
class Pants(Armor):
    def printAttributes(self):
        printwithdelay(f"Pants\nDefense> {self.defense}\nScrap Value> {self.scrap}\nMoney Value> {self.value}\n{self.tooltip}")
    slot="pants"
class Boot(Armor):
    def printAttributes(self):
        printwithdelay(f"Boots\nDefense> {self.defense}\nScrap Value> {self.scrap}\nMoney Value> {self.value}\n{self.tooltip}")
    slot="boots"
class Player(Entity):
    def __init__(self,playerdata):
        health,maxhealth,items,money,scrap,currentfloor,slots=playerdata
        self.health=health
        self.maxhealth=maxhealth
        self.items=items
        self.money=money
        self.scrap=scrap
        self.currentfloor=currentfloor
        self.slots=slots
    def itemsCompress(self):
        newitems=[]
        for item in self.items:
            newitems.append(item.compress())
        return newitems
    def slotsCompress(self):
        newslots={}
        for key in self.slots:
            newslots[key]=self.slots[key].compress()
        return newslots
    def compress(self):
        return {"health":self.health,"maxhealth":self.maxhealth,"items":self.itemsCompress(),"money":self.money,"scrap":self.scrap,"currentfloor":self.currentfloor,"slots":self.slotsCompress()}
    def defense(self):
        defense=self.slots["helmet"].defense+self.slots["chestplate"].defense+self.slots["pants"].defense+self.slots["boots"].defense
        return defense
    def die(self):
        printwithdelay("You have died.")
        if os.path.exists("player_save_file.json") is False:
            quit()
        os.remove("player_save_file.json")
        quit()
    def choose(self,options,prompt):
        printwithdelay(prompt)
        choice=input("Actions >")
        if choice.lower() in ["stats","health","money","floor","scrap"]:
            printwithdelay(f"Health> {self.health}\nMax Health> {self.maxhealth}\nMoney> {self.money}\nCurrent Floor> {self.currentfloor}\nScrap> {self.scrap}")
            self.choose(options,prompt)
        elif choice.lower()in ["items","item","inventory"]:
            printwithdelay("Items:")
            for item in self.items:
                printwithdelay(item.name)
            printwithdelay(f"Equipped:\nMainhand> {self.slots['mainhand'].name}\nHelmet> {self.slots['helmet'].name}\nChestplate> {self.slots['chestplate'].name}\nPants> {self.slots['pants'].name}\nBoots> {self.slots['boots'].name}")
            self.InventoryMenu()
            self.choose(options,prompt)
        elif choice.lower() in options:
            event=options[choice.lower()]
            event.run()
        else:
            printwithdelay(f"{choice} is not a valid action")
            self.choose(options,prompt)
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
        if isinstance(item,Quantity) is True:
            self.pickupQuantity(item)
            return
        self.items.append(item)
        article=appropriatearticle(item.name)
        printwithdelay(f"You Picked up {article} {item.name}!")
    def pickupList(self,items):
        for item in items:
            self.pickup(item)
    def pickupQuantity(self,item):
        iteminlist=checkList(item.name,self.items)
        if iteminlist is None:
            self.items.append(item)
            printwithdelay(f"You picked up {item.quantity} {item.name}s")
            return
        iteminlist.quantity+=item.quantity
        printwithdelay(f"You picked up {item.quantity} {item.name}s")

    def pickupMoney(self,amount):
        amount=int(amount)
        if amount<=1:
            printwithdelay(f"You picked up a single coin!")
            self.money+=1
            return
        printwithdelay(f"You picked up {amount} coins!")
        self.money+=amount
    def pickupScrap(self,amount):
        amount=int(amount)
        if amount<=1:
            printwithdelay(f"You salvaged a single scrap!")
            self.scrap+=1
            return
        printwithdelay(f"You salvaged {amount} scrap!")
        self.scrap+=amount
                
            
class Game:
    def __init__(self):
        if os.path.isfile("player_save_file.json") is False:
            self.player=Player(playerDataDecompress("default_save_file.json"))
            return
        self.player=Player(playerDataDecompress("player_save_file.json"))
    def openingsequence(self):
        printwithdelay("Welcome to the Ebony Dungeon")
        printwithdelay("You can make choices to get further into the dungeon, but beware of the danger")
        self.__entrance()
    def __entrance(self):
        options={"enter":EntranceEvent(self.player),"go":EntranceEvent(self.player),"proceed":EntranceEvent(self.player)}
        self.player.choose(options,"You stand at the entrance to a deep dungeon")
        
class Encounter:
    def __init__(self,randomencounternumber,player):
        self.randomEncounterNumber=randomencounternumber
        self.player=player
class ShopEncounter(Encounter):
    def beginEncounter(self):
        self.randomEncounterNumber-=1
        self.player.choose({"go":EnterRoom(self.player,self.randomEncounterNumber),"proceed":EnterRoom(self.player,self.randomEncounterNumber),"talk":Shop(self.player),"shop":Shop(self.player)},"You stumble upon a humble merchant")
class MonsterEncounter(Encounter):
    def beginEncounter(self):
        currentMonster=self.createMeleeMonster(self.player)
        options={"attack":AttackEvent(self.player,currentMonster,self),"hit":AttackEvent(self.player,currentMonster,self)}
        self.player.choose(options,f"You stumble into a {currentMonster.name}({currentMonster.health}/{currentMonster.maxhealth})!")
    def enemyRetalite(self,monster):
        rng=random.uniform(0,1)
        dmg=round(monster.weapon.damage-self.player.defense())
        if dmg<1:
            dmg=1
        critdmg=round((monster.weapon.damage*monster.weapon.critpower)-self.player.defense())
        if critdmg<1:
            critdmg=1
        if rng<=monster.weapon.critchance:
            self.player.takehit(critdmg)
            options={"attack":AttackEvent(self.player,monster,self),"hit":AttackEvent(self.player,monster,self)}
            self.player.choose(options,f"The {monster.name} performed a crit on you dealing {critdmg} damage!")
        self.player.takehit(dmg)
        options={"attack":AttackEvent(self.player,monster,self),"hit":AttackEvent(self.player,monster,self)}
        self.player.choose(options,f"The {monster.name} attacked you dealing {dmg} damage!")
    def monsterLoot(self,monster):
        self.player.pickupMoney(25*1.03**self.player.currentfloor)
        self.player.pickupScrap(5*1.02**self.player.currentfloor)
        rng=random.uniform(0,1)
        if rng>.5:
            return
        items=[monster.weapon,monster.helmet,monster.chestplate,monster.pants,monster.boots]
        self.player.pickup(random.choice(items))
    def monsterDeath(self,monster):
        printwithdelay(f"You have successfully slain the {monster.name}!")
        self.randomEncounterNumber-=1
        self.monsterLoot(monster)
        options={"go":EnterRoom(self.player,self.randomEncounterNumber),"proceed":EnterRoom(self.player,self.randomEncounterNumber),"enter":EnterRoom(self.player,self.randomEncounterNumber)}
        self.player.choose(options,"You come to find a door before you.")
class MeleeEncounter(MonsterEncounter):
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
        monsters=["Goblin","Zombie","Ninja","Pirate","Henchman","Zombie Viking","Viking","Marauder","Zombie Pirate","Skeleton","Skeleton Ninja","Skeleton Pirate","Skeleton Viking"]
        items={"weapons":["Sword","Scimitar","Waraxe","Shortsword","Longsword","Dagger","Spear","Mace","Flail","Club","Bludgeon","Katana","Saber","Lance","Halberd"],
               "helmets":["Greathelm","Helmet","Viking Helmet","Knight Helmet","Visor"],
               "chestplates":["Breastplate","Chestplate","Vest","Overarmor","Shirt","Chestpiece","Shining Armor"],
               "pants":["Pantaloons","Knight Leggings","Greaves"],
               "boots":["Combat Boots","Leather Boots","Sandels"]}
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
                      Melee((monsterWeaponName,damage,monsterItemTooltip,critpower,critchance)),
                      Helmet((monsterHelmetName,defense,monsterItemTooltip)),
                      Chestplate((monsterChestplateName,defense,monsterItemTooltip)),
                      Pants((monsterPantsName,defense,monsterItemTooltip)),
                      Boot((monsterBootsName,defense,monsterItemTooltip)))
        return monster
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
class Shop(Event):
    def run(self):
        print("This isn't fully fleshed out get fucked")
class EntranceEvent(Event):
    def run(self):
        self.player.currentfloor+=1
        printwithdelay(f"You have entered floor {self.player.currentfloor}")
        self.miniEncounterNumber=self.encounterNumber(self.player)
        self.currentEncounter=weightRandDict([(.9,MeleeEncounter(self.miniEncounterNumber,self.player)),(.1,ShopEncounter(self.miniEncounterNumber,self.player))])
        self.currentEncounter.beginEncounter()
class EnterRoom(Event):
    def __init__(self,player,miniEncouterNumber):
        self.player=player
        self.miniEncounterNumber=miniEncouterNumber
    def run(self):
        if self.miniEncounterNumber==0:
            options={"enter":EntranceEvent(self.player),"go":EntranceEvent(self.player),"proceed":EntranceEvent(self.player),"save":SaveGame(self.player)}
            self.player.choose(options,"Before you is a staircase that decends deeper into the dungeon. Before you descend, you may save.")
        self.currentEncounter=weightRandDict([(.9,MeleeEncounter(self.miniEncounterNumber,self.player)),(.1,ShopEncounter(self.miniEncounterNumber,self.player))])
        self.currentEncounter.beginEncounter()
        
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
            self.currentEncounter.enemyRetalite(self.monster)
        printwithdelay(f"You attacked the {self.monster.name} dealing {dmg} damage!")    
        self.monster.takehit(dmg,self.currentEncounter)
        printwithdelay(f"({self.monster.health}/{self.monster.maxhealth})")
        self.currentEncounter.enemyRetalite(self.monster)
class SaveGame(Event):
    def run(self):
        save_file=open("player_save_file.json","w")
        json.dump(self.player.compress(),save_file,indent=0)
        save_file.close()
        printwithdelay("Save Successful!")
        self.player.choose({"enter":EntranceEvent(self.player),"go":EntranceEvent(self.player),"proceed":EntranceEvent(self.player)},"Before you is a staircase that decends deeper into the dungeon.")

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

