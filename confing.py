import yaml


class ReadConfing():
    def __init__(self, path: str) -> None:
        self.data = yaml.load(open(path, "r", encoding="UTF-8"), Loader=yaml.FullLoader)

    def getconfing(self, ver_name: str):
        return self.data[ver_name]


def find_confing_path():
    import os

    def fing_confing(listdir, path: str):
        if "confing.yaml" in listdir:
            return os.path.join(path, "confing.yaml")
        elif "key.yaml" in listdir:
            return os.path.join(path, "key.yaml")

    listdir = os.listdir(".")
    abspath: str = os.path.abspath(".")
    confing_path = None

    if "share_game" in listdir:
        listdir_share_game = os.listdir("share_game")
        confing_path = fing_confing(
            listdir_share_game, os.path.join(abspath, "share_game")
        )
    elif "share-game" in listdir:
        listdir_share_game = os.listdir("share-game")
        confing_path = fing_confing(
            listdir_share_game, os.path.join(abspath, "share-game")
        )

    if not confing_path:
        confing_path = fing_confing(listdir, abspath)

    if confing_path:
        return confing_path
    else:

        class MissingKeyOrConfingError(Exception):
            def __str__(self) -> str:
                return "Missing key file or confing file"

        raise MissingKeyOrConfingError


confing_path = find_confing_path()
readConfing = ReadConfing(confing_path)
YOTUBER_URL = readConfing.getconfing("YOTUBER_URL")
YOTUBER_API_KEY = readConfing.getconfing("YOTUBER_API_KEY")

if __name__ == "__main__":
    print(confing_path)
    print(YOTUBER_URL)
    print(YOTUBER_API_KEY)
