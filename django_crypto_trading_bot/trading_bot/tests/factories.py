from datetime import datetime
from decimal import Decimal

import pytz
from django.utils import timezone
from factory import DjangoModelFactory, SubFactory

from django_crypto_trading_bot.trading_bot.models import (
    Exchanges,
    Order,
    Timeframes,
    Bot)
from django_crypto_trading_bot.users.tests.factories import UserFactory


class AccountFactory(DjangoModelFactory):
    class Meta:
        model = "trading_bot.Account"
        django_get_or_create = ["api_key"]

    exchange = Exchanges.BINANCE
    user = SubFactory(UserFactory)
    api_key = "*"
    secret = "*"


class TrxCurrencyFactory(DjangoModelFactory):
    class Meta:
        model = "trading_bot.Currency"
        django_get_or_create = ["short"]

    name = "TRON"
    short = "TRX"


class BnbCurrencyFactory(TrxCurrencyFactory):
    name = "Binance Coin"
    short = "BNB"


class EurCurrencyFactory(TrxCurrencyFactory):
    name = "Euro"
    short = "EUR"


class BtcCurrencyFactory(TrxCurrencyFactory):
    name = "Bitcoin"
    short = "BTC"


class UsdtCurrencyFactory(TrxCurrencyFactory):
    name = "Tether"
    short = "USDT"


class EthCurrencyFactory(TrxCurrencyFactory):
    name = "Ethereum"
    short = "ETH"


class MarketFactory(DjangoModelFactory):
    class Meta:
        model = "trading_bot.Market"
        django_get_or_create = ["base", "quote"]

    base = SubFactory(TrxCurrencyFactory)
    quote = SubFactory(BnbCurrencyFactory)
    exchange = Exchanges.BINANCE
    active = True
    precision_amount = 3
    precision_price = 4
    limits_amount_min = Decimal(0.1)
    limits_amount_max = Decimal(1000)
    limits_price_min = Decimal(0.1)
    limits_price_max = Decimal(1000)


class BnbEurMarketFactory(MarketFactory):
    base = SubFactory(BnbCurrencyFactory)
    quote = SubFactory(EurCurrencyFactory)


class EthBnbMarketFactory(MarketFactory):
    base = SubFactory(EthCurrencyFactory)
    quote = SubFactory(BnbCurrencyFactory)


class BtcBnbMarketFactory(MarketFactory):
    base = SubFactory(EthCurrencyFactory)
    quote = SubFactory(BnbCurrencyFactory)


class OutOfDataMarketFactory(MarketFactory):
    base = SubFactory(BtcCurrencyFactory)
    quote = SubFactory(UsdtCurrencyFactory)
    active = False
    precision_amount = 10
    precision_price = 10
    limits_amount_min = Decimal(0.1)
    limits_amount_max = Decimal(1000)
    limits_price_min = Decimal(0.1)
    limits_price_max = Decimal(1000)


class BotFactory(DjangoModelFactory):
    class Meta:
        model = "trading_bot.Bot"

    account = SubFactory(AccountFactory)
    market = SubFactory(MarketFactory)


class RisingChartBotFactory(BotFactory):

    trade_mode = Bot.TradeMode.RISING_CHART
    quote = SubFactory(BnbCurrencyFactory)
    max_amount = Decimal(1)
    min_rise = Decimal(5)
    stop_loss = Decimal(2)


class BuyOrderFactory(DjangoModelFactory):
    class Meta:
        model = "trading_bot.Order"
        django_get_or_create = ["order_id"]

    bot = SubFactory(BotFactory)
    order_id = "1"
    timestamp = timezone.now()
    status = Order.Status.CLOSED
    order_type = Order.OrderType.LIMIT
    side = Order.Side.SIDE_BUY
    price = Decimal(10)
    amount = Decimal(100)
    filled = Decimal(100)


class SellOrderFactory(BuyOrderFactory):
    order_id = "2"
    side = Order.Side.SIDE_SELL


class OpenBuyOrderFactory(BuyOrderFactory):
    order_id = "3"
    status = Order.Status.OPEN


class EndOrderFactory(BuyOrderFactory):
    order_id = "4"
    status = Order.Status.NOT_MIN_NOTIONAL


class BuyFeeOrderFactory(BuyOrderFactory):
    order_id = "5"
    fee_currency = SubFactory(BnbCurrencyFactory)
    fee_cost = Decimal(0.1)
    fee_rate = Decimal(0.01)


class RisingChartOrderFactory(BuyOrderFactory):
    order_id = "6"
    side = Order.Side.SIDE_BUY
    order_type = Order.OrderType.MARKET
    bot = SubFactory(RisingChartBotFactory)
    price = Decimal(1)
    last_price_tick = Decimal(1)
    market = SubFactory(MarketFactory)


class TradeFactory(DjangoModelFactory):
    class Meta:
        model = "trading_bot.Trade"
        django_get_or_create = ["trade_id"]

    order = SubFactory(BuyOrderFactory)
    trade_id = "123"
    timestamp = timezone.now()
    taker_or_maker = Order.OrderType.MARKET
    amount = Decimal(10)
    fee_currency = SubFactory(EurCurrencyFactory)
    fee_cost = Decimal(000.1)
    fee_rate = Decimal(00.1)


class OHLCVBnbEurFactory(DjangoModelFactory):
    class Meta:
        model = "trading_bot.OHLCV"
        django_get_or_create = ["market", "timestamp", "timeframe"]

    market = SubFactory(BnbEurMarketFactory)
    timeframe = Timeframes.MINUTE_1
    timestamp = datetime(
        year=2020, month=4, day=30, hour=23, tzinfo=pytz.timezone("UTC")
    )
    open_price = Decimal(0)
    highest_price = Decimal(0)
    lowest_price = Decimal(0)
    closing_price = Decimal(15.7987)
    volume_price = Decimal(0)


class OHLCVTrxBnbFactory(OHLCVBnbEurFactory):
    market = SubFactory(MarketFactory)
    closing_price = Decimal(15.7987)
