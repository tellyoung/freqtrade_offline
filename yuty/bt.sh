python freqtrade/main.py backtesting \
--config yuty/user_data/configs/open03/config_open03_futures.json \
--userdir yuty/user_data \
--strategy open03 \
--breakdown week month \
--strategy-path yuty/user_data/strategies \
--recursive-strategy-search \
--datadir /Users/yutieyang/Documents/yuty/yuty_projects/money_game/Datasets/binance/Vol_top20_202501_202506 \
--timerange 20250501-20250707


#freqtrade create-userdir --userdir /Users/yutieyang/Documents/yuty/yuty_projects/freqtrade_offline/yuty/user_data


python freqtrade/main.py backtesting --config yuty/user_data/configs/open03/config_open03_futures.json --userdir yuty/user_data --strategy open03 --breakdown week month --strategy-path yuty/user_data/strategies --recursive-strategy-search --datadir /Users/yutieyang/Documents/yuty/yuty_projects/money_game/Datasets/binance/Vol_top20_202501_202506 --timerange 20250501-20250707