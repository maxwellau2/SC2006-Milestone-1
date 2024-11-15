import requests
from datetime import datetime, timedelta


class telegramBot:
    def __init__(self, botToken: str, chatID: str, graphDirectory: str = ""):
        """
        If you got any problems drop me a telegram message at @Maaxweel
        botToken : api bot token given by bot father @BotFather on telegram,
        chatTd : chat id as assigned by user, you can find your unique chatid at api.telegram.org/bot{bottoken}/getUpdates, send a message and refresh,
        graphDirectory : default value is an empty string, use if you inte nd to send plotly.graph_objs.Figure graphs
        """
        self.botToken = botToken
        self.chatID = chatID
        self.graphDirectory = graphDirectory

    def sendText(self, msg: str) -> bool:
        """
        msg : message in string format
        """
        base_url = f"https://api.telegram.org/bot{self.botToken}/sendMessage?chat_id={self.chatID}&text={msg}"
        requests.post(base_url)  # Sending automated message
        return True

    def sendTextToChatID(self, msg: str, chatid: str) -> bool:
        """
        msg : message in string format
        """
        base_url = f"https://api.telegram.org/bot{self.botToken}/sendMessage?chat_id={chatid}&text={msg}"
        requests.post(base_url)  # Sending automated message
        return True

    def downloadImage(self, url: str, filename: str) -> None:
        """
        Downloads an image from the provided URL and saves it with the given filename.
        """
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Image downloaded successfully as {filename}")
        else:
            print("Failed to download image.")

    def pollResponse(self, specificity: bool, wait_time: int):
        """
        specificity : set to true if you want to listen ONLY to the chatid user, false if you want to listen to all users
        wait_time : wait time in seconds
        """
        assert (
            "-" not in self.chatID
        ), "ChatID is that of a Channel, unable to poll for responses"
        site = f"https://api.telegram.org/bot{self.botToken}/getUpdates"
        data = requests.get(site).json()  # reads data from the url getUpdates
        chatid = ""
        try:
            lastMsg = len(data["result"]) - 1
            updateIdSave = data["result"][lastMsg]["update_id"]
        except:
            updateIdSave = ""
        time = datetime.now()
        waitTime = time + timedelta(seconds=wait_time)

        while True:
            try:
                time = datetime.now()
                data = requests.get(site).json()  # reads data from the url getUpdates
                lastMsg = len(data["result"]) - 1
                updateId = data["result"][lastMsg]["update_id"]
                chatid = str(
                    data["result"][lastMsg]["message"]["chat"]["id"]
                )  # reads chat ID
                if specificity:
                    condition = self.chatID == chatid
                else:
                    condition = True
                if updateId != updateIdSave and condition:  # compares update ID
                    message_type = data["result"][lastMsg]["message"].get("photo")
                    if message_type:
                        file_id = message_type[-1]["file_id"]
                        file_info = requests.get(
                            f"https://api.telegram.org/bot{self.botToken}/getFile?file_id={file_id}"
                        ).json()
                        file_path = file_info["result"]["file_path"]
                        file_url = f"https://api.telegram.org/file/bot{self.botToken}/{file_path}"

                        # image_filename = os.path.basename(file_path)
                        # download_link = f'<a href="{file_url}">{image_filename}</a>'
                        requests.get(
                            f"https://api.telegram.org/bot{self.botToken}/getUpdates?offset="
                            + str(updateId)
                        )
                        return {"type": "image", "url": file_url, "chatid": chatid}
                    else:
                        text = data["result"][lastMsg]["message"][
                            "text"
                        ]  # reads what they have sent
                        requests.get(
                            f"https://api.telegram.org/bot{self.botToken}/getUpdates?offset="
                            + str(updateId)
                        )
                        break

                elif waitTime < time:
                    text = ""
                    chatid = ""
                    break
            except Exception as e:
                print("Error:", e)
                text = ""
                break
        return {"type": "text", "content": text, "chatid": chatid}
