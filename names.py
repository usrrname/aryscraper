import os
from util import get_names_from_csv
from folder_utils import get_names_in_folder

# Note: names are written in a way such they can be passed as a route into English or German wikipedia

# Assembled primary from https://commons.wikimedia.org/wiki/Category:Female_guards_in_Nazi_concentration_camps
# and female camp attendants in:
# https://commons.wikimedia.org/wiki/Category:Mug_shots_of_Holocaust_perpetrators,
# https://commons.wikimedia.org/wiki/Category:Belsen_trial_mugshots

female_guards = ['Alice Orlowski', 'Anna Hempel', 'Anneliese Kohlmann', 'Elisabeth Becker', 'Elisabeth Volkenrath', 'Ewa Paradies', 'Frieda Walter', 'Gerda Steinhoff', 'Gertrude Feist', 'Gertrude Saurer', 'Helene Kopper', 'Hermine Braunsteiner', 'Herta Bothe',
                 'Herta Oberheuser', 'Hertha Ehlert', 'Hilde Liesewitz', 'Hildegard Kanbach', 'Hildegard Lohbauer', 'Hildegard Neumann', 'Ilse Forste', 'Ilse Lothe', 'Irene Haschke', 'Irma Grese', 'Jenny-Wanda Barkmann', 'Juana Bormann', 'Maria Mandl', 'Therese Brandl', 'Wanda Klaff']

# Assembled from https://commons.wikimedia.org/wiki/Category:Mug_shots_of_Nazis

mugshots_of_nazis = ['August Heinrichsbauer', 'Albert Hartl', 'Arthur Nasse', 'Bernd von Brauchitsch', 'Bernhard Dietsche', 'Bernhard Schwarz', 'Bruno Grothe', 'Christoph Graf zu Stolberg-Stolberg', 'Erich Müller', 'Edwin Jung', 'Walter Letsch', 'Edward John Kerling', 'Emil Puhl', 'Erich Sparman', 'Erich Albrecht', 'Erich Darre', 'Erich Hahnenbruch', 'Erich Schroeder', 'Ernest Peter Burger', 'Ernst Buergin', 'Ernst John von Freyend', 'Ernst Korn', 'Ernst Lautz', 'Ernst Schaefer', 'Ernst Tesseraux', 'Erwin Brandt', 'Erwin von Lahousen', 'Fritz Schmelter', 'Franz Hupperschwiller', 'Franz Lenner', 'Franz Schlegelberger', 'Franz Xaver Schwarz', 'Frederich Kritzinger', 'Frederick Duquesne', 'Friedhelm Draeger', 'Friedrich Flick', 'Friedrich Jaehne', 'Friedrich Jeckeln', 'Fritz Bartels', 'Fritz Fischer', 'Fritz Gajewski', 'Fritz Grau', 'Fritz Meurer', 'Fritz Popp', 'Fritz Schwalm', 'George John Dasch', 'Gerhard Rose', 'Gregor Ebner', 'Guenther Tesch', 'Gustav Overbeck', 'Gustav von Halem', 'Günther Joel', 'Günther Nebelung', 'Heinz Scheurlen', 'Heinz Schmid-Loßberg', 'Hans Bavendamm', 'Hans Dieter Ellenbeck', 'Hans Hahl', 'Hans Johann Beck', 'Hans Kugler', 'Hans Mueller', 'Hans Petersen', 'Hans Werner Aufseß', 'Hans Zimmermann', 'Hans w Rinn', 'Harald Kuehnen', 'Heinrich Buscher', 'Heinrich Ebersberg', 'Heinrich Emmendorfer', 'Heinrich Gattineau', 'Heinrich Heinck', 'Heinrich Lohl', 'Heinrich Sellmer', 'Heinz Kaufmann', 'Helge Auleb', 'Helmut Johannsen', 'Helmuth Felmy', 'Herbert Hans Haupt', 'Herbert Huebner', 'Herbert Klemm', 'Herman Lang',
                     'Herman Otto Neubauer', 'Hermann Boehm', 'Hermann Cuhorst', 'Hermann Hartmann', 'Hermann Karoll', 'Hilar Giebel', 'Hor Wagner', 'Inge Viermetz', 'Jürgen von Klenck', 'Johannes Goebel', 'Joachim Entzian', 'Johann Gietler', 'Johannes Hermann Mueller', 'Josef Altmeyer', 'Max Jüttner', 'Karl-Heinz Bendt', 'Karl Lange', 'Karl Reinhardt (Politiker)', 'Karl Rühmer', 'Karl Leon Du Moulin-Eckart', 'Karl Donitz', 'Karl Hollidt', 'Karl Mummenthey', 'Karl Rasche', 'Karl Schroeder', 'Konrad Kaletsch', 'Konrad Meyer-Hetling', 'Konrad Radunski', 'Kurt Engert', 'Kurt Mayer', 'Kurt Schmidt-Klevenov', 'L Grauert', 'Leo Hepp', 'Leo Petri', 'Lippe Ernst Erbprinz zur', 'Lothar Fendler', 'Max Ilgner', 'Max Sollmann', 'Erwin Metzner', 'Michel Elmar', 'Paul Ohler', 'Oskar Welzl', 'Oskar Mueller', 'Oskars Dankers', 'Oswald Pohl', 'Oswald Rothaug', 'Otto Abs', 'Otto Schwarzenberger', 'Otto Ulm', 'Paul Zimmermann (SS-Mitglied)', 'Paul Bante', 'Paul Fehse', 'Paul Haefliger', 'Paul Pleiger', 'Paul Riege', 'Paul Scholz', 'Paulmann Werner', 'Philipp Heinrich Hoerlein', 'Reinhard Gehlen', 'Richard Hildebrandt', 'Richard Quirin', 'Rudolf Creutz', 'Rudolf Kerner', 'Rudolf Oeschey', 'Gustav Wilhelm Schübbe', 'Heinrich Schulz (assassin)', 'Stahl Friedrich', 'Uebelhack Friedrich', 'Ulrich Haberland', 'WP George John Dasch', 'Walter Laermann', 'Walter Staudinger', 'Kurt von Tippelskirch', 'Wolfgang Wirth', 'Werner von Hoven', 'Walter Duerrfeld', 'Walter Greiling', 'Walter Koehler', 'Walter Schellenberg', 'Walter Warlimont Detention Report', 'Werner Thiel', 'Wezel Emil', 'Wilhelm Bonatz', 'Wilhelm Rudolf Mann', 'Wilhelm von Ammon', 'Wilhelm von Ritter', 'Wilhem Keitel', 'Wilmar Hager', 'Wolfgang Mettgenberg']

