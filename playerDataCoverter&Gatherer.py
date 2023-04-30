from nbt import nbt
import pandas as pd
import time

playerDataPath = "playerdata/9ccce49d-1bf7-401b-ba03-efdaa31a287a.dat"
levelDataPath = "level.dat"
statDataPath = 'stats/9ccce49d-1bf7-401b-ba03-efdaa31a287a.json'

nbtfile = nbt.NBTFile(levelDataPath) # goes to world folder, get level.dat, make NBT file.
intalTickTime = int(str(nbtfile["Data"]["Time"]))
## Note: time in game is not one to one to real world time. (20 Ticks is 1 second)
durationTime = 180000 ##collects data for an duration of time
intervalTime = 1304 ## intervals of time


realTickTime = intalTickTime + durationTime
tickTime = intalTickTime
currentTickTime=intalTickTime

##empty lists and dataframe
df = pd.DataFrame()
timeList = []
playerListPostionY = []
playerListPostionX = []
playerListPostionZ = []
playerHealthList = []
playerFoodLevelList = []
playerSaturationList = []
playerXpLevelList = []
playerDimensionList = []
playerSlotSelectedList = []

while tickTime < realTickTime:
    time.sleep(2) #delay so the game as a chance to write to the file.
    gameTime = nbt.NBTFile(levelDataPath)
    tickTime = int(str(gameTime["Data"]["Time"]))
    if tickTime >= currentTickTime:
        currentGameTime = nbt.NBTFile(levelDataPath)
        tick2Time = int(str(currentGameTime["Data"]["Time"]))
        currentTickTime=tick2Time+intervalTime

        #More player Data
        playerData = nbt.NBTFile(playerDataPath)
        playerPostionY = int(float(str(playerData["Pos"][1])))
        playerPostionX = int(float(str(playerData["Pos"][0])))
        playerPostionZ = int(float(str(playerData["Pos"][2])))
        playerHealth = int(float(str(playerData["Health"])))
        playerFoodLevel = int(float(str(playerData["foodLevel"])))
        playerSaturation = int(float(str(playerData["foodSaturationLevel"])))
        playerXpLevel = int(float(str(playerData["XpLevel"])))
        playerDimension = int(float(str(playerData["Dimension"])))
        playerSlotSelected = int(float(str(playerData["SelectedItemSlot"])))

        #list appending
        timeList.append(tick2Time)
        playerListPostionY.append(playerPostionY)
        playerListPostionX.append(playerPostionX)
        playerListPostionZ.append(playerPostionZ)
        playerHealthList.append(playerHealth)
        playerFoodLevelList.append(playerFoodLevel)
        playerSaturationList.append(playerSaturation)
        playerXpLevelList.append(playerXpLevel)
        playerDimensionList.append(playerDimension)
        playerSlotSelectedList.append(playerSlotSelected)

        df2 = pd.read_json(statDataPath, orient='index')
        df2 = df2.transpose()
        df = df.append(df2)

        print(timeList)
        print(playerListPostionY)
        print(playerListPostionX)
        print(playerListPostionZ)
        print(playerHealthList)
        print(playerFoodLevelList)
        print(playerSaturationList)
        print(playerXpLevelList)
        print(playerDimensionList)
        print(playerSlotSelectedList)

        print(df)

#adding the lists to the Dataframe
#could of add the lists to end of dataframe but it makes more sense have to actrual playerData atomen the front of it
df.insert(0 ,'worldTime', timeList )
df.insert(1 , 'playerPostionY', playerListPostionY)
df.insert(2 , 'playerPostionX', playerListPostionX)
df.insert(3 , 'playerPostionZ', playerListPostionZ)
df.insert(4 , 'playerHealth', playerHealthList)
df.insert(5 , 'playerFoodLevel', playerFoodLevelList)
df.insert(6 , 'playerSaturation', playerSaturationList)
df.insert(7 , 'playerXpLevel', playerXpLevelList)
df.insert(8 , 'playerDimension', playerDimensionList)
df.insert(9 , 'playerSlotSelected', playerSlotSelectedList)
print(df)
df.to_csv('stats/rawData1.csv')