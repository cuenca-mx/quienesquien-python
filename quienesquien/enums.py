from enum import Enum, IntEnum


class SearchType(IntEnum):
    fisica = 0
    moral = 1


class SearchList(str, Enum):
    PPE = 'PPE'
    PEPINT = 'PEPINT'
    OFAC = 'OFAC'
    OFACN = 'OFACN'
    ONU = 'ONU'
    SAT69 = 'SAT69'
    SAT69B = 'SAT69B'
    SANC = 'SANC'
    ATF = 'ATF'
    BID = 'BID'
    BIS = 'BIS'
    BM = 'BM'
    BOE = 'BOE'
    CBI = 'CBI'
    DEA = 'DEA'
    DFAT = 'DFAT'
    EPA = 'EPA'
    FAMI = 'FAMI'
    FBI = 'FBI'
    FINCEN = 'FINCEN'
    FUNC = 'FUNC'
    GAFI = 'GAFI'
    HMT = 'HMT'
    ICE = 'ICE'
    INTP = 'INTP'
    LMW = 'LMW'
    OCDE = 'OCDE'
    OSFI = 'OSFI'
    FGJ = 'FGJ'
    FGR = 'FGR'
    FGRCOM = 'FGRCOM'
    PIS = 'PIS'
    REFIPRE = 'REFIPRE'
    SSEU = 'SSEU'
    UE = 'UE'
    UKMW = 'UKMW'
    USMS = 'USMS'
    VENC = 'VENC'
    CAR = 'CAR'
    DPRK = 'DPRK'
    DRC = 'DRC'
    GB = 'GB'
    IRAN = 'IRAN'
    IRAQ = 'IRAQ'
    LIBY = 'LIBY'
    MALI = 'MALI'
    ONUAQ = 'ONUAQ'
    ONUTAL = 'ONUTAL'
    SOMA = 'SOMA'
    SOUT = 'SOUT'
    SUDA = 'SUDA'
    YEME = 'YEME'


class Gender(str, Enum):
    masculino = 'M'
    femenino = 'F'
