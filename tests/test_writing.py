from unittest import TestCase

import exceptions
import writing


class Test(TestCase):
    def test_empty_bahn_durchgang_0_must_fail(self):
        try:
            writing.empty_bahn_durchgang(0)
            self.fail()
        except exceptions.IllegalInputException:
            pass

    def test_empty_bahn_durchgang_negative_number_must_fail(self):
        try:
            writing.empty_bahn_durchgang(-1)
            self.fail()
        except exceptions.IllegalInputException:
            pass

    def test_empty_bahn_durchgang_1_ok(self):
        correct = """Spieler 1=-1
Mannschaft 1=-1
Volle 1=
Abraeumer 1=
Zeit 1=
"""
        try:
            result = writing.empty_bahn_durchgang(1)
            self.assertEqual(correct, result)
        except exceptions.IllegalInputException:
            pass

    def test_create_str_durchgang_negative_durchgang_fail(self):
        durchgang = -1
        abraeumer = 20
        volle = 20
        zeit = 20
        spieler = 1
        mannschaft = 1
        try:
            writing.create_str_durchgang(volle, abraeumer, zeit, durchgang, spieler, mannschaft)
            self.fail()
        except exceptions.IllegalInputException:
            pass

    def test_create_str_durchgang_0_durchgang_fail(self):
        durchgang = 0
        abraeumer = 20
        volle = 20
        zeit = 20
        spieler = 1
        mannschaft = 1
        try:
            writing.create_str_durchgang(volle, abraeumer, zeit, durchgang, spieler, mannschaft)
            self.fail()
        except exceptions.IllegalInputException:
            pass
