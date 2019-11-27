from src import alpha_vantage, config

def main():
    alpha_vantage.verify_api_key(config.API_KEY)
    stock_data = alpha_vantage.get_stock_data(config.stocks, config.API_KEY)

if __name__ == "__main__":
    main()