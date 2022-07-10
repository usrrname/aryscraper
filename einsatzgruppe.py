
import os
from util import save_as_json
from folder_utils import find_corresponding_folder
from names import men
from wiki import get_wikidata, create_name_filename_map, get_wiki_info
from uuid import uuid4

einsatzgruppen_1939 = {
    # 'description': 'The first eight Einsatzgruppen of WWII were formed to aid the invasion of Poland on 1 September 1939. The Einsatzgruppen were paramilitary mobile killing squads that operated under the administration of the Schutzstaffel (SS), They were made up of Gestapo , Kripo and SD officials, deployed during Operation Tannenberg and the Intelligencektion until the spring of 1940; followed by the German AB-Aktion which ended at the end of 1940. Long before the attack on Poland, the Nazis, aided by the German minority living in the Second Polish Republic, drew up a list of Polish personalities containing the names of 61 000 members of the Polish elite. The list, printed in a 192-page book, is titled Sonderfahndungsbuch Polen. It is composed only of names and dates of birth of politicians, scholars, actors, intelligentsia, doctors, lawyers, nobility, priests, officers and many other people, put available for Einsatzgruppen and Volksdeutscher Selbstschutz. At the end of 1939, 50,000 Poles and Jews were murdered by these groups in the annexed territories, including more than 1,000 prisoners of war. The Einsatzgruppen performed murders with the support of the Volksdeutscher Selbstschutz, a paramilitary group consisting of ethnic Germans living in Poland.',
    'Chief of Security Police and SD, or CSSD': {
        'Leaders': {
            'Reinhard Heydrich': 'SS-Obergruppenführer und General der Polizei',
            'Heinrich Himmler': 'Reichsführer-SS',
            'Ernst Kaltenbrunner': 'SS-Obergruppenführer',
        }
    },
    'Einsatzgruppe I - Wien (14th Army)': {
        'Commander': {
            'Bruno Streckenbach': 'SS-Standartenführer',
        },
        'Einsatzkommando 1/I': {
            'Ludwig Hahn': 'SS-Sturmbannführer',
            'Heinrich Fehlis': 'SS-Sturmbannführer',
        },
        'Einsatzkommando 2/I': {
            'Bruno Müller': 'SS-Sturmbannführer'
        },
        'Einsatzkommando 3/I': {
            'Alfred Hasselberg': 'SS-Sturmbannführer',
            'Martin Weiss': 'SS-Hauptscharführer',
            'Helmut Rauca': 'Deputy to Joachim Hamann'
        },
        'Einsatzkommando 4/I': {
            'Karl Brunner': 'SS-Sturmbannführer'
        }
    },
    'Einsatzgruppe II – Oppeln (10th Army)': {
        'Commander': {
            'Emanuel Schäfer': 'SS-Obersturmbannführer',
        },
        'Einsatzkommando 1/II': {
            'Otto Sens': 'SS-Obersturmbannführer'
        },
        'Einsatzkommando 2/II': {
            'Karl-Heinz Rux': 'SS-Sturmbannführer'
        },
    },
    'Einsatzgruppe III – Breslau (8th Army)': {
        'Commander': {
            'Hans Fischer': 'SS-Obersturmbannführer',
            'Gustav Adolf Scheel': 'SS-Brigadeführer, Gauleiter of Salzburg, HSSPF Alpenland',
        },
        'Einsatzkommando 1/III': {
            'Wilhelm Scharpwinkel': 'SS-Sturmbannführer, Oberregierungsrat'
        },
        'Einsatzkommando 2/III': {
            'Fritz Liphardt': 'SS-Sturmbannführer'
        },
    },
    'Einsatzgruppe IV – Dramburg (4th Army)': {
        'Commander': {
            'Lothar Beutel': 'SS-Brigadeführer',
            'Josef Albert Meisinger': 'Standartenführer'
        },
        'Einsatzkommando 1/IV': {
            'Helmut Bischoff': 'SS-Sturmbannführer'
        },
        'Einsatzkommando 2/IV': {
            'Walter Hammer': 'SS-Sturmbannführer'
        },
    },
    'Einsatzgruppe V – Allenstein (3rd Army)': {
        'Commander': {
            'Ernst Damzog': 'SS-Standartenführer',
            'Hans Ehlich': 'SS-Standartenführer, Chief of the Amt III B "Volkstum und Gesundheit“ (ethnicity and health)'
        },
        'Einsatzkommando 1/V': {
            'Heinz Gräfe': 'SS-Sturmbannführer'
        },
        'Einsatzkommando 2/V': {
            'Robert Schefe': 'SS-Sturmbannführer, Regierungsrat (Bureau Secretary)'
        },
        'Einsatzkommando 3/V': {
            'Walter Albath': 'SS-Sturmbannführer'
        }
    },
    'Einsatzgruppe VI (Wielkopolska area)': {
        'Commander': {
            'Erich Naumann': 'SS-Oberführer',
        },
        'Einsatzkommando 1/VI': {
            'Franz Sommer': 'SS-Sturmbannführer'
        },
        'Einsatzkommando 2/VI': {
            'Gerhard Flesch': 'SS-Sturmbannführer',
            'Emil Haussmann': 'SS functionary'
        },
    },
    'Einsatzgruppe z.B.V. (Upper Silesia and Cieszyn Silesia areas)': {
        'Commander': {
            'Udo von Woyrsch': 'SS-Obergruppenführer (1939)',
            'Otto Rasch': 'SS-Oberführer',
            'Karl Eberhard Schöngarth': 'SS-Oberführer (1941)',
        },
        'Sub-unit 1': {
            'Otto Hellwig': 'SS-Obersturmbannführer',
        },
        'Sub-unit 2': {
            'Hans Trummler': 'SS-Standartenführer'
        },
    },
    'Einsatzkommando 16 – Danzig (Pomorze area)': {
        'Commander': {
            'Rudolf Tröger': 'SS-Sturmbannführer',
            'Horst Eichler': 'Kriminalkommissar und SS-Hauptsturmführer, Deputy'
        },
        'Gdynia Unit': {
            'Friedrich Class': 'SS-Hauptsturmführer'
        },
        'Toruń Unit': {
            'Hans-Joachim Leyer': 'SS-Sturmbannführer, Kriminalkommissar'
        },
        'Bydgoszcz Unit': {
            'Jakob Lölgen': 'Kriminalrat',
        }
    }
}


