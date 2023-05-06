import json
import pathlib

import PySimpleGUI as sg

from writing import create_str_for_block_lane

TOOLTIP_FORMAT = """Ist das Steuerelement zu dem entsprechenden Satz/Durchgang. 
Es ist ein String aus zwei Teilen. Der erste Teil sind die Mannschaft, die im entsprechenden Satz spielen. 
Der zweite Teil nach dem '/' ist jeweils der Durchgang für die Mannschaft. Die Trennung für mehrere 
Mannschaften ist mit '-'. 
BSP: 1-2-3/1-3-2= Mannschaften 1,2 und 3. Mannschaft 1 hat seinen ersten Durchgang, \
Mannschaft 2 seinen dritten und Mannschaft 3 ihren zweiten.
Sollte der Durchgang der Mannschaft mit dem des gesamten Durchgang kann es weggelassen werden. 
Nur wenn für alle gilt."""


def add_bahn(bahn_num: int, durchgaenge: int, spieler_anzahl: int, mannschaften: int) -> sg.Frame:
    """
    Create a new Frame for a new "Bahn"
    :param bahn_num: number of "Bahn"
    :type bahn_num: int
    :param durchgaenge: Number of Durchgänge
    :type durchgaenge: int
    :param spieler_anzahl: Number of Spieler
    :type spieler_anzahl: int
    :param mannschaften: number of mannschaften
    :type mannschaften: int
    :return: New Frame for the specific "Bahn"
    :rtype: sg.Frame
    """
    bahn_layout = list()
    for i in range(1, durchgaenge + 1):
        bahn_layout.append(
            [sg.T("Spieler"),
             sg.Drop(values=[x for x in range(1, spieler_anzahl + 1)], key=f"spieler-{bahn_num}-{i}", size=(10, 1)),
             sg.T("Mannschaft"),
             sg.Drop(values=[x for x in range(1, mannschaften + 1)], key=f"mannschaft-{bahn_num}-{i}", size=(10, 1))])
    new_bahn = sg.Frame(f"Bahn {bahn_num}", layout=bahn_layout, key=f"bahn-{bahn_num}-spalte")
    return new_bahn


def add_durchgang(bahn_anzahl: int, window: sg.Window, durchgang_num: int, spieleranzahl: int, mannschaften: int):
    """
    Adds an extra set to the gui.

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
        window.extend_layout(bahn_spalte, [
            [sg.T("Spieler"),
             sg.Drop(values=[x for x in range(1, spieleranzahl + 1)], key=f"spieler-{bahn}-{durchgang_num}",
                     size=(10, 1)),
             sg.T("Mannschaft"),
             sg.Drop(values=[x for x in range(1, mannschaften + 1)], key=f"mannschaft-{bahn}-{durchgang_num}",
                     size=(10, 1))]])


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
    haupt_frame_layout = [
        [sg.T("Name", tooltip="Name des Bahnschemas", ), sg.Input("", key="h-name")],
        [sg.T("Wechselmodus",
              tooltip="Gibt die das System pro Durchgang an. Das Steuerelement gibt die Mannschaft "
                      + "an. Es wird automatisch durch die Konfiguration die Sätze mit erstellte."),
         sg.Drop(values=values_wechsel, default_value="KEINE", key="h-wechselmodus"),
         sg.T("Spieler wahl",
              tooltip="Wahl des Spielers. Nimmt die Mannschaft und setzt den passenden Spieler ein."),
         sg.Drop(values=values_wahl, default_value="KEINE", key="h-wahl")],
        [sg.T("Anzahl Mannschaften", tooltip="Mannschaften im Modus"),
         sg.Input("2", key="mannschaften", size=(5, 1)),
         sg.T("Anzahl Spieler je Mannschaft"),
         sg.Input("4", key="spieler_je_mannschaft", size=(5, 1))],
        [sg.T("Anzahl Bahnen genutzt"), sg.Input("4", key="num_bahnen_genutzt", size=(5, 1)),
         sg.T("Anzahl Bahnen verfügbar"), sg.Input("8", key="num_bahnen_vorhanden", size=(5, 1)),
         sg.Check("Füllen", default=True, key="füllen")],
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


def valid(values: dict) -> bool:
    wechsel_name = values["h-wechselmodus"]
    with pathlib.Path("wechselmodus").joinpath(wechsel_name).open() as wechselmodus:
        modus_json = json.loads(wechselmodus.read())
    if int(modus_json["num_bahnen"]) != int(values["num_bahnen_genutzt"]):
        return False
    return True


def save(values: dict):
    """
    Create the new .ini file. The name ist "new.ini"
    :param values: values from the gui
    :type values: dict
    :return: nothing
    :rtype: -
    """
    if not valid(values):
        sg.PopupError("Plan ist ungültig! Bitte ändern! ", title="Ungültige Werte!")
        return
    output = []
    # header
    header = f"""[Allgemein]
