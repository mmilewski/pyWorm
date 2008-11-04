#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Moduł parsujący zawartość pliku skryptowego opisującego poziom.
'''

import re
import os.path

class LevelScriptParser(object):

    def __init__(self, spriteName):
#         self.__filename = os.path.join('..','gfx',spriteName,'script.sprite')
        self.__filename = os.path.join(spriteName)
        self.__fileContent = self.__read_file_contents()


    def __read_file_contents(self):
        ''' Wczytuje zawartość pliku. '''
        try:
            f = open(self.__filename,'rU')
            self.__fileContent = f.readlines()     # wczytaj cały plik
            f.close()
        except:
            print "ERROR: nieznaleziono pliku sprite\'a lub plik jest uszkodzony:", self.__filename
#            raise "" ???
        return self.__fileContent


    def __parse_definitions(self, definitions):
        print "__parse_definitions: funkcja nie jest skończona"
#         print "\nDEFINICJE:\n", definitions
#         reTable,commentStr = self.__create_regex_table()
#         reDefinition = re.compile( reTable['definitionArgs'] )
#         for definition in definitions:
#             m = reDefinition.match( definition )
#             if not m: print "definition NOT MATCHED"
        
        return True


    def __parse_creations(self, creations):
        print "__parse_creations: funkcja nie jest skończona"
#         print "\nKREACJE:", creations
#         reTable,commentStr = self.__create_regex_table()
#         reCreation = re.compile( reTable['creationArgs'] )
#         for creation in creations:
#             creation = creation.replace('\n','')
#             m = reCreation.match( creation )
#             if not m: print "creation NOT MATCHED"
        return True


    def parse(self):
        ''' Parsuje wczytane dane. '''
        if not self.__fileContent:
            print "WARNING: próba sparsowania pustej zawartości."
            return False

        reTable,commentStr = self.__create_regex_table()

        # przeczyszczenie danych (usunięcie komentarzy oraz pustych linii, strip)
        lines = self.__fileContent
        lines = map( lambda x: x.split(commentStr)[0], lines)   # usuń komentarze
        lines = filter( lambda x: not re.compile(reTable['emptyLine']).match(x), lines )
        lines = map( lambda x: x.strip(), lines)

        # wyłuaskanie definicji i kreacji
        joinedLines = '\n'.join(lines)
        definitions = re.compile( reTable['definition'], re.DOTALL ).findall( joinedLines )
        creations  = re.compile( reTable['creation'], re.DOTALL ).findall( joinedLines )

        # parsowanie definicji i kreacji oraz zwrócenie statusu operacji parsowania
        b1 = self.__parse_definitions( definitions )
        b2 = self.__parse_creations( creations )
        return (b1 and b2)


    def __create_regex_table(self):
        ''' definicja lini w pliku (jako wyrażenia regularne) '''
        commentStr = '--'       # ciąg rozpoczynający komentarz
        rs = {
            'emptyLine'      : '\s*$',
            'comment'        : '\s*'+commentStr+'(.*?)$',
            'definition'     : '(\[.*?\])',
            'definitionArgs' : '\[\s*([\w\d\s\.]+)\s*:\s*((?:(?:"[\w\d\s\./:;\'_]*"|[\d]+)\s*,\s*)+)\s*\]', # [nazwa: argument,*]
            'creation'       : '({.*?})',
            'creationArgs'   : '\{\s*([\w\d\s\.]+)\s*:\s*((?:(?:"[\w\d\s\./:;\'_]*"|[\d]+)\s*,\s*)+)\s*\}', # {nazwa: argument,*}
            }

        return (rs, commentStr)