einsatzgruppen_1941 = {
    'Chief of Security Police and SD, or CSSD': {
        'Leaders': {
            'Reinhard Heydrich': 'SS-Obergruppenführer und General der Polizei (1939–42)',
            'Erich von dem Bach-Zelewski': 'SS Supreme Commander, Central Russia',
            'Ernst Kaltenbrunner': 'SS-Obergruppenführer und General der Polizei (1943–45)',
        }
    },
    'Einsatzgruppe A (Army Group North – Baltic States)': {
        # 'established': 'June 1941',
        # 'disbanded': 'Oct. 1944',
        # 'locations': 'Estonia, Latvia, Lithuania, between their easten borders and Leningrad',
        # 'description': 'Einsatzgruppe A-attached to Army Group North-was formed at Gumbinnen, East Prussia on 23 June 1941. Stahlecker – its first commander – deployed the unit towards the Lithuanian border. His group consisted of 340 men from the Waffen SS, 89 from the Gestapo, 35 from the SD, 133 from the Orpo and 41 from the Kripo. When the Soviet troops withdrew from the temporary Lithuanian capital Kaunas, the city was retaken the next day by the Lithuanians during the anti-Soviet uprising.',
        'Commander': {
            'Franz Walter Stahlecker': 'SS-Brigadeführer und Generalmajor der Polizei (1941–42)',
            'Heinz Jost': 'SS-Brigadeführer und Generalmajor der Polizei (1942)',
            'Humbert Achamer-Pifrader': "SS-Oberführer und Oberst der Polizei (1942–43)",
            'Friedrich Panzinger': 'SS-Oberführer (1943–44)',
            'Wilhelm Fuchs': 'SS-Oberführer und Oberst der Polizei (1944)'
        },
        'Sonderkommando 1a': {
            'Martin Sandberger': 'SS-Obersturmbannführer (June 1941–1943)',
            'Bernhard Baatz': 'SS-Obersturmbannführer (1 August 1943–15 October 1944)'
        },
        'Sonderkommando 1b': {
            'Erich Ehrlinger': 'SS-Oberführer und Oberst der Polizei (1941)',
            'Walter Hoffmann': 'Deputy Commander SS-Sturmbannführer (1942)',
            'Eduard Strauch': 'SS-Obersturmbannführer (1942)',
            'Erich Isselhorst': 'SS-Sturmbannführer (1943)'
        },
        'Einsatzkommando 1a': {
            'Martin Sandberger': 'SS-Obersturmbannführer (1942)',
            'Karl Tschierschky': 'SS-Obersturmbannführer (1942)',
            'Erich Isselhorst': 'SS-Sturmbannführer (1942–43)',
            'Bernhard Baatz': 'SS-Obersturmbannführer (1943)'
        },
        'Einsatzkommando 1b': {
            'Hermann Hubig': 'SS-Sturmbannführer (1942)',
            'Manfred Pechau': 'SS-Sturmbannführer (1942)',
        },
        'Einsatzkommando 1c:': {
            'Kurt Graaf': 'SS-Sturmbannführer (1942)',
        },
        'Einsatzkommando 2': {
            'Rudolf Batz':  'SS-Obersturmbannführer (1941)',
            'Eduard Strauch': 'SS-Obersturmbannführer (1941)',
            'Rudolf Lange': 'SS-Sturmbannführer (1941–44)',
            'Manfred Pechau': 'SS-Sturmbannführer (1942)',
            'Reinhard Breder': 'SS-Sturmbannführer (1943)',
            'Oswald Poche': 'SS-Obersturmbannführer (1943–44)',
            'Wolfgang Kügler': 'SS-Untersturmführer, Teilkommandoführer (detachment leader)'
        },
        'Einsatzkommando 3': {
            'Karl Jäger': 'SS-Standartenführer (1941–1943)',
            'Wilhelm Fuchs': 'SS-Oberführer und Oberst der Polizei (1943–44)',
            'Hans-Joachim Böhme': 'SS-Sturmbannführer (1944-45)',
            'Joachim Hamann': 'SS-Obersturmführer, Leader of Rollkommando Hamann (1941)',
            'Rudolf Neugebauer': 'SS-Obersturmführer and Leader of Vilnius Gestapo (1942-43)'
        },
        'Einsatzkommando Tilsit': {
            'Hans-Joachim Böhme': 'SS-Sturmbannführer (1941)',
        },
        'Einsatzkommando zur besonderen Verwendung': {
            'Commander': {
                'Karl Eberhard Schöngarth': 'SS- Brigadierführer (1941)',
            },
            'Einsatzkommando Galizien': {
                'Walter Kutschmann': 'SS-Hauptsturmführer (1941)',
                'Hans Krueger': 'SS-Hauptsturmführer, Regional Commander KdS east Galicia',
                'Kurt Stawizki': 'SS-Sturmbannführer',
                'Felix Landau': 'SS-Hauptscharführer',
                'Wilhelm Rosenbaum': 'Logistics, Commandant of the Sipo-SD School',
                'Pieter Mentens': 'SS-Scharführer und Sonderführer',
                'Horst Waldenburger': 'SS-Scharführer'
            },
        },
        'Arajs Kommando': {
            'Viktors Arājs': 'SS-Sturmbannführer (1941-44)',
            'Herberts Cukurs': 'Hauptmann, Deputy Commander',
            'Konrāds Kalējs': 'SS-Sturmbannführer (1942-43)',
        }
    },
    'Einsatzgruppe B (Army Group Centre – Eastern Poland)': {
        # 'established': 'Jun. 1941',
        # 'disbanded': 'Aug. 1944',
        # 'locations': 'Warsaw, Belarus, Smolensk, Velikiye Luki, Kalinin, Orsha, Gomel, Chernigov, Orel, Kursk',
        # 'description': 'Einsatzgruppe B followed Army Group Center as it advanced into Soviet territory, starting from Warsaw and fanning out across Belarus toward Minsk and Smolensk. It conducted mass killings of Jews in the area controlled by Army Group Center (Rear) as well as in areas closer to the front. Sonderkommando 7a led by Walter Blume, was attached to the 9th Army under General Adolf Strauß. The Sonderkommando was active in Brest-Litovsk (see the Brześć Ghetto), Kobrin, Pruzhany, Slonim (the Słonim Ghetto), Baranovichi, Stowbtsy, Minsk (the Minsk Ghetto), Orsha, Klinzy, Briansk, Kursk, Tserigov, and Orel. ',
        'Commander': {
            'Arthur Nebe': 'SS-Gruppenführer und Generalmajor der Polizei (1941)',
            'Erich Naumann': 'SS-Brigadeführer und Generalmajor der Polizei (1941–43)',
            'Horst Böhme': 'SS-Standartenführer (1943)',
            'Erich Ehrlinger': 'SS-Oberführer und Oberst der Polizei (1943–44)',
            'Heinrich Seetzen': 'SS-Oberführer und Oberst der Polizei (1944)',
        },
        'Sonderkommando 7a': {
            'Walter Blume': 'SS-Standartenführer (1941)',
            'Eugene Steimle': 'SS-Standartenführer (1941)',
            'Kurt Matschke': 'SS-Hauptsturmführer (1941–42)',
            'Albert Rapp': 'SS-Obersturmbannführer (1942–43)',
            'Helmut Looss': 'SS-Sturmbannführer (1943–44)',
            'Gerhard Bast': 'SS-Sturmbannführer (1943–44)',
        },
        'Kommando Bialystok': {
            'Wolfgang Birkner': 'SS-Hauptsturmführer, Chief of the Kommando Bialystok'
        },
        'Kommando SS Zichenau-Schroettersburg': {
            'Hermann Schaper': 'SS-Obersturmführer'
        },
        'Sonderkommando 7b': {
            'Günther Rausch': 'SS-Sturmbannführer (1941–42)',
            'Adolf Ott': 'SS-Obersturmbannführer (1942–43)',
            'Josef Auinger': 'SS-Obersturmbannführer (1942–43)',
            'Karl-Georg Rabe': 'SS-Obersturmbannführer (1943–44)',
        },
        'Sonderkommando 7c': {
            'Friedrich-Wilhelm Bock': 'SS-Sturmbannführer (1942)',
            'Ernst Schmücker': 'SS-Hauptsturmführer (1942)',
            'Wilhelm Blühm': 'SS-Sturmbannführer (1942-43)',
            'Hans Eckhardt': 'SS-Sturmbannführer (1943)',
        },
        'Einsazkommanto 8': {
            'Otto Bradfisch': 'SS-Obersturmbannführer (1941–42)',
            'Heinz Richter': 'SS-Sturmbannführer (1942)',
            'Erich Isselhorst': 'SS-Sturmbannführer (1942)',
            'Hans Schindhelm': 'SS-Obersturmbannführe (1942–43)',
            'Alfred Rendörffer': 'SS-Sturmbannführer (1944)',
            'Josef Blösche': 'Rottenführer (Section Leader)',
        },
        'Einsatzkommando 9': {
            'Alfred Filbert': 'SS-Obersturmbannführer (1941)',
            'Oswald Schäfer': 'SS-Obersturmbannführer (1941–42)',
            'Wilhelm Wiebens': 'SS-Obersturmbannführer (1942–43)',
            'Friedrich Buchardt': 'SS-Obersturmbannführer (1943–44)',
            'Werner Kämpf': 'SS-Sturmbannführer (1943–44)'
        },
        'Vorkommando Moskau': {
            'Franz Six': 'SS-Brigadeführer (1941)',
            'Waldemar Klingelhöfer': 'SS-Obersturmbannführer (1941)',
            'Erich Körting': 'SS-Obersturmbannführer (1941)',
            'Friedrich Buchardt': 'SS-Sturmbannführer (1942)',
            'Friedrich-Wilhelm Bock': 'SS-Sturmbannführer (1942)',
            'Emil Augsburg': 'SS-Hauptsturmführer (1941–42)',
            'Bruno Sattler': 'Orderly Officer (1941-42)',
        }
    },
    'Einsatzgruppe C (Army Group South – Soviet Ukraine)': {
        # 'established': '1941',
        # 'disbanded': 'August 1943',
        # 'description': 'The Einzatzgruppe C, as a whole, was attached to the Army Group South. Its special task forces perpetrated mass killings across Ukraine',
        # 'locations': 'Kiev, Lviv, Babi Yar, Tarnopol (modern Ternopil, see the Tarnopol Ghetto), Kremenchug, Poltava, Sloviansk, Proskurov, Vinnytsia, Kramatorsk, Gorlovka and Rostov.',
        'Commander': {
            'Otto Rasch': 'SS-Gruppenführer und Generalmajor der Polizei (1941)',
            'Max Thomas': 'SS-Gruppenführer und Generalleutnant der Polizei (1941–43)',
            'Horst Böhme': 'SS-Standartenführer (1943–1944)',
            'Friedrich Jeckeln': 'SS-Obergruppenführer und General der Polizei (1943–44)',
        },
        'Einsatzkommando 4a': {
            'Paul Blobel': 'SS-Standartenführer (1941–42)',
            'Erwin Weinmann': 'SS-Obersturmbannführer (1942)',
            'Eugen Steimle': 'SS-Sturmbannführer (1942–43)',
            'Friedrich Schmidt': 'SS-Sturmbannführer (1943)',
            'Theodor Christensen': 'SS-Sturmbannführer (1943)',
            'Waldemar Von Radetzky': 'SS-Sturmbannführer, Deputy Chief',
        },
        'Einsatzkommando 4b': {
            'Günther Herrmann': 'SS-Obersturmbannführer (1941)',
            'Fritz Braune': 'SS-Obersturmbannführer (1941–42)',
            'Walter Hänsch': 'SS-Obersturmbannführer (1942)',
            'August Meier': 'SS-Obersturmbannführer (1942)',
            'Friedrich Suhr': 'SS-Sturmbannführer (1942–43)',
            'Waldemar Krause': 'SS-Sturmbannführer (1943–44)',
            'Lothar Fendler': 'SS-Sturmbannführer, Deputy Chief (1941–42)',
        },
        'Einsatzkommando 5': {
            'Erwin Schulz': 'SS-Oberführer (1941)',
            'August Meier': 'SS-Sturmbannführer (1941-42), Liason Officer'
        },
        'Einsatzkommando 6': {
            'Erhard Kroeger': 'SS-Standartenführer (1941)',
            'Robert Mohr': 'SS-Sturmbannführer (1941–42)',
            'Ernst Biberstein': 'SS-Obersturmbannführer (1942–1943)',
            'Friedrich Suhr': 'SS-Sturmbannführer (1943)',
            'Matthias Graf': 'SS-Untersturmführer',
        },
        'Einsatzkommando 1005': {
            'Paul Blobel': 'SS-Standartenführer (1942-44)',
        }
    },
    'Einsatzgruppe D (11th Army – Crimea)': {
        # 'description': 'Einsatzgruppe D, 600 troops initially, had its headquarters in Piatra-Neamt, Romania. Areas of operation were southern Ukraine, Crimea, Ciscaucasia. Dr. Otto Ohlendorf commanded Einsatzgruppe D. Himmler replaced him with SS-Brigadeführer und Generalmajor der Polizei dr. Walter Bierkamp. It was attached to the 11th Army.',
        # 'locations': 'Northern Transylvania, Cernauti, Kishinev, Ukraine, Crimea, Ciscaucasia.',
        'Commander': {
            'Otto Ohlendorf': 'SS-Gruppenführer und Generalleutnant der Polizei (1941–42)',
            'Walther Bierkamp': 'SS-Brigadeführer und Generalmajor der Polizei (1942–43)',
            'Willi Seibert': 'SS-Standartenführer, Deputy Chief'
        },
        'Adjutant': {
            'Heinz Schubert': 'SS-Obersturmbannführer, Adjutant to Otto Ohlendorf (1941)',
        },
        'Einsatzkommando 10a': {
            'Heinrich Seetzen': 'SS-Oberführer und Oberst der Polizei (1941–42)',
            'Kurt Christmann': 'SS-Sturmbannführer (1942–43)',
            'Helmut Oberlander': '‘Sonderführer’'
        },
        'Einsatzkommando 10b': {
            'Alois Persterer': 'SS-Obersturmbannführer (1941–42)',
            'Eduard Jedamzik': 'SS-Sturmbannführer',
        },
        'Einsatzkommando 11a': {
            'Paul Zapp': 'SS-Obersturmbannführer (1941–42)',
            'Fritz Mauer': 'SS-Sturmbannführer (1942)',
            'Gerhard Bast': 'SS-Sturmbannführer (1942)',
            'Werner Hersmann': 'SS-Sturmbannführer (1942–43)'
        },
        'Einsatzkommando 11b': {
            'Hans Unglaube': 'SS-Sturmbannführer (1941)',
            'Bruno Müller': 'SS-Obersturmbannführer (1941)',
            'Werner Braune': 'SS-Obersturmbannführer (1941–42)',
            'Paul Schultz': 'SS-Obersturmbannführer (1942–43)'
        },
        'Einsatzkommando 12': {
            'Gustav Adolf Nosske': 'SS-Obersturmbannführer (1941–42)',
            'Erich Müller': 'SS-Sturmbannführer (1942)',
            'Günther Herrmann': 'SS-Obersturmbannführer (1942–43)',
            'Emil Haussmann': 'SS-Sturmbannführer'
        },
    },
    'Einsatzgruppe E (12th Army – Croatia)': {
        # 'description': 'The Einsatzgruppe E was deployed in Croatia (i.e. in Yugoslavia) behind the 12th Army (Wehrmacht) in the area of Vinkovci (then Esseg), Sarajevo, Banja Luka, Knin, and Zagreb',
        # 'locations': 'Vinkovci (then Esseg), Sarajevo, Banja Luka, Knin, and Zagreb',
        'Commander': {
            'Ludwig Teichmann': 'SS-Obersturmbannführer (1941–43)',
            'Günther Herrmann': 'SS-Standartenführer (1943–44)',
            'Wilhelm Fuchs': 'SS-Oberführer und Oberst der Polizei (1944)'
        },
        'Einsatzkommando 10b': {
            'Joachim Deumling': 'SS-Obersturmbannführer und Oberregierungsrat (1943–45)',
            'Franz Sprinz': 'SS-Sturmbannführer (1945)'
        },
        'Einsatzkommando 11a': {
            'Rudolf Korndörfer': 'SS-Sturmbannführer und Regierungsrat (1943)',
            'Anton Fest': 'SS-Obersturmbannführer (1943–45)'
        },
        'Einsatzkommando 15': {
            'Willi Wolter': 'SS-Hauptsturmführer (1943–44)',
        },
        'Einsatzkommando 16': {
            'Johannes Thümmler': 'SS-Obersturmbannführer und Oberregierungsrat (1943)',
            'Joachim Freitag': 'SS-Obersturmbannführer (1943–44)'
        },
        'Einsatzkommando Agram': {
            'Rudolf Korndörfer': 'SS-Sturmbannführer und Regierungsrat (1943)',
        },
        'Einsatzkommando Tunis': {
            'Walter Rauff': 'SS-Standartenführer, Group Leader II D of RSHA'
        }
    },
    'Einsatzgruppe Serbien': {
        'Commander': {
            'Wilhelm Fuchs': 'SS-Oberführer und Oberst der Polizei (1941–42)',
            'Emanuel Schäfer': 'SS-Oberführer',
            'August Meyszner': 'SS-Gruppenführer und Generalleutnant of the Police',
        }
    },
    'Einsatzgruppe Norwegen': {
        'Commander': {
            'Franz Walter Stahlecker': 'SS-Oberführer (1940)',
            'Heinrich Fehlis': 'SS-Oberführer und Oberst der Polizei (1940-44)',
            'Fritz Weitzel': 'SS-Obergruppenführer (1904–1940)',
            'Wilhelm Rediess': 'SS-Obergruppenführer und General der Polizei (1900–1945)'
        },
    },
    'Einsatzgruppe H - Slovakia': {
        'Commander': {
            'Josef Witiska': 'SS-Standartenführer (1944)'
        }
    }
}

