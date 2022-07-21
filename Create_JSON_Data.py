import pandas as pd
from collections import OrderedDict
import json

'''
#df = pd.read_excel('VermintideEnemyStats.xlsx')#, sheet_name='Sheet')
print(df)
json_dict = df.to_json(orient='table') # orient='records', lines=True
#print(df.values.tolist())

#json_dict = df.values.tolist()
print(json_dict)

#json_dict = {"Name":"blub","Values":[{"ID":1},{"ID":2}]}
json_str = json.dumps(json_dict,indent=2)
print(json_str)

#Write to file:
with open("EnemyData.json", "w") as f: #, encoding="utf-8"
    f.write(json_dict)
'''

'''
test = "Hallo, ich bin ein Teststring! _|_ Bitte ignoriere mich!"
test = test.replace('_|_',"Blub Yeah!")
print(test)
'''


df = pd.read_excel('VermintideHeroStats.xlsx')#, sheet_name='Sheet')
print(df)

currenthero = None
currentweapon = None
dictionary = "["
weapondictionary = ""
attackdictionary = ""
for index, row in df.iterrows():
    if currenthero == None or currenthero != row['hero']:
        currenthero =  row['hero']
        weapondictionary = weapondictionary.replace('_|_',attackdictionary)
        dictionary = dictionary.replace('_|_',weapondictionary)
        attackdictionary = ""
        weapondictionary = ""
        dictionary += '{ "name":'+'"'+row['hero']+'"'+','+'"weapons": [' + ' _|_ ' + '] },'

    if weapondictionary != "" and weapondictionary[-1] != ",":
        weapondictionary += ','

    if currentweapon == None or currentweapon != row['weapon']:
        currentweapon = row['weapon']
        weapondictionary = weapondictionary.replace('_|_', attackdictionary)
        attackdictionary = ""
        weapondictionary += '{ "name":'+'"'+row['weapon']+'"'+','+'"attacks": [' + ' _|_ ' + '] },'

    if attackdictionary != "" and attackdictionary[-1] != "," :
        attackdictionary += ','
    attackdictionary += '{ "name":' +'"'+ row['attack']+'"'+ ',' + '"values":'
    attackdictionary += json.dumps([{'damage':row['damage'],'armordamage':row['armordamage'],'cleave':row['cleave'],'stagger':row['stagger'],'speed':row['speed'],'ranged':row['ranged']}])#+"\n"
    attackdictionary += '}'
    #print(json.dumps([{"damage":row['damage']},{"armordamage":row['armordamage']},{"cleave":row['cleave']},{"stagger":row['stagger']},{"speed":row['speed']}]))

weapondictionary = weapondictionary.replace('_|_', attackdictionary)
dictionary = dictionary.replace('_|_', weapondictionary)
dictionary += ']'

print(dictionary)

#json_dict = df.to_json(orient='table') # orient='records', lines=True
#json_str = json.dumps(json_dict,indent=2)

json_str = json.dumps(dictionary,indent=2)

with open("HeroData.json", "w") as f: #, encoding="utf-8"
    json.dump(json_str,f, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=2, separators=None)
