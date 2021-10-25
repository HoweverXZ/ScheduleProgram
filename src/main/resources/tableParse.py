"""
    @author: HoweverXz
    @Date: 2021/10/21
    纸上得来终觉浅 绝知此事要躬行
"""
import bs4
from pyquery import PyQuery as pq


class tableParser:
    def __init__(self, html: bs4.element.Tag):
        self.html = html
        self.info = {
            'courseInfos': [{
                'name': '',
                'position': '',
                'teacher': '',
                'weeks': [],
                'day': '',
                'sections': []}
            ],
            "sectionTimes": [
                {
                    "section": 1,
                    "startTime": "07:40",
                    "endTime": "08:25"
                },
                {
                    "section": 2,
                    "startTime": "08:35",
                    "endTime": "09:20"
                },
                {
                    "section": 3,
                    "startTime": "09:45",
                    "endTime": "10:25"
                },
                {
                    "section": 4,
                    "startTime": "10:35",
                    "endTime": "11:20"
                },
                {
                    "section": 5,
                    "startTime": "14:40",
                    "endTime": "15:25"
                },
                {
                    "section": 6,
                    "startTime": "15:35",
                    "endTime": "16:20"
                },
                {
                    "section": 7,
                    "startTime": "16:45",
                    "endTime": "17:25"
                },
                {
                    "section": 8,
                    "startTime": "17:35",
                    "endTime": "18:20"
                },
                {
                    "section": 9,
                    "startTime": "19:30",
                    "endTime": "20:15"
                },
                {
                    "section": 10,
                    "startTime": "20:25",
                    "endTime": "21:10"
                },

            ]
        }

    def tableParse(self, ):
        self.add("name", "position", "teacher", [], "day", [])
        return self.info

    def add(self, name: str, position: str, teacher: str, weeks: [], day: str, sections: []):
        # 重新命名方便处理
        self.info['courseInfos'].append({
            'name': name,
            'position': position,
            'teacher': teacher,
            'weeks': weeks,
            'day': day,
            'sections': sections})

    def parse(self):
        del self.info['courseInfos'][0]
        num = 0
        # 数据处理区
        element = self.html.find_all(class_="kbcontent")
        for i in element:
            result = pq(str(i))
            if result.text() != "":
                res = result.text().strip().split("\n")
                res = [i for i in res if i != ""]
                if len(res) % 7 == 6 or len(res) % 6 == 0:
                    for a in range(0, len(res), 7):
                        name = res[a] + res[a + 1]
                        teacher = res[a + 2]
                        weeksandsections = res[a + 3].split(')[')
                        weeks = self.weekParser(weeksandsections[0])
                        sections = self.sectionParser(weeksandsections[1])
                        position = res[a + 4] + res[a + 5]
                        self.add(name, position, teacher, weeks, str(num), sections)
                else:
                    for a in range(0, len(res), 6):
                        name = res[a]
                        teacher = res[a + 1]
                        weeksandsections = res[a + 2].split(')[')
                        weeks = self.weekParser(weeksandsections[0])
                        sections = self.sectionParser(weeksandsections[1])
                        position = res[a + 3] + res[a + 4]
                        self.add(name, position, teacher, weeks, str(num), sections)

    def weekParser(self,weeks: str):
        result = []
        raw = weeks.replace('(周', '').split(',')
        for i in raw:
            if i.find('-') == -1:
                result.append(i)
            else:
                begin = i.split('-')[0]
                end = i.split('-')[1]
                for ranges in range(int(begin), int(end) + 1):
                    result.append(ranges)
        return result

    def sectionParser(self,sections: str):
        return [int(i) for i in sections.replace('节]', '').split('-')]
