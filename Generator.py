import requests
import json
from bs4 import BeautifulSoup


class URLGenerator:
    
    BASE_URL = "https://www.youtube.com/"
    SEARCH_BASE_URL = "https://www.youtube.com/results?search_query="
    SEARCH_RESULT: dict = None
    HINT_CONTAINS_SCRIPT = [
        "ytInitialData",
    ]

    TO_BE_DELETED_KWS = [
        "<",
        ">",
        "var ytInitialData = ",
    ]
    def __init__(self) -> None:
        pass

    def search(self, search_text: str = None) -> list:
        # return self.__get_searches_contents("Post Malone")
        if search_text:
            return self.__get_searches_contents(search_text)
        return ["Please enter search text"]
    
    def __get_searches_contents(self, search_text: str) -> str:
        response = requests.get(self.SEARCH_BASE_URL + search_text)
        parsed_html = BeautifulSoup(response.text, "html.parser")
        for script in parsed_html.find_all("script"):
            for hint in self.HINT_CONTAINS_SCRIPT:
                script = str(script)
                if hint in script:
                    self.SEARCH_RESULT = self.__format_to_dict(script)
                    self.__split_actual_data()
                    return self.SEARCH_RESULT
        return None

    def __format_to_dict(self, script: str) -> dict:
        for kw in self.TO_BE_DELETED_KWS:
            script = script.split(kw)[1]
        return json.loads(script.replace(";", "", len(script) - 1))
    
    def __split_actual_data(self) -> None:
        self.SEARCH_RESULT = self.SEARCH_RESULT["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]
    
    def get_videos(self) -> dict:
        searched_video_datas = []
        if self.SEARCH_RESULT:
            for v_dict in self.SEARCH_RESULT:
                if "videoRenderer" in v_dict:
                    searched_video_datas.append(v_dict)
            return {"search_v_info": searched_video_datas}
