import dataclasses
import json
from dataclasses import dataclass
from typing import List

from bs4 import BeautifulSoup

@dataclass
class Feat:
    name: str
    desc: str
    source_name: str
    source_type: str
    
@dataclass
class Feats:
    feats: List[Feat]

@dataclass
class Spell:
    name: str
    
@dataclass
class Spells:
    spells: List[Spell]

@dataclass
class Character:
    feats: Feats
    spells: Spells
    
def get_feats():
    feat_list = Feats([])
    
    with open("sheet.html") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        
    repitems = soup.find_all("div", class_="repitem")

    for repitem in repitems:
        display_blocks = repitem.find_all("div", {'class': 'display'})
        for block in display_blocks:
            name = block.find("span", {'class': 'title',
                                       'name': 'attr_name'})
            
            desc = block.find("span", {'class': 'desc',
                                       'name': 'attr_description'})
            
            source = block.find("span", {'class': 'subheader'})
            if source:
                source_name = source.find("span", {'name': 'attr_source'})
                source_type = source.find("span", {'name': 'attr_source_type'})
            
                feat_attrs = [name, desc, source_name, source_type]
                
                if all(x is not None for x in feat_attrs):
                    feat_list.feats.append(Feat(name.text,
                                                desc.text,
                                                source_name.text,
                                                source_type.text))
    return feat_list

def get_spells():
    spell_list = Spells([])
    
    with open("sheet.html") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        
    spells = soup.find_all("div", {'class': 'spell'})
    
    for spell in spells:
        name = spell.find("span", {'class': 'spellname',
                                   'name': 'attr_spellname'})
        
        if name.text != "":
            spell_list.spells.append(Spell(name.text))

    return spell_list

def main():
    feats = get_feats()
    spells = get_spells()
    
    character = Character(feats, spells)
    
    print(json.dumps(dataclasses.asdict(character)))

if __name__ == '__main__':
    main()
                
        

