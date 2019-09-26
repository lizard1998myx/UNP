from UNP.Interface import Interface
from UNP.Application import Loginer


def activate():
    Interface().keyboard()


def activate_shortcut():
    Loginer().active()


def activate_passive():
    Loginer().passive()
