import yaml


class ReadConfing():
    def __init__(self, path: str) -> None:
        self.data = yaml.load(open(path, "r", encoding="UTF-8"), Loader=yaml.FullLoader)

    def getconfing(self, ver_name: str):
        return self.data[ver_name]


readConfing = ReadConfing("share_game/confing.yaml")
YOTUBER_URL = readConfing.getconfing("YOTUBER_URL")
YOTUBER_API_KEY = readConfing.getconfing("YOTUBER_API_KEY")

if __name__ == "__main__":
    print(YOTUBER_URL)
    print(YOTUBER_API_KEY)
