from typing_extensions import Self


class COTDetail(object):
    def __init__(self,instrumentname,importdate,openinterest,noncomm_long,noncomm_short):
        self.instrumentname = instrumentname
        self.importdate = importdate
        self.openinterest = openinterest
        self.noncomm_long = noncomm_long
        self.noncomm_short = noncomm_short