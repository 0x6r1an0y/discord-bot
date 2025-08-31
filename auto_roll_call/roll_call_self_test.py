import asyncio
from .roll_call import test_wrapper #多加一個點才可以讓他讀到roll_call不知道為什麼
import multiprocessing
from concurrent.futures.thread import ThreadPoolExecutor
#auto py to exe ->Manual Argument Input-> --collect-data grapheme


normal_url = "https://itouch.cycu.edu.tw/active_system/query_course/learning_activity_stulogin.jsp?act_no=15ce5f9e-5f1c-47be-89af-ad160ccc3dc5"
terminate_url = "https://itouch.cycu.edu.tw/active_system/query_course/learning_activity_stulogin.jsp?act_no=9b429952-0f3e-474e-b5e8-f0c8875bb877"
test_data = [[normal_url,[["11012345","10912345","10912346"],["123456789","123456789","123456789"],["暱稱1","暱稱2","暱稱3"],False]],
            [normal_url,[['11012345'],['123456879'],['測試'],False]],
            [terminate_url,[['11012345'],['123456879'],['測試'],False]],
            [normal_url,[['11012345'],['12345678'],['測試'],False]]]




#    multiprocessing.Pool(os.cpu_count()).map(test_wrapper, test_data)
        # 同官方文件所述 map 和 starmap 差別僅在於能否傳入 Multi-args 多參數到同一個 function 內


async def roll_call_test():
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor() # 初始化线程池
    tasks = []
    for i, data in enumerate(test_data):
        task = loop.run_in_executor(executor, await test_wrapper(data))
        tasks.append(task)
    #print(tasks)
    loop.run_until_complete(asyncio.wait(tasks)) # 异步调用
    #for i, data in enumerate(test_data):
    #    await test_wrapper(data)
