import json
import pathlib

import PySimpleGUI as sg


def create_start_window() -> sg.Window:
    """
    Initial call function. This function should be called to create the start window.
    :return: the new start window.
    :rtype: sg.Window
    """
    layout = [[sg.Button("Neues Schema?", key="NEU")]]
    window = sg.Window("Bahnsystem erstellen", layout=layout)
    return window


def add_bahn(bahn_num: int, durchgänge: int, spieler_anzahl: int, mannschaften: int) -> sg.Frame:
    bahn_layout = [[sg.T("Spieler"),
                    sg.Drop(values=[x for x in range(1, spieler_anzahl + 1)], key=f"spieler-{bahn_num}-{1}",
                            size=(10, 1)), sg.T("Mannschaft"),
                    sg.Drop(values=[x for x in range(1, mannschaften + 1)], key=f"mannschaft-{bahn_num}-{1}",
                            size=(10, 1))]]
    for i in range(2, durchgänge + 1):
        bahn_layout.append([sg.T("Spieler"),
                            sg.Drop(values=[x for x in range(1, spieler_anzahl + 1)], key=f"spieler-{bahn_num}-{i}",
                                    size=(10, 1)), sg.T("Mannschaft"),
                            sg.Drop(values=[x for x in range(1, mannschaften + 1)], key=f"mannschaft-{bahn_num}-{i}",
                                    size=(10, 1))])
    new_bahn = sg.Frame(f"Bahn {bahn_num}", layout=bahn_layout, key=f"bahn-{bahn_num}-spalte")
    return new_bahn


def add_durchgang(bahn_anzahl: int, window: sg.Window, durchgang_num: int, spieleranzahl, mannschaften):
    """
    Adds a extra set to the gui.

    :param bahn_anzahl:
    :type bahn_anzahl:
    :param window:
    :type window:
    :param durchgang_num:
    :type durchgang_num:
    :param spieleranzahl:
    :type spieleranzahl:
    :param mannschaften:
    :type mannschaften:
    :return:
    :rtype:
    """
    steuer_spalte = window["steuer-spalte"]
    window.extend_layout(steuer_spalte, [[sg.T("Mannschaft-Format"),
                                          sg.Input("", key=f"selected-mannschaft-{durchgang_num}", size=(10, 1))]])
    for bahn in range(1, bahn_anzahl + 1):
        bahn_spalte = window[f"bahn-{bahn}-spalte"]
        window.extend_layout(bahn_spalte, [[sg.T("Spieler"),
                                            sg.Drop(values=[x for x in range(1, spieleranzahl + 1)],
                                                    key=f"spieler-{bahn}-{durchgang_num}", size=(10, 1)),
                                            sg.T("Mannschaft"),
                                            sg.Drop(values=[x for x in range(1, mannschaften + 1)],
                                                    key=f"mannschaft-{bahn}-{durchgang_num}", size=(10, 1))]])


def create_new_window() -> sg.Window:
    """
    Main loop for create new schema
    :return: nothing
    :rtype: -
    """
    values_wechsel = [modus.stem for modus in pathlib.Path("wechselmodus").iterdir() if modus.is_file()]
    values_wechsel.append("KEINE")
    values_wahl = [wahl.stem for wahl in pathlib.Path("bahnwahl").iterdir() if wahl.is_file()]
    values_wahl.append("KEINE")
    haupt_frame_layout = [[sg.T("Name", tooltip="Name des Bahnschemas", ), sg.Input("", key="h-name")],
                          [sg.T("Wechselmodus",
                                tooltip="Gibt die das System pro Durchgang an. Das Steruelement gibt die Mannschaft an."
                                        + " Es wird automatisch durch die Konfiguration die Sätze mit erstellte."),
                           sg.Drop(values=values_wechsel, default_value="KEINE", key="h-wechselmodus"),
                           sg.T("Spieler wahl",
                                tooltip="Wahl des Spielers. Nimmt die Mannschaft und setzt den passenden Spieler ein."),
                           sg.Drop(values=values_wahl, default_value="KEINE", key="h-wahl")],
                          [sg.T("Anzahl Mannschaften", tooltip="Mannschaften im Modus"),
                           sg.Input("2", key="mannschaften", size=(5, 1)),
                           sg.T("Anzahl Spieler je Mannschaft"),
                           sg.Input("4", key="spieler_je_mannschaft", size=(5, 1))],
                          [sg.T("Anzahl Bahnen genutzt"), sg.Input("4", key="num_bahnen_genutzt", size=(5, 1)),
                           sg.T("Anzahl Bahnen verfügbar"), sg.Input("8", key="num_bahnen_vorhanden", size=(5, 1))],
                          [sg.T("Durchgänge"), sg.Input("2", key="num_durchgänge", size=(5, 1))],
                          [sg.T("Volle", tooltip="Anzahl Volle pro Satz/Durchgang."),
                           sg.Input("15", key="volle", size=(6, 1)),
                           sg.T("Räumer", tooltip="Anzahl Abräumer pro Satz/Durchgang."),
                           sg.Input("15", key="abräumer", size=(6, 1)),
                           sg.T("Zeit", tooltip="Zeit pro Satz/Durchgang in Minuten"),
                           sg.Input("12", key="zeit", size=(6, 1))],
                          [sg.Button("Aktualisieren", key="h-update", disabled=True),
                           sg.Button("Init", tooltip="Initiale Eingabe, erzeugt Bahnen und benötigte Elemente.",
                                     key="h-init", disabled=False),
                           sg.Button("Durchgang dazu", key="h-add-durchgang", disabled=True),
                           sg.Button("Speichern", key="h-save", disabled=True)]]
    haupt_frame = sg.Frame("Hauptinfos", layout=haupt_frame_layout)
    schema_layout = [[]]
    schema = sg.Frame("Bahnanlegung", layout=schema_layout, key="frame-bahn", expand_x=True)
    layout = [[haupt_frame], [schema]]
    return sg.Window("Neues Bahnschema", layout=layout)


