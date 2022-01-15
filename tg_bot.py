import telebot
from Model.OrderModel import Order
from panel import panel

token =  '5059610535:AAEXE2CGwKQNMd2JUd7xuKsYMCOeGwYvcCE'
bot = telebot.TeleBot(token)



@bot.message_handler(content_types=['text'])
def read_text(message):
    
    try:
        if  len(message.text.splitlines()) < 4:
            bot.reply_to(message, "Siparişin 4 satırdan daha az olamaz. Lütfen eklemek istediğinz siparişi kontrol edip atınız.")
        else:
           
            
            order = Order.create(
                    OrderText=message.text.encode(encoding="utf-8"),
                    IsComplete=False,
                    MessageId=message.id,
                    UserId=str(message.chat.id))

            order.save()

            bot.reply_to(message, "Sıraya eklendi.")
           
            # panel()
        
            unRepliedMessages = Order.select().where((Order.IsReplied == False) & (Order.PanelId > 0))
            if(unRepliedMessages.count() > 0):
                for unRepliedMessage in unRepliedMessages:
    
                    bot.send_message(int(unRepliedMessage.UserId), str(unRepliedMessage.PanelId) + ' ' + unRepliedMessage.PanelProduct, reply_to_message_id= unRepliedMessage.MessageId)
                    query = (Order.update({Order.IsReplied: True}).where(Order.Id == unRepliedMessage.Id))
                    query.execute()

    except Exception as e:
        print(e) 

    

bot.polling(none_stop=True)
