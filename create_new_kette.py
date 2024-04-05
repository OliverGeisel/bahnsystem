import pathlib

import PySimpleGUI as sg

from writing import create_str_ketten_lane


def create_kette_window() -> sg.Window:
    layout = [
        [sg.T("Name", tooltip="Name des Bahnschemas", ), sg.Input("", key="name")],
        [sg.T("Anzahl Spieler:"), sg.Spin(values=[v for v in range(1, 101)], initial_value=4, key="spieler_anzahl"),
         sg.T("Anzahl Bahnen genutzt:"),
         sg.Spin(values=[v for v in range(1, 21)], initial_value=4, key="bahnen_genutzt")],
        [sg.T("Anzahl Bahnen verfügbar:"),
         sg.Spin(values=[v for v in range(1, 21)], initial_value=8, key="bahnen_verfügbar")],
        [sg.T("Mannschaften:"), sg.Sp(values=[v for v in range(1, 21)], initial_value=1, key="mannschaften_anzahl")],
        [sg.Button("Init", key="INIT"), sg.Button("Erstellen", key="CREATE", disabled=True)],
        [sg.Frame("Bahnen", layout=[[]], key="bahn_frame")]
    ]
    window = sg.Window("Neuer Kettenstart", layout=layout)
    return window


def create_bahnen(values: dict, window: sg.Window):
    bahnen_num = int(values["bahnen_genutzt"])
    frame = window["bahn_frame"]
    bahnen = list()
    for i in range(1, bahnen_num + 1):
        bahn_layout = [[sg.T(f"Bahn {i}"), sg.T("Volle"),
                        sg.Sp(values=[v for v in range(201)], initial_value=15, key=f"bahn_{i}_volle"),
                        sg.T("Abräumer"),
                        sg.Sp(values=[v for v in range(201)], initial_value=15, key=f"bahn_{i}_abräumer"),
                        sg.T("Zeit"), sg.Sp(values=[v for v in range(50)], initial_value=12, key=f"bahn_{i}_zeit")]]
        new_bahn = [sg.Column(layout=bahn_layout, key=f"bahn_{i}_column")]
        bahnen.append(new_bahn)
    window.extend_layout(frame, bahnen)


def save(values: dict):
    output = []
    # header
    header = f"""[Allgemein]
Name={values["name"]} 
Art={int(values["mannschaften_anzahl"]) - 1}
Anzahl={values["spieler_anzahl"]}
Anzahl Bahnen={values["bahnen_genutzt"]}
"""
    output.append(header)
    # body
    bahnen_genutzt = int(values["bahnen_genutzt"])
    bahnen_vorhanden = int(values["bahnen_verfügbar"])
    for i in range(1, bahnen_vorhanden + 1):
        disabled = i > bahnen_genutzt
        output.append(create_str_ketten_lane(i, values, disabled))
    # write to out dir
    out_dir = pathlib.Path("out")
    if not out_dir.exists():
        out_dir.mkdir()
    with out_dir.joinpath(f"{values['name']}.ini").open(mode="w") as outputFile:
        outputFile.writelines(output)
    sg.PopupOK("Schema wurde erstellt!", title="Gespeichert")


def run_kette_window(window: sg.Window):
    while True:
        event, values = window.read()
        if event == "CREATE":
            save(values)
        elif event == "INIT":
            window["CREATE"].update(disabled=False)
            window["INIT"].update(disabled=True)
            create_bahnen(values, window)
        elif event == sg.WINDOW_CLOSED:
            return
        else:
            return