def create_durchgang_string(volle: int, abräumer: int, zeit: int, durchgang: int, bahn_num: int, values: dict,
                            invalid: bool = False) -> str:
    """
    Creates the
    :param volle:
    :type volle:
    :param abräumer:
    :type abräumer:
    :param zeit:
    :type zeit:
    :param durchgang:
    :type durchgang:
    :param bahn_num:
    :type bahn_num:
    :param values:
    :type values: dict
    :param invalid: says if a lane is invalid (default = false)
    :type invalid: bool
    :return:
    :rtype:
    """
    back = ""
    wechselmodus = values['h-wechselmodus']
    bahnwahl = values['h-wahl']
    if wechselmodus != "KEINE":
        wechselmodus_path = pathlib.Path(f"wechselmodus/{wechselmodus}.json")
        with wechselmodus_path.open("r") as wechselmodus_file:
            wechselmodus = json.loads(wechselmodus_file.read())
    if bahnwahl != "KEINE":
        bahnwahl_path = pathlib.Path(f"bahnwahl/{bahnwahl}.json")
        with bahnwahl_path.open("r") as bahnwahl_file:
            bahnwahl = json.loads(bahnwahl_file.read())
    if wechselmodus == "KEINE" and bahnwahl == "KEINE":
        spieler = int(values[f"spieler-{bahn_num}-{durchgang}"]) - 1
        mannschaft = int(values[f"mannschaft-{bahn_num}-{durchgang}"]) - 1
        back = f"""Spieler {durchgang}={spieler}
        Mannschaft {durchgang}={mannschaft}
        Volle {durchgang}={volle}
        Abraeumer {durchgang}={abräumer}
        Zeit {durchgang}={zeit}\n"""
    # Jeder Durchgang einzeln angegeben aber Mannschaft wird gewählt
    elif wechselmodus == "KEINE" and bahnwahl != "KEINE":
        pass  # todo
    # Jeder Durchgang mal Wechselmodus, und Mannschaft + Spieler wird angegeben
    elif wechselmodus != "KEINE" and bahnwahl == "KEINE":
        pass  # todo
    # Jeder Durchgang ist mal dem Wechselmodus und Mannschaften werden gewählt
    else:
        back = write_wechsel_and_select(abräumer, back, bahn_num, bahnwahl, durchgang, invalid, values, volle,
                                        wechselmodus, zeit)
    return back


def write_wechsel_and_select(abräumer, back, bahn_num, bahnwahl, durchgang, invalid, values, volle, wechselmodus, zeit):
    # Für jeden Satz im Wechselmodus
    anzahl_sätze = len(wechselmodus["modus"])
    for satz_num, satz in enumerate(wechselmodus["modus"], 1):
        satz_gesamt = (durchgang - 1) * anzahl_sätze + satz_num
        if invalid:
            spieler_der_mannschaft = -1
            mannschaft = -1
            volle_out = ""
            abräumer_out = ""
            zeit_out = ""
        else:
            start_pos = satz[bahn_num - 1]  #
            mannschaft_nummer_index = bahnwahl["select"][start_pos - 1][0] - 1
            if not str(values[f"selected-mannschaft-{durchgang}"]).__contains__("/"):
                durchgang_der_mannschaft = durchgang
            else:
                durchgang_der_mannschaft = str(values[f"selected-mannschaft-{durchgang}"]).split("/")[1].split("-")[
                    mannschaft_nummer_index]
            spieler_der_mannschaft = bahnwahl["select"][start_pos - 1][1] + (durchgang_der_mannschaft - 1) * \
                                     bahnwahl["spieler_je_mannschaft"] - 1
            mannschaft_nummer = str(values[f"selected-mannschaft-{durchgang}"]).split("/")[0].split("-")[
                mannschaft_nummer_index]
            mannschaft = int(mannschaft_nummer) - 1
            volle_out = volle
            abräumer_out = abräumer
            zeit_out = zeit
        back += f"""Spieler {satz_gesamt}={spieler_der_mannschaft}
Mannschaft {satz_gesamt}={mannschaft}
Volle {satz_gesamt}={volle_out}
Abraeumer {satz_gesamt}={abräumer_out}
Zeit {satz_gesamt}={zeit_out}
"""
    return back


