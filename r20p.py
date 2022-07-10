import dataclasses
import json
from dataclasses import dataclass
from typing import List

from bs4 import BeautifulSoup

@dataclass
class Feat:
    name: str
    desc: str
    sourceName: str
    sourceType: str

@dataclass
class Spell:
    name: str
    spellLevel: str
    spellSchool: str
    castingTime: str
    range: str
    target: str
    components: str
    desc: str
    higherLevels: str
    
@dataclass
class Character:
    name: str
    feats: List[Feat]
    spells: List[Spell]
    
def get_feats(soup):
    feat_list = []
        
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
                    feat_list.append(Feat(name.text,
                                          desc.text,
                                          source_name.text,
                                          source_type.text))
    return feat_list

def get_spells(soup):
    spell_list = []
    
    spells = soup.find_all("div", {'class': 'spell'})
    
    for spell in spells:
        name = spell.find("span", {'class': 'spellname',
                                   'name': 'attr_spellname'})
        
        if name.text != "":
            level = spell.find("span", {'name': 'attr_spelllevel'})
            school = spell.find("span", {'name': 'attr_spellschool'})
            casting_time = spell.find("span", {'name': 'attr_spellcastingtime'})
            range = spell.find("span", {'name': 'attr_spellrange'})
            target = spell.find("span", {'name': 'attr_spelltarget'})
            components = spell.find("span", {'name': 'attr_spellcomp_materials'})
            desc = spell.find("span", {'name': 'attr_spelldescription'})
            higher_levels = spell.find("span", {'name': 'attr_spellathigherlevels'})
            
            
            spell_list.append(Spell(name.text,
                                    level.text,
                                    school.text,
                                    casting_time.text,
                                    range.text,
                                    target.text,
                                    components.text,
                                    desc.text,
                                    higher_levels.text))

    return spell_list

def get_name(soup):
    return soup.find("title").text

def build_character(soup):
    name = get_name(soup)
    feats = get_feats(soup)
    spells = get_spells(soup)
    
    return Character(name, feats, spells)

def main():
    with open("sheet.html") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        
    character = build_character(soup)
    
    print(json.dumps(dataclasses.asdict(character)))

if __name__ == '__main__':
    main()
                
        