Name={values["h-name"]} 
Art={int(values["mannschaften"]) - 1}
Anzahl={values["spieler_je_mannschaft"]}
Anzahl Bahnen={values["num_bahnen_genutzt"]}
"""
    output.append(header)
    # body
    bahnen_genutzt = int(values["num_bahnen_vorhanden"])
    bahnen_vorhanden = int(values["num_bahnen_genutzt"])
    for i in range(1, bahnen_genutzt + 1):
        disabled = i > bahnen_vorhanden
        output.append(create_str_for_block_lane(i, values, disabled))
    if values["füllen"]:
        # todo fill if missing  .p
        pass
    with pathlib.Path(f"{values['h-name']}.ini").open(mode="w") as outputFile:
        outputFile.writelines(output)
    sg.Popup("Schema gespeichert")


def update_frame_bahn(values: dict, window: sg.Window):
    """
    Event Function for Update-Button.
    :param values: dict from inputs
    :type values: dict
    :param window: Window to update
    :type window: sg.Window
    :return: -
    :rtype: -
    """
    durchgang_num = int(values["num_durchgänge"])
    current_durchgaenge = len(window["steuer-spalte"].Rows)
    if current_durchgaenge < durchgang_num:
        num_new_durchgaenge = durchgang_num - current_durchgaenge
        for i in range(1, num_new_durchgaenge + 1):
            add_durchgang(int(values["num_bahnen_genutzt"]), window, current_durchgaenge + i,
                          int(values["spieler_je_mannschaft"]), int(values["mannschaften"]))


def run_create_new_window(window: sg.Window) -> None:
    """
    Run the create window for new schemas.
    :param window: Window
    :type window:  sg.Window
    :return: exit program
    :rtype: -
    """
    while True:
        event, values = window.read()
        if event == "h-init":
            frame_bahn = window["frame-bahn"]
            durchgaenge = int(values["num_durchgänge"])
            disable_buttons(window)
            column_layout = []
            for i in range(1, durchgaenge + 1):
                column_layout.append(
                    [sg.T("Mannschaft-Format", tooltip=TOOLTIP_FORMAT),
                     sg.Input(key=f"selected-mannschaft-{i}", size=(10, 1))])
            layout_add: list = [[sg.Column(column_layout, key="steuer-spalte")]]
            for i in range(1, int(values["num_bahnen_genutzt"]) + 1):
                layout_add[0].append(
                    add_bahn(i, durchgaenge, int(values["spieler_je_mannschaft"]), int(values["mannschaften"])))
            window.extend_layout(frame_bahn, layout_add)
        if event == "h-add-durchgang":
            durchgaenge_count = window["num_durchgänge"]
            num_durchgaenge_alt = int(durchgaenge_count.get())
            durchgaenge_count.update(value=str(num_durchgaenge_alt + 1))
            add_durchgang(int(values["num_bahnen_genutzt"]), window, num_durchgaenge_alt + 1,
                          int(values["spieler_je_mannschaft"]), int(values["mannschaften"]))
        if event == "h-update":
            update_frame_bahn(values, window)
        if event == "h-save":
            save(values)

        if event == sg.WINDOW_CLOSED:
            window.close()
            return


def disable_buttons(window):
    update_button = window["h-update"]
    add_button = window["h-add-durchgang"]
    save_button = window["h-save"]
    window["h-init"].update(disabled=True)
    update_button.update(disabled=False)
    add_button.update(disabled=False)
    save_button.update(disabled=False)
