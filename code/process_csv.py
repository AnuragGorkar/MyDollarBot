import datetime
import pandas as pd
import add
import helper
def process_csv_file(message,bot):
    try:
            chat_id = str(message.chat.id)
            path=save_file(message=message,bot=bot)
            if path!='':
                df=pd.read_csv(path)
                for index, row in df.iterrows():
                    record_date = datetime.datetime.strptime(row['date(mm/dd/yy)'],"%m/%d/%Y")
                    if record_date<=datetime.datetime.today():
                        amount_value = helper.validate_entered_amount(str(row['amount'])) 
                        if float(amount_value)>0 and str(row['category']) in helper.spend_categories:
                            record_date=record_date.strftime(helper.getDateFormat() + ' ' + helper.getTimeFormat())
                            helper.write_json(add.add_user_record(chat_id, "{},{},{}".format(str(record_date), str(row['category']), str(amount_value))))
                bot.send_message(chat_id, "Records added Successfully")

            else:
                bot.send_message(chat_id, "Sorry Could not upload the csv file.")                             
        
    except Exception as e:
        bot.send_message(chat_id, "Error ocurred while processing a file")

def save_file(message,bot):
        chat_id = str(message.chat.id)
        file_info = bot.get_file(message.document.file_id)
        file = bot.download_file(file_info.file_path)
        extension=file_info.file_path.split(".")[1]
        if extension!='csv':
            bot.send_message(chat_id, "Please upload a file with csv extension")
        else:    
            file_path = "data/{}_records.csv".format(chat_id)
            with open(file_path, mode="wb") as f:
                f.write(file)

            return file_path 

        return ''            

    
