package main

import (
	"github.com/line/line-bot-sdk-go/linebot"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
)

func main() {
	// 전차 봇
	channelAccessToken := "LINE_ACCESS_KEY"
	channelSecret := "LINE_SECRET_KEY"

	bot, err := linebot.New(channelSecret, channelAccessToken)
	if err != nil {
		log.Fatal(err)
	}
	http.HandleFunc("/callback", func(w http.ResponseWriter, req *http.Request) {
		events, err := bot.ParseRequest(req)
		if err != nil {
			if err == linebot.ErrInvalidSignature {
				w.WriteHeader(400)
			} else {
				w.WriteHeader(500)
			}
			return
		}
		for _, event := range events {
			if event.Type == linebot.EventTypeMessage {
				data, _ := ioutil.ReadFile("/rlink.txt")
				originalContentURL := string(data)
				previewImageURL := string(data)
				if _, err := bot.ReplyMessage(
					event.ReplyToken,
					linebot.NewImageMessage(originalContentURL, previewImageURL).
						WithQuickReplies(linebot.NewQuickReplyItems(
							linebot.NewQuickReplyButton(
								"https://i.imgur.com/ZnpdqUu.png",
								linebot.NewMessageAction("電車", "電車")))),
				).Do(); err != nil {
					panic(err)
				}
			}
		}
	})
	log.Fatal(http.ListenAndServeTLS(":443", "/public.pem", "/private.pem", nil))
}
