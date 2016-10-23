from kino.template import MsgTemplate
from slack.slackbot import SlackerAdapter
from utils.resource import MessageResource

class Guide(object):

    def __init__(self):
        self.slackbot = SlackerAdapter()
        self.template = MsgTemplate()

    def help(self):
        attachments = self.template.make_help_template(self.__guide(), self.__example())
        self.slackbot.send_message(attachments=attachments)

    def __guide(self):
        guide_msg = "Kino는 Slack Bot으로 기본으로 개발된 Personal Assistant A.I 입니다.\n"
        guide_msg += "필요한 기능이 있으면 그때그때 개발하면서 똑똑해지고 있습니다.\n"
        guide_msg += "현재는 시간에 따라 실행하고자 하는 함수를 등록할 수 있고, 입력에 따른 답을 하는 수준입니다..\n\n"
        guide_msg += "아래 사용할 수 있는 기능 예시들 입니다. "
        return guide_msg

    def __example(self):
        example = {
            "Greeting": "키노야 안녕",
            "Worker": "키노야 일 하자",
            "Notifier": "알람 등록해줘, 알람 보여줘, 알람 삭제",
            "Between": "시간대 추가해줘, 시간대 보자, 시간대 제거해줘",
            "Functions": "함수 보여줘",
            "Weather": "날씨 알려줘, 날씨 어때?"
        }
        return example