# Assembled from https://commons.wikimedia.org/wiki/Category:Mug_shots_of_Holocaust_perpetrators

holocaust_perpetrators = ['Adam Ankenbrand', 'Adolf Ott', 'Adolf Pokorny', 'Adolf Theuer', 'Albert Fredrich Schwartz', 'Albert Kesselring', 'Albin Gretsch', 'Alfred Andreas Hofmann', 'Alfried Krupp von Bohlen und Halbach', 'Alice Orlowski', 'Ansgar Pichen', 'Anton Bergmeier', 'Arthur Andrae', 'Arthur Dietzsch', 'August Heinrich Bender', 'Werner Braune', 'Christof Knoll', 'Claus Schilling', 'Cornelius Schwanner', 'Edmund Veesenmayer', 'Eduard Lorenz', 'Eduard Strauch', 'Edwin Katzenellenbogen', 'Emil Buehring', 'Emil Haussmann', 'Emil Mahl', 'Emil Paul Pleissner', 'Erhard Brauny', 'Erich Dinges', 'Erich Muhsfeldt', 'Erich Zoddel', 'Ernst Biberstein', 'Ernst Girzick', 'Ernst Heinrich von Weizsäcker', 'Erwin Schulz', 'Erwin von Helmersen', 'Eugen Steimle', 'Fritz Schmelter', 'Felix Rühl', 'Feodor Fedorenko', 'Franz Hoessler', 'Franz Kraus', 'Franz Six', 'Franz Stofel', 'Franz Xaver Trenkle', 'Franz Zinecker', 'Fridolin Puhr', 'Frieda Walter', 'Friedrich Ruppert', 'Friedrich Wetzel', 'Friedrich Karl Wilhelm', 'Fritz Becher', 'Fritz Buntrock', 'Fritz Fischer', 'Fritz Hintermayer', 'Fritz Klein', 'Fritz ter Meer', 'Günther Pancke', 'Georg Schallermair', 'Georg König', 'Georg Rickhey', 'Georg Schnitzler', 'Georg Weltz', 'Gerhard Rose', 'Gertrude Feist', 'Gertrude Sauer', 'Guido Reimer', 'Gustav Heigel', 'Gustav Nosske', 'Günther Altenburg', 'Hans-Theodor Schmidt', 'Hans Eisele', 'Hans Lammers', 'Hans Hoffmann', 'Hans Kurt Eisele', 'Hans Merbach', 'Hans Möser', 'Hans Wolf', 'Hans Wolfgang Romberg', 'Heinrich Buetefisch', 'Heinrich Buuck', 'Heinrich Oster', 'Heinrich Schmidt', 'Heinz Detmers', 'Heinz Jost', 'Heinz Schubert', 'Helene Kopper', 'Helmut Poppendick', 'Helmut Roscher', 'Herbert Kappler', 'Herman Hackman', 'Herman Helbig', 'Hermann Becker Freyseng', 'Hermann Eberle', 'Hermann Grossmann', 'Hermann Krumey', 'Hermann Pister', 'Hermann Schmitz', 'Hilde Liesewitz', 'Hubert Krautwurst',
                          'Ignatz Schlomovicz', 'Joachim Mrugoswsky', 'Joachim Ribbentrop', 'Johana Borman', 'Johann Eichelsdoerfer', 'Johann Kick', 'Johann Kirsch', 'Johann Paul Kremer', 'Josef Fuchsloch', 'Josef Hirtreiter', 'Josef Kestel', 'Josef Kilian', 'Josef Leipold', 'Josef Remmele', 'Juana Bormann', 'Justus Beyer', 'Jürgen Stroop', 'Karl Genzken', 'Karl Ernst Möckel', 'Karl Frenzel', 'Karl Krauch', 'Karl von Roques', 'Konrad Schaefer', 'Josef Kramer', 'Kurt Blom', 'Kurt Heinrich', 'Leonhard Eichberger', 'Luise Danz 1947', 'Maria Mandel Krakow', 'Martin Gottfried Weiss', 'Martin Hellinger', 'Martin Sandberger', 'Martin Sandberger', 'Matthias Graf', 'Max Johann Marcus Schobert', 'Max Pauly', 'Michael Redwitz', 'Oskar Schmitz', 'Oskar Groning', 'Oskar Helbig', 'Oskar Schroeder', 'Otto Ambros', 'Otto Barnewald', 'Otto Bovensiepen', 'Otto Brinkmann', 'Otto Förschner', 'Otto Ohlendorf', 'Otto Ohlendorf', 'Otto Rasch', 'Otto Schulz', 'Otto Wolfgang Gunther Klaus', 'Peter Weingärtner', 'Paul Blobel', 'Paul Maischein', 'Paul Rostock', 'Peter Betz', 'Peter Merker', 'Philipp Grimm', 'Reiner Stahel', 'Richard Köhler', 'Richard Walenta', 'Rudolf Brandt', 'Rudolf Jacobi', 'Rudolf Suttrop', 'Schubert Heinz', 'Sebastian Schmid', 'Sepp Dietrich', 'Siegfried Handloser', 'Siegfried Ruff', 'Simon Wilhelm', 'Sylvester Filleboeck', 'Ulrich Greifelt', 'Viktor Brach', 'Vinzenz Schoettl', 'Vladislav Ostrovski', 'Waldemar Hoven', 'Waldemar Klingelhöfe', 'Waldemar von Radetzky', 'Walter Blume', 'Walter Buch', 'Walter Haensch', 'Walter Ulbricht', 'Walter Wendt', 'Werner Alfred Berger', 'Werner Greunuss', 'Wilhelm Altenloh', 'Wilhelm Beiglboeck', 'Wilhelm Dorr', 'Wilhelm Pfannenstiel', 'Wilhelm Wagner', 'Wilhelm Welter', 'Willi Seibert', 'Willi Tessmann', 'Willi Zwiener', 'Wolfgang Romberg']