ignore_keys = ['established', 'disbanded', 'description', 'locations']

include_keys = ['Chief of Security Police and SD, or CSSD',
                'Commander', 'Adjutant']

include_group = ['kommando', 'unit', 'Commander']

folder_map = create_name_filename_map('./men')
# check if person obj with name exists


def get_all_names(obj):
    objectkeys = [key for key in obj.keys() if key not in ignore_keys]
    for group in objectkeys:
        for k, v in obj[group].items():
            if isinstance(v, dict):
                for k2, v2 in v.items():
                    yield k2, str(uuid4())


einsatz1 = set(name for name in get_all_names(einsatzgruppen_1939))
einsatz2 = set(name for name in get_all_names(einsatzgruppen_1941))


def find_role_and_unit(obj, name):
    objectkeys = [key for key in obj.keys() if key not in ignore_keys]
    role = ''
    for group in objectkeys:
        shortened_group_name = group.split(
            ' ')[0] + ' ' + group.split(' ')[1]

        for k, v in obj[group].items():

            if isinstance(v, dict):
                for k2, v2 in v.items():
                    if k2 == name:
                        if k == 'Commander' or k == 'Adjutant':
                            role = f'{k} of {shortened_group_name}'
                        else:
                            unit = f', {k}' if k not in include_keys else ''
                            role = f'{v2}' + unit
                        return {'role': role, 'group': shortened_group_name}


def create_data(nameset, obj, filename):
    people = []

    for name, uuid in nameset:
        folder_name = find_corresponding_folder(name, './men')
        person = {}
        person['name'], person['id'], person['wikiquery'] = name, uuid, folder_name

        if folder_name == None:
            print("Couldn't find corresponding folder for {name}")
            person['wikiquery'] = name.replace(' ', '_')

        role_unit = find_role_and_unit(obj, name)

        if role_unit != None:
            print("Found {role_unit} for {name}")
            person.update(role_unit)

        try:
            meta = get_wiki_info(folder_name, folder_map[folder_name])
            person.update(meta)
            print('Successfully added meta data for ' + name)
        except Exception as e:
            print(e)
            pass
        finally:
            print('Adding {name} to list')
            people.append(person)

        save_as_json(filename, people)
