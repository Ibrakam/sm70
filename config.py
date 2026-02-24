from dotenv import dotenv_values


config_values = dotenv_values(".env") #{"ALGORTIHM": HS256}


algorithm = config_values["ALGORTIHM"]
secret_key = config_values["SECRET_KEY"]
accexx_token_exp_min = int(config_values["ACCESS_TOKEN_EXPIRE_MINUTES"])
