import lyre
from botbuddy import BotBuddy

credentials = {
    BotBuddy.creds_file_key : "creds.json"
}
    
buddy = BotBuddy()
buddy.setup(lyre.generate_entry, retry=True, credentials=credentials)
buddy.post()