# Assembled from https://commons.wikimedia.org/wiki/Category:Belsen_trial_mugshots
# Note: womens names removed and added to female_guards
belsen_trial_guards = ['Ansgar Pichen', 'Erich Zoddel', 'Franz Stofel', 'Franz Xaver Trenkle', 'Ignatz Schlomovicz',
                       'Josef Kramer', 'Oscar Schmitz', 'Peter Weingärtner', 'Vladislav Ostrovski', 'Wilhelm Dorr']

# Assembled from:
# https://en.wikipedia.org/wiki/List_of_SS_personnel
# https://commons.wikimedia.org/wiki/Category:Belsen_trial_mugshots
# https://commons.wikimedia.org/wiki/Category:Mug_shots_of_Holocaust_perpetrators
# Note: womens names removed and added to female_guards
men = ['Adam_Ankenbrand', 'Adam_Grünewald', 'Adolf_Diekmann', 'Adolf_Eichmann', 'Adolf_Hitler', 'Adolf_Katz_(SS-Mitglied)', 'Adolf_Ott_(SS-Mitglied)', 'Adolf_Pokorny', 'Adolf_Strauss_(general)', 'Adolf_Theuer', 'Adolf_von_Bomhard', 'Ain-Ervin_Mere', 'Albert_Forster', 'Albert_Fredrich_Schwartz', 'Albert_Hartl', 'Albert_Kesselring', 'Albert_Konrad_Gemmeker', 'Albert_Rapp', 'Albert_Speer', 'Albert_Widmann', 'Albin_Gretsch', 'Aleksander_Laak', 'Alexander_Mach', 'Alexander_Piorkowski', 'Alfons_Rebane', 'Alfred_Andreas_Hofmann', 'Alfred_Filbert', 'Alfred_Franke-Gricksch', 'Alfred_Naujocks', 'Alfred_Spilker', 'Alfred_Wünnenberg', 'Alfried_Krupp_von_Bohlen', 'Alois_Brunner', 'Alois_Persterer', 'Amon_Göth', 'Ansgar_Pichen', 'Ante_Pavelić', 'Anton_Bergmeier', 'Anton_Burger', 'Anton_Dunckern', 'Anton_Reinthaller', 'Anton_Thernes', 'Anton_Thumann', 'Arnold_Büscher', 'Arnold_Strippel', 'Arpad_Wigand', 'Arthur_Andrae', 'Arthur_Dietzsch', 'Arthur_Greiser', 'Arthur_Liebehenschel', 'Arthur_Mülverstedt', 'Arthur_Nasse', 'Arthur_Nebe', 'Arthur_Rödl', 'Arthur_Seyss-Inquart', 'Artur_Phleps', 'August_Becker', 'August_Blei', 'August_Bogusch', 'August_Frank', 'August_Heinrich_Bender', 'August_Heinrichsbauer', 'August_Heissmeyer', 'August_Hirt', 'August_Meysner', 'August_Miete', 'August_Schmidthuber', 'Auke_Bert_Pattist', 'Baldur_von_Schirach', 'Benno_Martin', 'Benno_von_Arent', 'Benson_Railton_Metcalf_Freeman', 'Bernd_Rosemeyer', 'Bernd_von_Brauchitsch', 'Bernhard_Baatz', 'Bernhard_Dietsche', 'Bernhard_Krüger', 'Bernhard_Schwarz', 'Bronislaw_Kaminski', 'Bruno_Beger', 'Bruno_Gesche', 'Bruno_Grothe', 'Bruno_Lohse', 'Bruno_Müller', 'Bruno_Sattler', 'Bruno_Streckenbach', 'Carl_Krauch', 'Carl_Oberg', 'Carl_Værnet', 'Christian_Frederik_von_Schalburg', 'Christian_Mergenthaler', 'Christian_Shnug', 'Christian_Wirth', 'Christof_Ludwig_Knoll', 'Christoph_Diehm', 'Christoph_Graf_zu_Stolberg-Stolberg', 'Claus_Schilling', 'Cornelius_Schwanner', 'Curt_von_Gottberg', 'Derk-Elsko_Bruins', 'Detlef_Nebbe', 'Edmund_Geer', 'Edmund_Veesenmayer', 'Eduard_Deisenhofer', 'Eduard_Jedamzik ', 'Eduard_Krebsbach', 'Eduard_Lorenz', 'Eduard_Paul_Tratz', 'Eduard_Roschmann', 'Eduard_Strauch', 'Eduard_Weiter', 'Eduard_Wirths', 'Edward_John_Kerling', 'Edwin_Jung', 'Edwin_Katzenellenbogen', 'Eggert_Reeder', 'Egon_Zill', 'Emanuel_Schafer', 'Emil_Augsburg', 'Emil_Bühring', 'Emil_Haussmann', 'Emil_Mahl', 'Emil_Maurice', 'Emil_Mazuw', 'Emil_Paul_Pleissner', 'Emil_Puhl', 'Emil_Sembach', 'Emil_Wezel', 'Enno_Lolling', 'Erhard_Brauny', 'Erhard_Kroeger', 'Eric_Muhsfeldt', 'Erich_Albrecht', 'Erich_Bauer', 'Erich_Darre', 'Erich_Deppner', 'Erich_Dinges', 'Erich_Ehrlinger', 'Erich_Engels_(SS-Mitglied)', 'Erich_Fuchs', 'Erich_Hahnenbruch', 'Erich_Isselhorst', 'Erich_Kempka', 'Erich_Klausener', 'Erich_Koch', 'Erich_Körting', 'Erich_Lachmann', 'Erich_Mix', 'Erich_Muhsfeldt', 'Erich_Müller', 'Erich_Naumann', 'Erich_Neumann', 'Erich_Priebke', 'Erich_Roth', 'Erich_Schroeder', 'Erich_Sparmann', 'Erich_Steidtmann', 'Erich_Zoddel', 'Erich_von_dem_Bach-Zelewski', 'Erich_von_der_Heyde', 'Ernest_Peter_Burger', 'Ernst-Robert_Grawitz', 'Ernst_August_Rode', 'Ernst_Barkmann', 'Ernst_Biberstein', 'Ernst_Boepple', 'Ernst_Bürgin', 'Ernst_Damzog', 'Ernst_Girzick', 'Ernst_Hartmann', 'Ernst_Heinrich_von_Weizsäcker', 'Ernst_Hermann_Himmler', 'Ernst_John_von_Freyend', 'Ernst_Kaltenbrunner', 'Ernst_Knorr', 'Ernst_Korn', 'Ernst_Lautz', 'Ernst_Leopold_Prinz_zur_Lippe', 'Ernst_Lerch', 'Ernst_Otto_Fick', 'Ernst_Schaefer', 'Ernst_Tesseraux', 'Ernst_Wilhelm_Bohle', 'Ernst_Woermann', 'Erwin_Brandt', 'Erwin_Lambert', 'Erwin_Metzner', 'Erwin_Rommel', 'Erwin_Rösener', 'Erwin_Schulz', 'Erwin_Weinmann', 'Erwin_von_Helmersen', 'Erwin_von_Lahousen', 'Eugen_Dollmann', 'Eugen_Steimle', 'Eugène_Vaulot', 'Felix_Landau', 'Felix_Rühl', 'Felix_Steiner', 'Feodor_Fedorenko', 'Ferdinand_Porsche', 'Ferdinand_von_Sammern-Frankenegg', 'Franz_Abromeit', 'Franz_Augsberger', 'Franz_Breithaupt', 'Franz_Hayler', 'Franz_Hössler', 'Franz_Josef_Huber', 'Franz_Joseph,_Prince_of_Hohenzollern-Emden', 'Franz_Karl_Reichleitner', 'Franz_Konrad_(SS officer)', 'Franz_Kraus', 'Franz_Kutschera', 'Franz_Lenner', 'Franz_Lucas', 'Franz_Murer', 'Franz_Rademacher', 'Franz_Reichleitner', 'Franz_Schädle', 'Franz_Schlegelberger', 'Franz_Schönhuber', 'Franz_Six', 'Franz_Sprinz', 'Franz_Stangl', 'Franz_Stofel', 'Franz_Suchomel', 'Franz_Viktor_Eirenschmalz', 'Franz_Walter_Stahlecker', 'Franz_Xaver_Schwarz', 'Franz_Xaver_Trenkle', 'Franz_Ziereis', 'Franz_Zinecker', 'Frederich_Kritzinger', 'Frederick_Duquesne', 'Fridolin_Glass', 'Fridolin_Puhr', 'Friedrich-Wilhelm_Bock', 'Friedrich-Wilhelm_Krüger', 'Friedrich_Alpers', 'Friedrich_Boßhammer', 'Friedrich_Buchardt', 'Friedrich_Entress', 'Friedrich_Flick', 'Friedrich_Franz,_Hereditary_Grand_Duke_of_Mecklenburg-Schwerin', 'Friedrich_Hildebrandt', 'Friedrich_Jaehne', 'Friedrich_Jeckeln', 'Friedrich_Panzinger', 'Friedrich_Peter', 'Friedrich_Ruppert', 'Friedrich_Schmidt_(Politiker,_1902)', 'Friedrich_Stahl', 'Friedrich_Suhr', 'Friedrich_Uebelhoer', 'Friedrich_Weber_(veterinarian)', 'Friedrich_Wetzel', 'Friedrich_Wilhelm', 'Fritz_Arlt', 'Fritz_Bartels', 'Fritz_Becher', 'Fritz_Braune', 'Fritz_Buntrock', 'Fritz_Darges', 'Fritz_Fischer', 'Fritz_Freitag', 'Fritz_Gajewski', 'Fritz_Grau', 'Fritz_Hartjenstein', 'Fritz_Henke', 'Fritz_Hintermayer', 'Fritz_Katzmann', 'Fritz_Klein', 'Fritz_Liphardt', 'Fritz_Meurer', 'Fritz_Neidholdt', 'Fritz_Popp', 'Fritz_Sauckel', 'Fritz_Schmelter', 'Fritz_Schmidt_(SS_officer)', 'Fritz_Schwalm', 'Fritz_Tittmann', 'Fritz_Weitzel', 'Fritz_Witt', 'Fritz_Wächtler', 'Fritz_ter_Meer', 'Fritz_von_Scholz', 'Gebhard_Ludwig_Himmler', 'Georg_August_Weltz', 'Georg_Keppler', 'Georg_Konrad_Morgen', 'Georg_Lörner', 'Georg_Rickhey', 'Georg_Ritter_von_Hengl', 'Georg_Schnitzler', 'Georg_Wilhelm_Müller', 'George_John_Dasch', 'George_Kettmann', 'Gerhard_Bast', 'Gerhard_Flesch', 'Gerhard_Klopfer', 'Gerhard_Palitzsch', 'Gerhard_Rose', 'Gottfried_Graf_von_Bismarck-Schönhausen', 'Gottlieb_Hering', 'Gottlob_Berger', 'Gregor_Ebner', 'Guenther_Tesch', 'Guido_Reimer', "Gunter_d'Alquen", 'Gustav_Abb', 'Gustav_Adolf_Nosske', 'Gustav_Adolf_Scheel', 'Gustav_Adolf_von_Wulffen', 'Gustav_Heigel', 'Gustav_Laabs', 'Gustav_Lombard', 'Gustav_Münzberger', 'Gustav_Nosske', 'Gustav_Overbeck', 'Gustav_Sorge', 'Gustav_Wagner', 'Gustav_Wilhelm_Schübbe', 'Gustav_von_Halem', 'Günther_Altenburg', 'Günther_Herrmann_(SS_commander)', 'Günther_Joel', 'Günther_Nebelung', 'Günther_Pancke', 'Günther_Schwägermann', 'Günther_Tamaschke', 'Hajo_Herrmann', 'Hanns_Albin_Rauter', 'Hanns_Bobermin', 'Hanns_Martin_Schleyer', 'Hans-Adolf_Prützmann', 'Hans-Georg_von_Charpentier', 'Hans-Joachim_Böhme_(SS-Mitglied)', 'Hans-Theodor_Schmidt', 'Hans-Ulrich_Geschke', 'Hans_Asperger', 'Hans_Aumeier', 'Hans_Baur', 'Hans_Bavendamm', 'Hans_Bothmann', 'Hans_Dieter_Ellenbeck', 'Hans_Dorr', 'Hans_Eisele_(physician)', 'Hans_F._K._Günther', 'Hans_Fischböck', 'Hans_Fleischhacker', 'Hans_Frank', 'Hans_Friedemann_Götze', 'Hans_Hahl', 'Hans_Haltermann', 'Hans_Hermann_Junge', 'Hans_Hinkel', 'Hans_Hoffmann', 'Hans_Hüttig', 'Hans_Jüttner', 'Hans_Kammler', 'Hans_Kehrl', 'Hans_Kraus', 'Hans_Krueger', 'Hans_Krüger', 'Hans_Kugler', 'Hans_Lammers', 'Hans_Lörner', 'Hans_Merbach', 'Hans_Mueller', 'Hans_Münch', 'Hans_Möser', 'Hans_Nieland', 'Hans_Petersen', 'Hans_Rinn_(Bankmanager)', 'Hans_Schindhelm', 'Hans_Sommer', 'Hans_Stark', 'Hans_Tidow', 'Hans_Trummler', 'Hans_Walter_Zech-Nenntwich', 'Hans_Werner_Aufseß', 'Hans_Wilhelm_König', 'Hans_Woellke', 'Hans_Wolf', 'Hans_Wolfgang_Romberg', 'Hans_Zimmermann', 'Harald_Kühnen', 'Harald_Nugiseks', 'Harald_Riipalu', 'Harold_Cole', 'Hartmann_Lauterbacher', 'Heinrich_Buetefisch', 'Heinrich_Buscher', 'Heinrich_Buuck', 'Heinrich_Bütefisch', 'Heinrich_Ebersberg', 'Heinrich_Emmendorfer', 'Heinrich_Fehlis', 'Heinrich_Freiherr_von_Stackelberg', 'Heinrich_Gattineau', 'Heinrich_Hamann_(Polizist)', 'Heinrich_Heim', 'Heinrich_Himmler', 'Heinrich_Lohl', 'Heinrich_Müller', 'Heinrich_Oster', 'Heinrich_Petersen', 'Heinrich_Petersen_(SS_officer)', 'Heinrich_Schmidt', 'Heinrich_Schulz_(assassin)', 'Heinrich_Schwarz', 'Heinrich_Seetzen', 'Heinrich_Sellmer', 'Heinrich_Worster', 'Heinz-Fritz_Müller', 'Heinz_Auerswald', 'Heinz_Barth', 'Heinz_Baumkötter', 'Heinz_Brücher', 'Heinz_Detmers', 'Heinz_Fanslau', 'Heinz_Felfe', 'Heinz_Gräfe', 'Heinz_Jost', 'Heinz_Kaufmann', 'Heinz_Lammerding', 'Heinz_Linge', 'Heinz_Linke', 'Heinz_Macher', 'Heinz_Reinefarth', 'Heinz_Scheurlen', 'Heinz_Schmid-Loßberg', 'Heinz_Schubert_(SS officer)', 'Heinz_Tensfeld', 'Helge_Auleb', 'Hellmuth Becker', 'Hellmuth_Felmy', 'Helmut_Bischoff', 'Helmut_Hugo_Glaser', 'Helmut_Johannsen', 'Helmut_Kunz', 'Helmut_Kämpfe', 'Helmut_Oberlander', 'Helmut_Poppendick', 'Helmut_Rauca', 'Helmut_Roscher', 'Helmut_Tanzmann', 'Helmuth_Friedrichs', 'Hendrik_Seyffardt', 'Henk_Feldmeijer', 'Henri_Fenet', 'Henri_Lafont', 'Herbert_Backe', 'Herbert_Böttcher', 'Herbert_Cukurs', 'Herbert_Floss', 'Herbert_Gille', 'Herbert_Hagen', 'Herbert_Hans_Haupt', 'Herbert_Huebner', 'Herbert_Jankuhn', 'Herbert_Kappler', 'Herbert_Klemm', 'Herbert_Lange', 'Herbert_Scherpe', 'Herbert_Wahler', 'Herman_Göring', 'Herman_Hackman', 'Herman_Helbig', 'Herman_Lang', 'Hermann_Abendroth', 'Hermann_Becker-Freyseng', 'Hermann_Boehm_(eugenicist)', 'Hermann_Cuhorst', 'Hermann_Eberle', 'Hermann_Fegelein', 'Hermann_Florstedt', 'Hermann_Gauch', 'Hermann_Grossmann', 'Hermann_Harm', 'Hermann_Hartmann', 'Hermann_Hubig', 'Hermann_Höfle',
       'Hermann_Karoli', 'Hermann_Krumey', 'Hermann_Maringgele', 'Hermann_Michel', 'Hermann_Muhs', 'Hermann_Pister', 'Hermann_Pook', 'Hermann_Prieß', 'Hermann_Schaper', 'Hermann_Schmitz', 'Hermann_Weiser', 'Hilar_Giebel', 'Hilmar_Wäckerle', 'Hinrich_Lohse', 'Hinrich_Schuldt', 'Hor_Wagner', 'Horst_Böhme_(SS_officer)', 'Horst_Fischer', 'Horst_Klein', 'Horst_Kopkow', 'Horst_Schumann', 'Hubert_Gomerski', 'Hubert_Klausner', 'Hubert_Krautwurst', 'Hubert_Meyer', 'Hugo-Heinz_Schmick', 'Hugo_Blaschke', 'Hugo_Jury', 'Hugo_Kraas', 'Hugo_von_Abercron', 'Humbert_Achamer-Pifrader', 'Hyacinth_Graf_Strachwitz', 'Ignatz_Schlomowicz', 'Inge_Viermetz', 'Ion_Antonescu', 'Irmfried_Eberl', 'Jakob_Grimminger', 'Jakob_Sporrenberg', 'Joachim_Albrecht_Eggeling', 'Joachim_Boosfeld', 'Joachim_Entzian', 'Joachim_Hamann', 'Joachim_Mrugoswsky', 'Joachim_Peiper', 'Joachim_Ribbentrop', 'Joachim_Rumohr', 'Joachim_von_Ribbentrop', 'Johann_Beck_(SS-Mitglied)', 'Johann_Eichelsdoerfer', 'Johann_Friedrich_Stöver', 'Johann_Gietler', 'Johann_Kantschuster', 'Johann_Kick', 'Johann_Kirsch', 'Johann_Klier', 'Johann_Niemann', 'Johann_Paul_Kremer', 'Johann_Rattenhuber', 'Johann_Schwarzhuber', 'Johann_von_Leers', 'Johannes_Hermann_Mueller', 'Johannes_Thümmler', 'Josef_Albert_Meisinger', 'Josef_Altmeyer', 'Josef_Altstötter', 'Josef_Auinger', 'Josef_Blösche', 'Josef_Bühler', 'Josef_Bürckel', 'Josef_Fitzthum', 'Josef_Fuchsloch', 'Josef_Hirtreiter', 'Josef_Kestel', 'Josef_Kieffer', 'Josef_Kollmer', 'Josef_Kramer', 'Josef_Leipold', 'Josef_Mengele', 'Josef_Oberhauser', 'Josef_Pospichil', 'Josef_Remmele', 'Josef_Riegler', 'Josef_Schillinger', 'Josef_Spacil', 'Josef_Tiso', 'Josef_Witiska', 'Joseph_Berchtold', 'Joseph_Darnand', 'Joseph_Klehr', 'Joseph_Kramer', 'Josias,_Hereditary_Prince_of_Waldeck_and_Pyrmont', 'Jozef_Kindel', 'Julian_Scherner', 'Julius_Dettmann', 'Julius_Schaub', 'Julius_Schreck', 'Julius_Streicher', 'Justus_Beyer', 'Jürgen_Stroop', 'Jürgen_Wagner', 'Jürgen_von_Klenck', 'Karl-Friedrich_Höcker', 'Karl-Gustav_Sauberzweig', 'Karl-Heinrich_Brenner', 'Karl-Heinz_Bendt', 'Karl-Heinz_Bürger', 'Karl-Heinz_Rux', 'Karl-Maria_Demelhuber', 'Karl_Babor', 'Karl_Brandt', 'Karl_Brunner_(SS general)', 'Karl_Bömelburg', 'Karl_Chmielewski', 'Karl_Diebitsch', 'Karl_Dönitz', 'Karl_Eberhard_Schöngarth', 'Karl_Ernst_Möckel', 'Karl_Fiehler', 'Karl_Freiherr_Michel_von_Tüßling', 'Karl_Frenzel', 'Karl_Fritzsch', 'Karl_Gebhardt', 'Karl_Genzken', 'Karl_Gesele', 'Karl_Gutenberger', 'Karl_Hanke', 'Karl_Hass', 'Karl_Hermann_Frank', 'Karl_Hollidt', 'Karl_Höfer', 'Karl_Jäger', 'Karl_Klaustermeyer', 'Karl_Kloskowski', 'Karl_Lange', 'Karl_Maria_Wiligut', 'Karl_Mummenthey', 'Karl_Peter_Berg', 'Karl_Pfeffer-Wildenbruch', 'Karl_Pflaumer', 'Karl_Pflomm', 'Karl_Rahm', 'Karl_Rasche', 'Karl_Reinhardt_(Politiker)', 'Karl_Rühmer', 'Karl_Schroeder', 'Karl_Silberbauer', 'Karl_Sommer_(SS-Mitglied)', 'Karl_Streibel', 'Karl_Ullrich', 'Karl_Wilhelm_Krause', 'Karl_Wolff', 'Karl_von_Eberstein', 'Karl_von_Roques', 'Karlis_Ozols', 'Klaus_Barbie', 'Knud_Børge_Martinsen', 'Konrad_Henlein', 'Konrad_Kaletsch', 'Konrad_Meyer-Hetling', 'Konrad_Radunski', 'Konrad_Schaefer', 'Konrad_Schellong', 'Konrāds_Kalējs ', 'Konstantin_von_Neurath', 'Kurt_Blom', 'Kurt_Bolender', 'Kurt_Christmann', 'Kurt_Daluege', 'Kurt_Engert', 'Kurt_Franz', 'Kurt_Gildisch', 'Kurt_Gruber', 'Kurt_Heinrich_(SS-Mitglied)', 'Kurt_Heissmeyer', 'Kurt_Lischka', 'Kurt_Mayer', 'Kurt_Meyer', 'Kurt_Schmidt-Klevenow', 'Kurt_Stawizki', 'Kurt_von_Tippelskirch', 'Leo_Hepp', 'Leo_Petri', 'Leo_Volk', 'Leonardo_Conti', 'Leonhard_Eichberger', 'Lorenz_Hackenholt', 'Lothar_Beutel', 'Lothar_Fendler', 'Ludolf_Jakob_von_Alvensleben', 'Ludolf_von_Alvensleben', 'Ludwig_Fischer', 'Ludwig_Grauert_(Staatssekretär)', 'Ludwig_Hahn', 'Ludwig_Heinemann', 'Ludwig_Kepplinger', 'Ludwig_Ruckdeschel', 'Ludwig_Steeg', 'Ludwig_Stumpfegger', 'Léon_Degrelle', 'Maria_Mandel_Krakow', 'Martin_Bormann', 'Martin_Gottfried_Weiss', 'Martin_Hellinger', 'Martin_James_Monti', 'Martin_Kohlroser', 'Martin_Sandberger', 'Martin_Sommer', 'Martin_Weiss_(Nazi_official)', 'Matthias_Graf', 'Matthias_Kleinheisterkamp', 'Max_Amann', 'Max_Clara', 'Max_Ilgner', 'Max_Jüttner', 'Max_Kiefer', 'Max_Koegel', 'Max_Pauly', 'Max_Schobert', 'Max_Seela', 'Max_Simon', 'Max_Sollmann', 'Max_Thomas', 'Max_Wielen', 'Max_de_Crinis', 'Maximilian_Grabner', 'Maximilian_List', 'Maximilian_von_Herff', 'Michael_Karkoc', 'Michael_Lippert', 'Michael_Redwitz', 'Michael_Wittmann', 'Michel_Elmar', 'Nikolaus_von_Falkenhorst', 'Odilo_Globocnik', 'Oscar_Hans', 'Oscar_Schmitz', 'Oskar_Dirlewanger', 'Oskar_Gröning', 'Oskar_Helbig', 'Oskar_Mueller', 'Oskar_Schroeder', 'Oskar_Welzl', 'Oskars_Dankers', 'Oswald_Pohl', 'Oswald_Rothaug', 'Oswald_Schäfer', 'Otto-Heinrich_Drechsler', 'Otto_Abetz', 'Otto_Abs', 'Otto_Ambros', 'Otto_Barnewald', 'Otto_Bovensiepen', 'Otto_Bradfisch', 'Otto_Brinkmann', 'Otto_Calliebe', 'Otto_Dietrich', 'Otto_Förschner', 'Otto_Günsche', 'Otto_Hellwig', 'Otto_Hofmann', 'Otto_Moll', 'Otto_Ohlendorf', 'Otto_Rasch', 'Otto_Schulz', 'Otto_Schwarzenberger', 'Otto_Skorzeny', 'Otto_Steinbrinck', 'Otto_Steinhäusl', 'Otto_Ulm', 'Otto_Wächter', 'Otto_von_Wächter', 'Paul-Werner_Hoppe', 'Paul_Bante', 'Paul_Blobel', 'Paul_Dickopf', 'Paul_Egger', 'Paul_Fehse', 'Paul_Haefliger', 'Paul_Hausser', 'Paul_Heigl', 'Paul_Hennicke', 'Paul_Hermann_Feustel', 'Paul_Maischein', 'Paul_Ohler', 'Paul_Otto_Geibel', 'Paul_Pleiger', 'Paul_Radomski', 'Paul_Riege', 'Paul_Rostock', 'Paul_Scharfe', 'Paul_Scholz', 'Paul_Schulz', 'Paul_Zapp', 'Paul_Zimmermann_(SS-Mitglied)', 'Paulmann_Werner', 'Perry_Broad', 'Peter_Betz', 'Peter_Högl', 'Peter_Kroeger', 'Peter_Merker', 'Peter_Weingärtner', 'Philipp_Bouhler', 'Philipp_Grimm', 'Philipp_Heinrich_Hoerlein', 'Philipp_Schmitt', 'Pierre_Paoli', 'Pieter_Menten', 'Pio_Filippani_Ronconi', 'Prince_Christoph_of_Hesse', 'Reimond_Tollenaere', 'Reiner_Stahel', 'Reinhard_Breder', 'Reinhard_Gehlen', 'Reinhard_Heydrich', 'Reinhold_Daum', 'Reinhold_Hanning', 'Richard_Baer', 'Richard_Glücks', 'Richard_Hildebrandt', 'Richard_Kaaserer', 'Richard_Korherr', 'Richard_Köhler', 'Richard_Nitsch', 'Richard_Quirin', 'Richard_Schulze-Kossens', 'Richard_Thomalla', 'Richard_Walenta', 'Richard_Walther_Darré', 'Richard_Wendler', 'Robert_Möhr', 'Rochus_Misch', 'Rolf_Czurda', 'Rolf_Engel', 'Rolf_Günther', 'Rudolf_August_Oetker', 'Rudolf_Batz', 'Rudolf_Beckmann', 'Rudolf_Brandt', 'Rudolf_Creutz', 'Rudolf_Diels', 'Rudolf_Hess', 'Rudolf_Höß', 'Rudolf_Jacobi', 'Rudolf_Kerner', 'Rudolf_Korndörfer', 'Rudolf_Lange', 'Rudolf_Mildner', 'Rudolf_Neugebauer', 'Rudolf_Oeschey', 'Rudolf_Querner', 'Rudolf_Reinecke', 'Rudolf_Scheide', 'Rudolf_Suttrop', 'Rudolf_von_Ribbentrop', 'Ruediger_Pipkorn', 'Samuel_Kunz', 'Sebastian_Schmid', 'Sepp_Dietrich', 'Siegfried_Graetschus', 'Siegfried_Handloser', 'Siegfried_Ruff', 'Siegfried_Seidl', 'Siegfried_Wolfgang_Fehmer', 'Siert_Bruins', 'Sigmund_Rascher', 'Sverre_Riisnæs', 'Sylvester_Filleböck', 'Sylvester_Stadler', 'Søren_Kam', 'Theo_Saevecke', 'Theodor_Christensen_(SS_Mitglied)', 'Theodor_Dannecker', 'Theodor_Eicke', 'Theodor_Wisch', 'Thomas_Müller_(SS_officer)', 'Tscherim_Soobzokov', 'Udo_von_Woyrsch', 'Uebelhack_Friedrich', 'Ulrich_Graf', 'Ulrich_Greifelt', 'Ulrich_Haberland', 'Viktor_Brack', 'Viktor_Eberhard_Gräbner', 'Viktors_Arājs', 'Vilis_Janums', 'Vinzenz_Kaiser', 'Vinzenz_Schöttl', 'Vojtech_Tuka', 'Waldemar_Fegelein', 'Waldemar_Hoven', 'Waldemar_Klingelhöfer', 'Waldemar_Kraft', 'Waldemar_von_Radetzky', 'Walter_Albath', 'Walter_Blume_(SS officer)', 'Walter_Braemer', 'Walter_Buch', 'Walter_Dürrfeld', 'Walter_Gerth', 'Walter_Greiling', 'Walter_Haensch', 'Walter_Hauck', 'Walter_Huppenkothen', 'Walter_Koehler', 'Walter_Krüger', 'Walter_Kutschmann', 'Walter_Laermann', 'Walter_Letsch', 'Walter_Mattner', 'Walter_Quakernack', 'Walter_Reder', 'Walter_Schellenberg', 'Walter_Schieber', 'Walter_Schimana', 'Walter_Schmitt', 'Walter_Sohst', 'Walter_Staudinger', 'Walter_Ulbricht', 'Walter_Warlimont', 'Walter_Wendt', 'Walter_von_Reichenau', 'Walther_Bierkamp', 'Walther_Funk', 'Walther_Rauff', 'Walther_Schröder', 'Werner_Berger', 'Werner_Best', 'Werner_Blankenburg', 'Werner_Braune', 'Werner_Greunuss', 'Werner_Haase', 'Werner_Hersmann', 'Werner_Heyde', 'Werner_Knab', 'Werner_Lorenz', 'Werner_Naumann', 'Werner_Ostendorff', 'Werner_Paulmann', 'Werner_Thiel', 'Werner_von_Hoven', 'Wernher_von_Braun', 'Wilhelm_Albert_(SS officer)', 'Wilhelm_Altenloh', 'Wilhelm_Beiglboeck', 'Wilhelm_Beiglböck ', 'Wilhelm_Bittrich', 'Wilhelm_Boger', 'Wilhelm_Bonatz', 'Wilhelm_Dörr_(Nazi)', 'Wilhelm_Emmerich', 'Wilhelm_Friedrich_Loeper', 'Wilhelm_Fritz_von_Roettig', 'Wilhelm_Fuchs', 'Wilhelm_Gideon', 'Wilhelm_Günther', 'Wilhelm_Harster', 'Wilhelm_Höttl', 'Wilhelm_Karl_Keppler', 'Wilhelm_Kment', 'Wilhelm_Koppe', 'Wilhelm_Kube', 'Wilhelm_Mohnke', 'Wilhelm_Murr', 'Wilhelm_Pfannenstiel', 'Wilhelm_Rediess', 'Wilhelm_Ritter_von_Leeb', 'Wilhelm_Rosenbaum', 'Wilhelm_Rudolf_Mann', 'Wilhelm_Scharpwinkel', 'Wilhelm_Schröder', 'Wilhelm_Simon', 'Wilhelm_Stuckart', 'Wilhelm_Trabandt', 'Wilhelm_Wagner', 'Wilhelm_Welter', 'Wilhelm_Wiebens', 'Wilhelm_Zander', 'Wilhelm_von_Ammon', 'Wilhelm_von_Grolman', 'Wilhem_Keitel', 'Willem_Sassen', 'Willi_Schatz', 'Willi_Seibert', 'Willi_Tessmann', 'Willi_Zwiener', 'Willy_Gerhard_Hack', 'Wilmar_Hager', 'Wolf-Heinrich_Graf_von_Helldorf', 'Wolfgang_Abel', 'Wolfgang_Birkner', 'Wolfgang_Mettgenberg', 'Wolfgang_Otto_(SS-Mitglied)', 'Wolfgang_Romberg', 'Wolfgang_Wirth', 'Wolfram_Sievers', 'Władysław_Ostrowski']

