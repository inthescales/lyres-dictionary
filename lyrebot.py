import lyre
from botbuddy import BotBuddy

credentials = {
    BotBuddy.creds_file_key : "creds.json"
}
    
buddy = BotBuddy()
buddy.setup(lyre.write_entry, interval="1h", retry=True, credentials=credentials)
buddy.launch()
