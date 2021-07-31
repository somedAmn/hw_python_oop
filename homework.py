import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = list()

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = list()
        today = dt.date.today()
        for record in self.records:
            if record.date == today:
                today_stats.append(record.amount)
        return sum(today_stats)

    def get_week_stats(self):
        week_stats = 0
        today = dt.date.today()
        day_week_ago = today - dt.timedelta(weeks=1)
        for record in self.records:
            if day_week_ago <= record.date <= today:
                week_stats += record.amount
        return week_stats

    def get_today_balance(self):
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    USD_RATE = 75.0
    EURO_RATE = 85.0
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency):
        balance = self.get_today_balance()
        currencies = {
            'rub': ('руб', CashCalculator.RUB_RATE),
            'usd': ('USD', CashCalculator.USD_RATE),
            'eur': ('Euro', CashCalculator.EURO_RATE)
        }
        name, rate = currencies[currency]
        balance = round(balance / rate, 2)
        if balance > 0:
            return f'На сегодня осталось {balance} {name}'
        elif balance == 0:
            return 'Денег нет, держись'
        else:
            return f'Денег нет, держись: твой долг - {abs(balance)} {name}'


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        balance = self.get_today_balance()
        if balance > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {balance} кКал')
        return 'Хватит есть!'