women = ['Alice Orlowski', 'Anna Hempel', 'Anna Klein', 'Anneliese Kohlmann', 'Dorothea Binz', 'Elfriede Rinkel', 'Elisabeth Becker', 'Elisabeth Lupka', 'Elisabeth Marschall', 'Elisabeth Volkenrath', 'Elsa Ehrich', 'Emma Zimmer', 'Erna Beilhardt', 'Erna Wallisch', 'Eva Justin', 'Ewa Paradies', 'Frieda Walter', 'Gerda Steinhoff', 'Gertrud Feist', 'Gertrud Saurer', 'Gertrud Scholtz-Klink', 'Greta Bösel', 'Helena Kopper',
         'Hermine Braunsteiner', 'Herta Bothe', 'Herta Oberheuser', 'Hertha Ehlert', 'Hilde Liesewitz', 'Hilde Lohbauer', 'Hildegard Kanbach', 'Hildegard Lächert', 'Hildegard Neumann', 'Ilse Forster', 'Ilse Koch', 'Ilse Lothe', 'Irene Haschke', 'Irma Grese', 'Jenny-Wanda Barkmann', 'Johanna Braach', 'Johanna Langefeld', 'Juana Bormann', 'Luise Danz', 'Margarete Gallinat', 'Maria Mandl', 'Ruth Neudeck', 'Therese Brandl', 'Vera Salvequart', 'Wanda Klaff']


sstv_commanders = ['Theodor Eicke', 'Matthias Kleinheisterkamp', 'Georg Keppler',
                   'Max Simon', 'Heinz Lammerding', 'Hermann Priess', 'Karl Ullrich', 'Hellmuth Becker']
