import time

import firebase


class Bug(object):
    def __init__(self, where, what, how, username, userid, resolved=False):
        self.where = where
        self.what = what
        self.how = how
        self.username = username
        self.userid = userid
        self.resolved = resolved

    @classmethod
    def toObj(cls, data):
        return cls(
            data["where"],
            data["what"],
            data["how"],
            data["username"],
            data["userID"],
            data["resolved"],
        )

    def toDict(self):
        return {
            "where": self.where,
            "what": self.what,
            "how": self.how,
            "username": self.username,
            "userID": self.userid,
            "resolved": self.resolved,
        }

    def __repr__(self):
        return (
            f"Bug encountered in: {self.where}\nBug description: {self.what}\nSteps to reproduce bug: {self.how}\n"
            f"Bug status: {'Fixed' if self.resolved else 'In progress'}"
        )

    async def report_bug(self):
        await firebase.add_data(
            "bugs", f"{self.userid}_{int(time.time())}", self.toDict()
        )
        return self

    @classmethod
    async def get_bugs(cls):
        bugs = await firebase.get_support_data("bugs")
        return list(map(cls.toObj, bugs))


class Ticket(object):
    def __init__(self, title, desc, username, userid, resolved=False):
        self.title = title
        self.desc = desc
        self.username = username
        self.userid = userid
        self.resolved = resolved

    @classmethod
    def toObj(cls, data):
        return cls(
            data["title"],
            data["desc"],
            data["username"],
            data["userID"],
            data["resolved"],
        )

    def toDict(self):
        return {
            "title": self.title,
            "desc": self.desc,
            "username": self.username,
            "userID": self.userid,
            "resolved": self.resolved,
        }

    def __repr__(self):
        return f"Title: {self.title}\nDescription: {self.desc}\nTicket status: {'Resolved' if self.resolved else 'Open'}"

    async def submit_ticket(self):
        await firebase.add_data(
            "tickets", f"{self.userid}_{int(time.time())}", self.toDict()
        )
        return self

    @classmethod
    async def get_tickets(cls, userid):
        tickets = await firebase.get_support_data("tickets", userid)
        return list(map(cls.toObj, tickets))


class Feature(object):
    def __init__(self, title, desc, username, userid, status="Pending"):
        self.title = title
        self.desc = desc
        self.username = username
        self.userid = userid
        self.status = status

    @classmethod
    def toObj(cls, data):
        return cls(
            data["title"],
            data["desc"],
            data["username"],
            data["userID"],
            data["status"],
        )

    def toDict(self):
        return {
            "title": self.title,
            "desc": self.desc,
            "username": self.username,
            "userID": self.userid,
            "status": self.status,
        }

    def __repr__(self):
        return f"Title: {self.title}\nDescription: {self.desc}\nStatus: {self.status}"

    async def request_feature(self):
        await firebase.add_data(
            "features", f"{self.userid}_{int(time.time())}", self.toDict()
        )
        return self

    @classmethod
    async def get_feature(cls):
        ft = await firebase.get_support_data("features")
        ftObj = list(map(Feature.toObj, filter(lambda x: x["status"] == "Pending", ft)))
        return ftObj
