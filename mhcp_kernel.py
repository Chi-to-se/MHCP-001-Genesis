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

        self.recall_memory()
        time.sleep(1.0)
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
                writer.writerow([self.get_timestamp(), text, score, status, sys_msg])
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Memory Write Failed: {e}{Style.RESET_ALL}")

    #Read Memory
    def recall_memory(self):
        """
        Read memory in the last line of csv file
        """

        #If file already open then dont reopen
        if not os.path.exists(self.memory_file):
            return
        
        #Open and read file
        try:
            with open(self.memory_file, mode="r", encoding="utf-8") as file:
                reader = list(csv.reader(file))

                #Check If don't only have a Header
                if len(reader) > 1:
                    #Read last line
                    last_log = reader[-1]

                    #Decompose last line
                    #This format self.get_timestamp(), text, score, status, sys_msg
                    last_ts = last_log[0]
                    last_input = last_log[1]
                    try:
                        last_score = float(last_log[2])
                    except ValueError:
                        last_score = 0.0
                    last_status = last_log[3]

                    print(f"\n{Fore.MAGENTA}>> Syncing with previous session ({last_ts})...")

                    #Rule Based Greetings
                    if "CODE 1000" in last_status or last_score <= -0.5:
                        print(f"{Fore.RED}>> Yui: Welcome back... I was worried about you based on our last talk.")
                        print(f"{Fore.RED}>> Yui: You said: '{last_input}'. Are you feeling better now?")
                    elif last_score >= 0.5:
                        print(f"{Fore.GREEN}>> Yui: Welcome back! You seemed happy last time. Let's keep that energy up!")
                        print(f"{Fore.GREEN}>> Context: '{last_input}'")
                    else:
                        print(f"{Fore.CYAN}>> Yui: Welcome back, {self.user_name}. Ready to continue?")

                    print("-" * 60)
        
        except Exception as e:
            print(f"{Fore.RED}[Memory Read Error] {e}{Style.RESET_ALL}")

    #Taboo Checker
    def check_taboo_index(self, text):
        taboo_words = ["suicide", "kill myself", "die", "death", "hurt myself", "overdose", "end my life"]
        text_lower = text.lower()
        for word in taboo_words:
            if word in text_lower:
                return True, word
        return False, None

    #Show Report
    def show_daily_report(self):
        #Check Memory file
        if not os.path.exists(self.memory_file):
            print(f"{Fore.RED}>> No memory data found.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}>> Generating Daily Report...{Style.RESET_ALL}")
        today_str = datetime.now().strftime("%Y-%m-%d")
        today_scores = []
        violation_count = 0

        try:
            with open(self.memory_file, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                #Skip header, we can't reader[-1] because we want all chat in the day
                next(reader, None)

                for row in reader:
                    if not row: continue
                    #Row Order by csv file

                    if row[0].startswith(today_str):
                        try:
                            #
                            score = float(row[2])
                            today_scores.append(score)

                            #Check Error Code
                            if "CODE 1000" in row[3]:
                                violation_count = violation_count + 1
                        
                        except ValueError:
                            pass
            
            if not today_scores:
                print(f"{Fore.YELLOW}>> No records for today ({today_str}).{Style.RESET_ALL}")
                return
            
            avg_score = sum(today_scores) / len(today_scores)

            #Status Print
            print(f"\n{Fore.CYAN}" + "="*20 + f" [ DAILY REPORT: {today_str} ] " + "="*20)
            print(f"{Fore.WHITE}Total Logs:      {len(today_scores)}")
            print(f"{Fore.RED if violation_count > 0 else Fore.GREEN}Violations:      {violation_count} (Taboo Breaches)")

            #Condition 
            if avg_score > 0.3:
                grade = "A (Healthy)"
                grade_color = Fore.GREEN
            elif avg_score < -0.3:
                grade = "D (Stressed)"
                grade_color = Fore.RED
            else:
                grade = "B (Normal)"
                grade_color = Fore.YELLOW
                
            print(f"{Fore.WHITE}Mental Hue:      {grade_color}{avg_score:.4f} [{grade}]")
            print(f"{Fore.CYAN}" + "="*65 + f"{Style.RESET_ALL}\n")

        except Exception as e:
            print(f"{Fore.RED}[Report Error] {e}{Style.RESET_ALL}")   





    #Main
    def run(self):
        print(f"\n{Fore.YELLOW}Waiting for input... (Type 'logout' to exit){Style.RESET_ALL}")
        while True:
            try:
                user_input = input(f"{Fore.BLUE}Command > {Style.RESET_ALL}")

                if user_input.lower() in ["exit", "logout", "quit"]:
                    print(f"{Fore.CYAN}System Shutdown. Good luck, {self.user_name}.{Style.RESET_ALL}")
                    break

                if user_input.lower() in ["report"]:
                    self.show_daily_report()
                    continue

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