import firebase


class Portfolio(object):
    def __init__(self, userid, username, balance=0, invested=0, investments=None):
        self.userid = userid
        self.username = username
        self.balance = balance
        self.invested = invested
        self.investments = investments if investments is not None else {}

    @property
    def account_value(self):
        return self.balance + self.portfolio_value

    @property
    def portfolio_value(self):
        value = 0
        for coin, count in self.investments.items():
            coin_obj = Coin(coin)
            value += coin_obj.price * count
        return value

    @property
    def pnl(self):
        return self.portfolio_value - self.invested

    @classmethod
    def toObj(cls, data):
        return cls(
            data["userID"],
            data["username"],
            data["balance"],
            data["invested"],
            data["investments"],
        )

    def toDict(self):
        return {
            "userID": self.userid,
            "username": self.username,
            "balance": self.balance,
            "invested": self.invested,
            "investments": self.investments,
        }

    def __repr__(self):
        return (
            f"Account value: £{self.account_value}\nPortfolio value: £{self.portfolio_value}\nTotal invested: £{self.invested}\n"
            f"Free funds: £{self.balance}\nP&L: £{self.pnl}\nInvestments: {self.investments}"
        )

    # @classmethod
    # def open_account(cls, userid, username):
    #     '''
    #     1. Check if user has an account.
    #     2. -> if account exists, return false
    #     3. Create account object
    #     4. Store in firebase db using userid as documentID
    #     5. return true
    #     '''
    #     user = firebase.get_exchange_data("users", userid)
    #     if user is None:
    #         userportfolio = cls(username, userid)
    #         firebase.add_data("users", str(userid), userportfolio.toDict())
    #         return True
    #     return False

    # @staticmethod
    # def close_account(userid):
    #     '''
    #     1. Check if user has an account.
    #     2. -> if account does not exists, return false
    #     3. Find account in firebase db using userid
    #     4. Delete entry
    #     5. return true
    #     '''
    #     user = firebase.get_exchange_data("users", userid)
    #     if user is not None:
    #         firebase.db.collection("users").document(str(userid)).delete()
    #         return True
    #     return False

    # @classmethod
    # def get_account(cls, userid):
    #     '''
    #     1. Check if user has an account.
    #     2. -> if account does not exists, return false
    #     3. Find account in firebase db using userid
    #     4. Convert back to object from dict
    #     5. return embed
    #     '''
    #     user = firebase.get_exchange_data("users", userid)
    #     if user is not None:
    #         return cls.toObj(user)
    #     return None

    # @classmethod
    # def deposit(cls, userid, value):
    #     '''
    #     1. Check if user has an account.
    #     2. -> if account does not exists, return false
    #     3. Find account in firebase db using userid
    #     4. Add funds to free funds
    #     5. Update user data in firebase
    #     5. return true
    #     '''
    #     user = firebase.get_exchange_data("users", userid)
    #     if user is not None:
    #         prtfl = cls.toObj(user)
    #         prtfl.balance += int(value)
    #         firebase.add_data("users", str(userid), prtfl.toDict())
    #         return True
    #     return False

    # @classmethod
    # def transfer(cls, from_id, to_id, coin, amount):
    #     from_acc = cls.get_account(from_id)
    #     to_acc = cls.get_account(to_id)
    #     if from_acc or to_acc is None:
    #         return False
    #     from_acc.investments[coin] -= amount
    #     to_acc.investments[coin] += amount
    #     return True


class Coin(object):
    def __init__(self, ticker):
        self.ticker = ticker
        self.exchange = Exchange()

    @property
    def price(self):
        return self.exchange.get_price(self)


class Exchange(object):
    def __init__(self):
        pass

    @property
    def coins(self):
        """
        get coins from firebase
        :return:
        """
        return None

    def get_coins(self):
        return self.coins

    def get_price(self, coin):
        if coin in self.coins:
            pass
        return None

    def get_graph(self, coin):
        if coin in self.coins:
            pass
        return None

    @staticmethod
    def open_account(userid, username):
        user = firebase.get_exchange_data("users", userid)
        if user is None:
            user_portfolio = Portfolio(username, userid)
            firebase.add_data("users", str(userid), user_portfolio.toDict())
            return True
        return False

    @staticmethod
    def close_account(userid):
        user = firebase.get_exchange_data("users", userid)
        if user is not None:
            firebase.db.collection("users").document(str(userid)).delete()
            return True
        return False

    @staticmethod
    def get_account(userid):
        user = firebase.get_exchange_data("users", userid)
        if user is not None:
            return Portfolio.toObj(user)
        return None

    @staticmethod
    def deposit(userid, value):
        user = firebase.get_exchange_data("users", userid)
        if user is not None:
            prtfl = Portfolio.toObj(user)
            prtfl.balance += int(value)
            firebase.add_data("users", str(userid), prtfl.toDict())
            return True
        return False

    def reset(self):
        pass

    def buy(self):
        pass

    def sell(self):
        pass

    def transfer(self):
        pass
