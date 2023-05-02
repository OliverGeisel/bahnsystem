import json
import pathlib


def empty_bahn_durchgang(durchgang: int) -> str:
    return f"""Spieler {durchgang}=-1
Mannschaft {durchgang}=-1
Volle {durchgang}=
Abraeumer {durchgang}=
Zeit {durchgang}=
"""


def create_str_durchgang(volle: int, abraeumer: int, zeit: int, durchgang: int, spieler: int,
                         mannschaft: int) -> str:
    return f"""Spieler {durchgang}={spieler}
Mannschaft {durchgang}={mannschaft}
Volle {durchgang}={volle}
Abraeumer {durchgang}={abraeumer}
Zeit {durchgang}={zeit}
"""


def create_block_durchgang_string(volle: int, abraeumer: int, zeit: int, durchgang: int, bahn_num: int, values: dict,
                                  invalid: bool = False) -> str:
    """
    Creates the string to
    :param volle:
    :type volle:
    :param abraeumer:
    :type abraeumer:
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
    :return: The complete String for one "Durchgang"
    :rtype: str
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
        back = create_str_durchgang(volle, abraeumer, zeit, durchgang, spieler, mannschaft)
    # Jeder Durchgang einzeln angegeben aber Mannschaft wird gewählt
    elif wechselmodus == "KEINE" and bahnwahl != "KEINE":
        pass  # todo
    # Jeder Durchgang mal Wechselmodus, und Mannschaft + Spieler wird angegeben
    elif wechselmodus != "KEINE" and bahnwahl == "KEINE":
        pass  # todo
    # Jeder Durchgang ist mal dem Wechselmodus und Mannschaften werden gewählt
    else:
        back = create_block_wechsel_and_select(abraeumer, back, bahn_num, bahnwahl, durchgang, invalid, values, volle,
                                               wechselmodus, zeit)
    return back


def create_block_wechsel_and_select(abraeumer: int, back: str, bahn_num: int, bahnwahl: dict, durchgang: int,
                                    invalid: bool, values: dict, volle: int, wechselmodus: dict, zeit: int) -> str:
    # Für jeden Satz im Wechselmodus
    anzahl_saetze = len(wechselmodus["modus"])
    for satz_num, satz in enumerate(wechselmodus["modus"], 1):
        satz_gesamt = (durchgang - 1) * anzahl_saetze + satz_num
        if invalid:
            back += empty_bahn_durchgang(satz_gesamt)
        else:
            start_pos = satz[bahn_num - 1]  #
            mannschaft_nummer_index = bahnwahl["select"][start_pos - 1][0] - 1
            if "/" not in str(values[f"selected-mannschaft-{durchgang}"]):
                durchgang_der_mannschaft = durchgang
            else:
                durchgang_der_mannschaft = int(str(values[f"selected-mannschaft-{durchgang}"]).split("/")[1].split("-")[
                                                   mannschaft_nummer_index])
            spieler_der_mannschaft: int = bahnwahl["select"][start_pos - 1][1] \
                                          + (durchgang_der_mannschaft - 1) * bahnwahl["spieler_je_mannschaft"] - 1
            mannschaft_nummer: int = int(str(values[f"selected-mannschaft-{durchgang}"]).split("/")[0].split("-")[
                                             mannschaft_nummer_index])
            mannschaft: int = int(mannschaft_nummer) - 1
            volle_out: int = volle
            abraeumer_out: int = abraeumer
            zeit_out: int = zeit
            back += create_str_durchgang(volle_out, abraeumer_out, zeit_out, satz_gesamt, spieler_der_mannschaft,
                                         mannschaft)
    return back


def create_str_for_block_lane(bahn_num: int, values: dict, disabled: bool = False) -> str:
    """
    create string for a single "BAhn".
    :param bahn_num: number of the lane
    :type bahn_num: int
    :param values: values from the gui
    :type values: dict
    :param disabled: Says if the bahn is not used
    :type disabled: bool
    :return: the complete string for the "Bahn"
    :rtype: str
    """
    if disabled:
        zeit = 0
        volle = 0
        abraeumer = 0
    else:
        zeit = int(values["zeit"])
        volle = int(values["volle"])
        abraeumer = int(values["abräumer"])
    anzahl_durchgaenge = int(values["num_durchgänge"])
    string = f"[Bahn {bahn_num}]\n"
    for durchgang in range(1, anzahl_durchgaenge + 1):
        durchgang_string = create_block_durchgang_string(volle, abraeumer, zeit, durchgang, bahn_num, values, disabled)
        string += durchgang_string
    return string


def create_str_ketten_lane(bahn_num: int, values: dict, disabled: bool = False) -> str:
    used_bahnen = int(values["bahnen_genutzt"])
    count_spieler_per_m = int(values["spieler_anzahl"])
    count_mannschaften = int(values["mannschaften_anzahl"])
    max_durchgaenge = count_spieler_per_m * count_mannschaften + used_bahnen - 1
    if disabled:
        zeit = 0
        volle = 0
        abraeumer = 0
    else:
        zeit = int(values[f"bahn_{bahn_num}_zeit"])
        volle = int(values[f"bahn_{bahn_num}_volle"])
        abraeumer = int(values[f"bahn_{bahn_num}_abräumer"])
    string = f"[Bahn {bahn_num}]\n"
    for durchgang in range(1, max_durchgaenge + 1):
        if disabled or durchgang < bahn_num or durchgang > max_durchgaenge - (4 - bahn_num):
            string += empty_bahn_durchgang(durchgang)
        else:
            spieler = (durchgang - bahn_num) // count_mannschaften
            mannschaft = (durchgang - bahn_num) % count_mannschaften
            durchgang_string = create_str_durchgang(volle, abraeumer, zeit, durchgang, spieler, mannschaft)
            string += durchgang_string
    return string
