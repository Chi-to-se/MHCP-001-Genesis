import time
from datetime import datetime 
from colorama import Fore, Style, init
from textblob import TextBlob

#Initialize colorama
init(autoreset=True)

#Initialize colorama
init(autoreset=True)

class MHCP_System:
    def __init__(self):
        self.system_name = "MHCP-001"
        self.version = "0.1.0 (Prototype)"
        self.user_name =  "Admin"

        #Boot System
        print(f"{Fore.CYAN}Initializing {self.system_name} Kernel...{Style.RESET_ALL}")
        time.sleep(0.5)
        print(f"{Fore.CYAN}Loading Language Modules... [TextBlob]{Style.RESET_ALL}")
        time.sleep(0.5)
        print(f"{Fore.GREEN}System Online. Version: {self.version}{Style.RESET_ALL}")
        print("-" * 60)

    #Get now time
    def get_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #Analyze emotion
    def analyze_sentiment(self, text):
        """
        Analyze text sentiment using TextBlob.
        ReturnL polarity score (-1.0 to 1.0)
        """
        blob = TextBlob(text)
        return blob.sentiment.polarity 

    #Logging
    def log_response(self, message, polarity):
        ts = self.get_timestamp()
        
        #Scoring
        if polarity > 0.3:
            status = "Positive"
            color_res = Fore.GREEN
            sys_msg = "Psychological Hue: Green. Mental State Optimal."
        elif polarity < -0.3:
            status = "Negative"
            color_res = Fore.RED
            sys_msg = "WARNING: Psychological Hue: Red. Stress detected."
        else:
            status = "Neutral"
            color_res = Fore.YELLOW
            sys_msg = "Psychological Hue: Grey. State Stable."

        print(f"\n{Fore.MAGENTA}[LOG] {ts} >> INCOMING SIGNAL")
        print(f"{Fore.WHITE}Input: {message}")
        time.sleep(0.3)
        print(f"{color_res}[ANALYSIS] Status: {status} | Score: {polarity:.4f}")
        print(f"{Fore.CYAN}>> Cardinal: {sys_msg}")
        print(f"{Fore.BLACK}{Fore.WHITE} [ RECORDED ] {Style.RESET_ALL}")
        print("-" * 60)

    #Main
    def run(self):
        print(f"\n{Fore.YELLOW}Waiting for input... (Type 'logout' to exit){Style.RESET_ALL}")
        while True:
            try:
                user_input = input(f"{Fore.BLUE}Command > {Style.RESET_ALL}")

                if user_input.lower() in ["exit", "logout", "quit"]:
                    print(f"{Fore.CYAN}System Shutdown. Good luck, {self.user_name}.{Style.RESET_ALL}")
                    break

                if user_input.strip():
                    score = self.analyze_sentiment(user_input)
                    self.log_response(user_input, score)

            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Forced Shutdown.{Style.RESET_ALL}")
                break

if __name__ == "__main__":
    app = MHCP_System()
    app.run()