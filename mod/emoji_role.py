#無法做僅限自己看到的訊息，限制於交互活動
#dictionary 構成:{'emoji':[id,name]}
#如果要使用something[0][0][1]的方式跟物件調用就必須將dict轉換為list
data_dict = {
'⛏️' :[1026376824978149376,"礦工"],
'🫢'   :[1026574918906810458,"啞巴"],
'💿' :[675247066020052992,"DJ"],
'💃' :[838500128385269842,"美女"],
'🕺' :[838499612276424785,"帥哥"],
'🤵‍♂️' :[831831497120022528,"紳士"],
'🤮' :[1011280769773215814,"處男"],
'👃' :[838500913479680062,"大GG"]
}

def know_emoji_find_id(emoji)->int:
    try:
        return data_dict[emoji][0]#id
    except KeyError:#當在字典的key找不到emoji時
        return 0
    

def know_emoji_find_name(emoji)->str:
    try:
        return data_dict[emoji][1]#name
    except KeyError:#當在字典的key找不到emoji時
        return 0


def know_id_find_emoji(id)->str:
    __data_list = list(data_dict.items())#dictionary物件強迫轉為List
    for i in range(0,len(__data_list)):
        try:
            if __data_list[i][1][0] == id:#id
              return __data_list[i][0]#emoji
        except KeyError:#當在字典的key找不到id時
            return 0

def know_id_find_name(id)->str:
    __data_list = list(data_dict.items())#dictionary物件強迫轉為List
    for i in range(0,len(__data_list)):
        try:
            if __data_list[i][1][0] == id:#id
              return __data_list[i][1][1]#name
        except KeyError:#當在字典的key找不到id時
            return 0

def know_name_find_id(name)->int:
    __data_list = list(data_dict.items())#dictionary物件強迫轉為List
    for i in range(0,len(__data_list)):
        try:
            if __data_list[i][1][1] == name:#name
              return __data_list[i][1][0]#id
        except KeyError:#當在字典的key找不到name時
            return 0


def know_name_find_emoji(name)->str:
    __data_list = list(data_dict.items())#dictionary物件強迫轉為List
    for i in range(0,len(__data_list)):
        try:
            if __data_list[i][1][1] == name:#name
              return __data_list[i][0]#emoji
        except KeyError:#當在字典的key找不到name時
            return 0