def write_lane(bahn_num: int, values: dict, invalid=False) -> str:
    """
    create string for a single line
    :param bahn_num: number of the lane
    :type bahn_num: int
    :param values: values from the gui
    :type values: dict
    :param invalid:
    :type invalid: bool
    :return: the complete string for the lane
    :rtype: str
    """
    if not invalid:
        zeit = int(values["zeit"])
        volle = int(values["volle"])
        abräumer = int(values["abräumer"])
    else:
        zeit = 0
        volle = 0
        abräumer = 0
    anzahl_durchgänge = int(values["num_durchgänge"])
    string = f"[Bahn {bahn_num}]\n"
    for durchgang in range(1, anzahl_durchgänge + 1):
        durchgang_string = create_durchgang_string(volle, abräumer, zeit, durchgang, bahn_num,
                                                   values, invalid)
        string += durchgang_string
    return string


def save(values: dict):
    """
    Create the new .ini file. The name ist "new.ini"
    :param values: vallues from the gui
    :type values: dict
    :return: nothing
    :rtype: -
    """
    output = []
    # header
    header = f"""[Allgemein]
Name={values["h-name"]} 
Art=3
Anzahl={values["spieler_je_mannschaft"]}
Anzahl Bahnen={values["mannschaften"]}
"""
    output.append(header)
    for i in range(1, int(values["num_bahnen_vorhanden"]) + 1):
        invalid = i > int(values["num_bahnen_genutzt"])
        output.append(write_lane(i, values, invalid))
    with pathlib.Path("neu.ini").open(mode="w") as outputFile:
        outputFile.writelines(output)


def update_frame_bahn(frame_bahn: sg.Frame, values: dict, window: sg.Window):
    durchgang_num = int(values["num_durchgänge"])
    if len(frame_bahn.Rows[0]) < int(values["num_durchgänge"]) + 1:
        add_durchgang(int(values["num_bahnen_genutzt"]), window, durchgang_num, int(values["spieler_je_mannschaft"]),
                      int(values["mannschaften"]))


def run_create_new_window(window: sg.Window):
    while 1:
        event, values = window.read()
        if event == "h-init":
            update_button = window["h-update"]
            update_button.update(disabled=False)
            window["h-init"].update(disabled=True)
            add_button = window["h-add-durchgang"]
            add_button.update(disabled=False)
            save_button = window["h-save"]
            save_button.update(disabled=False)
            frame_bahn = window["frame-bahn"]
            durchgaenge = int(values["num_durchgänge"])
            column_layout = [[]]
            for i in range(1, durchgaenge + 1):
                column_layout.append(
                    [sg.T("Mannschaft-Format",
                          tooltip="""Ist das Steuerelement zu dem entsprechenden Satz/Durchgang. 
Es ist ein String aus zwei Teilen. Der erste Teil sind die Mannschaft, die im entsprechenden Satz spielen. 
Der zweite Teil nach dem '/' ist jeweils der Durchgang für die Mannschaft. Die Trennung für mehrere 
Mannschaften ist mit '-'. 
BSP: 1-2-3/1-3-2= Mannschaften 1,2 und 3. Mannschaft 1 hat seinen ersten Durchgang, 
    Mannschaft 2 seinen dritten und Mannschaft 3 ihren zweiten.
Sollte der Durchgang der Mannschaft mit dem des gesamten Durchgang kann es weggelassen werden. 
Nur wenn für alle gilt."""),
                     sg.Input(key=f"selected-mannschaft-{i}", size=(10, 1))])
            layout_add = [[sg.Column(column_layout, key="steuer-spalte")]]
            for i in range(1, int(values["num_bahnen_genutzt"]) + 1):
                layout_add[0].append(
                    add_bahn(i, durchgaenge, int(values["spieler_je_mannschaft"]), int(values["mannschaften"])))
            window.extend_layout(frame_bahn, layout_add)
        if event == "h-add-durchgang":
            durchgänge_count = window["num_durchgänge"]
            num_durchgänge_alt = int(durchgänge_count.get())
            durchgänge_count.update(value=str(num_durchgänge_alt + 1))
            add_durchgang(int(values["num_bahnen_genutzt"]), window, num_durchgänge_alt + 1,
                          int(values["spieler_je_mannschaft"]), int(values["mannschaften"]))
        if event == "h-update":
            frame_bahn = window["frame-bahn"]
            update_frame_bahn(frame_bahn, values, window)
            print("aktualisiert")
        if event == "h-save":
            save(values)
        if event == sg.WINDOW_CLOSED:
            window.close()
            return


def run_start_window(window: sg.Window):
    event, value = window.read()
    if event == "NEU":
        window.close()
        new_window = create_new_window()
        run = run_create_new_window
    else:
        return
    run(new_window)
