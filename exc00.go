package main

type Message struct {
	Text   string `json:"text"`
	ChatID string `json:"chatId"`
}

type Chat struct {
	ChatID      string `json:"chatId"`
	MessageList []Message
}

type Handler struct {
	ChatList            map[string]*Chat // chatID, *Chat
	receivedMessageChan chan Message     // channel with all incoming payloads
    
    if dest := metadata["chatId"]; dest != nil {

        tmpTextMessage := PayloadToGraphqlTextMessage(message)
        h.chatList[dest.(string)].MessagesChan <- &tmpTextMessage

        h.chatList[dest.(string)].TextMessageList = append(h.chatList[dest.(string)].TextMessageList, &tmpTextMessage)
    
}

func NewHandler() *Handler {
	return &Handler{
		ChatList:            make(map[string]*Chat),
		receivedMessageChan: make(chan Message),
	}
}

// Handler.handle() handles incoming messages
func (h *Handler) Handle() error {
	// on every new Message in chan
	for message := range h.receivedMessageChan {
		// TODO handle incoming messages
		//  if chatid of message is in list of all chats add it to particular chat
		//  otherwise return error
		//  tip: check if key exists in map
		println(message.Text)
		panic("implement me")
	}
	return nil
}
