species = [
    'all', 'aardvark', 'aardwolf', 'baboon', 'bat', 'batearedfox', 'buffalo',
    'bushbuck', 'bushpig', 'caracal', 'cattle', 'cheetah', 'civet', 'dikdik',
    'duiker', 'eland', 'elephant', 'fire', 'gazellegrants', 'gazellethomsons',
    'genet', 'giraffe', 'guineafowl', 'hare', 'hartebeest', 'hippopotamus',
    'honeybadger', 'human', 'hyenabrown', 'hyenaspotted', 'hyenastriped',
    'impala', 'insectspider', 'jackal', 'koribustard', 'kudu', 'leopard',
    'lionfemale', 'lionmale', 'mongoose', 'monkeysamango', 'nyala', 'ostrich',
    'otherbird', 'porcupine',
'reedbuck',
'reptiles',
'rhinoceros',
'rodents',
'sable',
'secretarybird',
'serval',
'steenbok',
'topi',
'vervetmonkey',
'vulture',
'warthog',
'waterbuck',
'wildcat',
'wilddog',
'wildebeest',
'zebra',
'zorilla'
]

def species_choices():
    ss = []
    for s in species:
        ss.append((s,s))
    return ss

seasons = ['ALL', 'SER_S13', 'SER_S14', 'SER_S15', 'SER_S16']

def select_choices(choice_list):
    sc = []
    for choice in choice_list:
        sc.append((choice,choice))
    return sc
