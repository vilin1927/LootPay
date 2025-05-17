from environs import Env

# Initialize environment variables
env = Env()
env.read_env()

# Bot configuration
BOT_TOKEN = env.str("BOT_TOKEN")
ADMIN_IDS = list(map(int, env.list("ADMIN_IDS"))) 