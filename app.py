# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi('') #Your Channel Access Token
handler = WebhookHandler('') #Your Channel Secret

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(PostbackEvent)
def handle_text_message(event):
    print event.postback.data

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)

    text = event.message.text #message from user

    if text.lower().strip() == "show-me-button":
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://www.everrich-group.com/Upload/fe5ac954-dcc5-479e-8cbe-ffa90cf14d41/TC/cover.jpg',
                title='Menu',
                text='Please select',
                actions=[
                    PostbackTemplateAction(
                        label='postback',
                        text='postback text',
                        data='action=buy&itemid=1'
                    ),
                    MessageTemplateAction(
                        label='message',
                        text='message text'
                    ),
                    URITemplateAction(
                        label='uri',
                        uri='http://example.com/'
                    )
                ]
            )
        ))
    elif text.lower().strip() == "show-me-slideshow":
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://www.everrich-group.com/Upload/fe5ac954-dcc5-479e-8cbe-ffa90cf14d41/TC/cover.jpg',
                        title='Menu1',
                        text='Desc1',
                        actions=[
                            PostbackTemplateAction(
                                label='Purchase',
                                text=profile.display_name + ' thank you for buying this',
                                data='data=1'
                            ),
                            MessageTemplateAction(
                                label='Detail',
                                text='This is a great tea'
                            ),
                            URITemplateAction(
                                label='U1',
                                uri='http://abc.com/1'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://www.everrich-group.com/Upload/fe5ac954-dcc5-479e-8cbe-ffa90cf14d41/TC/cover.jpg',
                        title='Menu2',
                        text='Desc2',
                        actions=[
                            PostbackTemplateAction(
                                label='Purchase',
                                text=profile.display_name + ' thank you for buying this',
                                data='data=2'
                            ),
                            MessageTemplateAction(
                                label='Detail',
                                text='This is the best tea'
                            ),
                            URITemplateAction(
                                label='U2',
                                uri='http://abc.com/2'
                            )
                        ]
                    )
                ]
            )
        ))
    else:
        print text
        #line_bot_api.reply_message(
        #    event.reply_token,
        #    TextSendMessage(text=text)) #reply the same message from user
    

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])
