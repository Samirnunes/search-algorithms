from enum import Enum

class State(Enum):
    RN = 0
    PB = 1
    CE = 2
    PE = 3
    AL = 4
    SE = 5
    PI = 6
    BA = 7
    ES = 8
    DF = 9
    MA = 10
    TO = 11
    GO = 12
    MG = 13
    RJ = 14
    PA = 15
    MT = 16
    MS = 17
    SP = 18
    RR = 19
    AP = 20
    PR = 21
    AM = 22
    RO = 23
    AC = 24
    SC = 25
    RS = 26
        
    @classmethod
    def map(cls, i: int):
        return {state.value: state.name for state in cls}[i]