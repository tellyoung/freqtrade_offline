"""Offline version of Binance exchange subclass"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import ccxt
from pandas import DataFrame

from freqtrade.constants import DEFAULT_DATAFRAME_COLUMNS
from freqtrade.enums import CandleType, MarginMode, PriceType, TradingMode
from freqtrade.exceptions import DDosProtection, OperationalException, TemporaryError
from freqtrade.exchange import Exchange
from freqtrade.exchange.binance import Binance
from freqtrade.exchange.exchange_types import FtHas, Tickers
from freqtrade.util.datetime_helpers import dt_from_ts


logger = logging.getLogger(__name__)


class BinanceOffline(Binance):
    """
    Offline version of Binance exchange.
    This class overrides methods that would normally make network requests,
    returning static or pre-defined data instead.
    """

    def __init__(self, config: Dict[str, Any], validate: bool = True) -> None:
        """
        Initialize the BinanceOffline class.
        :param config: Configuration dictionary
        :param validate: Validate the config
        """
        # Initialize the parent class without connecting to the exchange
        super(Exchange, self).__init__(config, validate=validate)
        
        # Override _ft_has and _ft_has_futures to disable features that require network requests
        self._ft_has.update({
            "stoploss_on_exchange": False,
            "ws_enabled": False,
        })
        
        self._ft_has_futures.update({
            "ws_enabled": False,
        })
        
        # Override markets to avoid loading from exchange
        self.markets = {}
        
        # Override currencies to avoid loading from exchange
        self.currencies = {}
        
        # Override precision to avoid loading from exchange
        self.precision = {}
        
        # Override fees to avoid loading from exchange
        self.fees = {}
        
        # Override timeframes to avoid loading from exchange
        self.timeframes = {}
        
        # Override required_candle_call_count to avoid loading from exchange
        self.required_candle_call_count = 1
        
        # Override exchange_has to avoid checking exchange features
        self.exchange_has = {}
        
        # Override markets_loading to avoid loading markets
        self.markets_loading = False
        
        # Override markets_loaded to avoid loading markets
        self.markets_loaded = True
        
        # Override _api to avoid making network requests
        self._api = None
        
        # Override _api_async to avoid making network requests
        self._api_async = None
        
        # Override _loop to avoid making network requests
        self._loop = None
        
        # Override _loop_lock to avoid making network requests
        self._loop_lock = None
        
        # Override _last_markets_refresh to avoid refreshing markets
        self._last_markets_refresh = datetime.now()
        
        # Override _last_ws_update to avoid refreshing markets
        self._last_ws_update = datetime.now()
        
        # Override _last_ws_ping to avoid refreshing markets
        self._last_ws_ping = datetime.now()
        
        # Override _ws_state to avoid refreshing markets
        self._ws_state = {}
        
        # Override _ws_state_lock to avoid refreshing markets
        self._ws_state_lock = None
        
        # Override _ws_state_cond to avoid refreshing markets
        self._ws_state_cond = None
        
        # Override _ws_state_thread to avoid refreshing markets
        self._ws_state_thread = None
        
        # Override _ws_state_thread_lock to avoid refreshing markets
        self._ws_state_thread_lock = None
        
        # Override _ws_state_thread_cond to avoid refreshing markets
        self._ws_state_thread_cond = None

    def get_tickers(
        self,
        symbols: Optional[List[str]] = None,
        *,
        cached: bool = False,
        market_type: Optional[TradingMode] = None,
    ) -> Tickers:
        """
        Override get_tickers to return empty dict instead of making network requests.
        :param symbols: List of symbols to get tickers for
        :param cached: Use cached data
        :param market_type: Market type
        :return: Empty dict
        """
        return {}

    def get_historic_ohlcv(
        self,
        pair: str,
        timeframe: str,
        since_ms: int,
        candle_type: CandleType,
        is_new_pair: bool = False,
        until_ms: Optional[int] = None,
    ) -> DataFrame:
        """
        Override get_historic_ohlcv to return empty DataFrame instead of making network requests.
        :param pair: Pair to get data for
        :param timeframe: Timeframe
        :param since_ms: Since timestamp in milliseconds
        :param candle_type: Candle type
        :param is_new_pair: Is new pair
        :param until_ms: Until timestamp in milliseconds
        :return: Empty DataFrame
        """
        logger.info(f"Returning empty DataFrame for {pair} {timeframe} {candle_type}")
        return DataFrame(columns=DEFAULT_DATAFRAME_COLUMNS)

    def get_historic_ohlcv_fast(
        self,
        pair: str,
        timeframe: str,
        since_ms: int,
        candle_type: CandleType,
        is_new_pair: bool = False,
        until_ms: Optional[int] = None,
    ) -> DataFrame:
        """
        Override get_historic_ohlcv_fast to return empty DataFrame instead of making network requests.
        :param pair: Pair to get data for
        :param timeframe: Timeframe
        :param since_ms: Since timestamp in milliseconds
        :param candle_type: Candle type
        :param is_new_pair: Is new pair
        :param until_ms: Until timestamp in milliseconds
        :return: Empty DataFrame
        """
        logger.info(f"Returning empty DataFrame for {pair} {timeframe} {candle_type} (fast)")
        return DataFrame(columns=DEFAULT_DATAFRAME_COLUMNS)

    def fetch_funding_rates(self, symbols: Optional[List[str]] = None) -> Dict[str, Dict[str, float]]:
        """
        Override fetch_funding_rates to return empty dict instead of making network requests.
        :param symbols: List of symbols to get funding rates for
        :return: Empty dict
        """
        return {}

    def load_leverage_tiers(self) -> Dict[str, List[Dict]]:
        """
        Override load_leverage_tiers to return empty dict instead of making network requests.
        :return: Empty dict
        """
        return {}

    def dry_run_liquidation_price(
        self,
        pair: str,
        open_rate: float,
        is_short: bool,
        amount: float,
        stake_amount: float,
        leverage: float,
        wallet_balance: float,
        open_trades: List[Any],
    ) -> Optional[float]:
        """
        Override dry_run_liquidation_price to return None instead of making calculations.
        :param pair: Pair to calculate liquidation price for
        :param open_rate: Entry price of position
        :param is_short: True if the trade is a short, false otherwise
        :param amount: Absolute value of position size incl. leverage (in base currency)
        :param stake_amount: Stake amount - Collateral in settle currency.
        :param leverage: Leverage used for this position.
        :param wallet_balance: Amount of margin_mode in the wallet being used to trade
        :param open_trades: List of open trades in the same wallet
        :return: None
        """
        return None

    async def _async_get_trade_history_id_startup(
        self, pair: str, since: int
    ) -> Tuple[List[List], str]:
        """
        Override _async_get_trade_history_id_startup to return empty list instead of making network requests.
        :param pair: Pair to get trade history for
        :param since: Since timestamp
        :return: Empty list and "0"
        """
        return [], "0"

    async def _async_get_trade_history_id(
        self, pair: str, until: int, since: int, from_id: Optional[str] = None
    ) -> Tuple[str, List[List]]:
        """
        Override _async_get_trade_history_id to return empty list instead of making network requests.
        :param pair: Pair to get trade history for
        :param until: Until timestamp
        :param since: Since timestamp
        :param from_id: From ID
        :return: Pair and empty list
        """
        return pair, []

    def additional_exchange_init(self) -> None:
        """
        Override additional_exchange_init to do nothing instead of making network requests.
        """
        pass

    def get_proxy_coin(self) -> str:
        """
        Override get_proxy_coin to return stake currency instead of making network requests.
        :return: Stake currency
        ""
        return self._config["stake_currency"]