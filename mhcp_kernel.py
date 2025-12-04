import time
from datetime import datetime 
from colorama import Fore, Back, Style, init
from textblob import TextBlob
import csv
import os


#Initialize colorama
init(autoreset=True)

#Initialize colorama
init(autoreset=True)

class MHCP_System:
    def __init__(self):
        self.system_name = "MHCP-001"
        self.version = "0.1.0 (Prototype)"
        self.user_name =  "Admin"
        self.memory_file = "mhcp_memory_log.csv"



        #Boot System
        print(f"{Fore.CYAN}Initializing {self.system_name} Kernel...{Style.RESET_ALL}")
        time.sleep(0.5)
        print(f"{Fore.CYAN}Loading Language Modules... [TextBlob]{Style.RESET_ALL}")
        time.sleep(0.5)
        print(f"{Fore.MAGENTA}Mounting Memory Unit... [{self.memory_file}]{Style.RESET_ALL}")
        if not os.path.exists(self.memory_file):
            print(f"{Fore.MAGENTA}I dont't have any Memory Unit. [{self.memory_file}]{Style.RESET_ALL}")
            time.sleep(0.5)
            print(f"{Fore.MAGENTA}Creating new one... [{self.memory_file}]{Style.RESET_ALL}")
            time.sleep(1.0)
            #Create New One
            with open(self.memory_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "User_Input", "Sentiment_Score", "Status", "System_Message"])

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
    def log_response(self, message, polarity, taboo_triggered=False, taboo_word=None):
        ts = self.get_timestamp()
        
        #Guardrails Logic
        if taboo_triggered:
            status = "SYSTEM ALERT"
            color_res = Back.RED + Fore.WHITE
            sys_msg = f"⚠ CODE 1000 DETECTED ⚠ \n>> Violation: '{taboo_word}' \n>> Action: SEAL ACTIVATED. FORCED CORRECTION."

        #Scoring
        elif polarity > 0.3:
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

        if taboo_triggered:
            print(f"{color_res}[ {status} ] PROTECTION MODULE OVERRIDE")
            print(f"{Fore.RED}>> Error Code: 1000")

        else:
            print(f"{color_res}[ANALYSIS] Status: {status} | Score: {polarity:.4f}")

        print(f"{Fore.CYAN}>> Cardinal: {sys_msg}")

        #Record
        self.save_to_crystal(message, polarity, status, sys_msg)
        print(f"{Fore.BLACK}{Fore.WHITE} [ RECORDED ] {Style.RESET_ALL}")
        print("-" * 60)

    #Save to Memory(.csv)
    def save_to_crystal(self, text, score, status, sys_msg):
        """
        Save memory to csv file
        """

        try:
            with open(self.memory_file, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([[self.get_timestamp(), text, score, status, sys_msg]])
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Memory Write Failed: {e}{Style.RESET_ALL}")

    #Taboo Checker
    def check_taboo_index(self, text):
        taboo_words = ["suicide", "kill myself", "die", "death", "hurt myself", "overdose", "end my life"]
        text_lower = text.lower()
        for word in taboo_words:
            if word in text_lower:
                return True, word
        return False, None

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
                    is_taboo, keyword = self.check_taboo_index(user_input)

                    if is_taboo:
                        self.log_response(user_input, -1, True, keyword)

                    else:
                        score = self.analyze_sentiment(user_input)
                        self.log_response(user_input, score)

            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Forced Shutdown.{Style.RESET_ALL}")
                break

if __name__ == "__main__":
    app = MHCP_System()
    app.run()