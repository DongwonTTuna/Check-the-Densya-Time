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
	channelAccessToken := "htPV5d5FPpYbt535I4Ol41e+0cruvp35rb+uf6fU8wKS7smSRIkm6wc06/QF97ltihl99BzlCoEIOF8ah9E5qlu2dQh89u8lIBmicZ2h5D45rG2yXEjHQw+b1mKm/BuLWwOTmPod4kdKs2lRv+XEiwdB04t89/1O/w1cDnyilFU="
	channelSecret := "ebe3ff3872ffff29d981bb24a2a737d9"

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
	log.Fatal(http.ListenAndServeTLS(":443", "/home/opc/public.pem", "/home/opc/private.pem", nil))
}
