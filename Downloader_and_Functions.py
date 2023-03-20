
from queue import Queue
import youtube_dl
import time

#  global variables to store data and pass update-info to the Gui
progress_que = 0
finished_display_number = 0
url_download_que = Queue(maxsize=1000)  # program will stop if this number is reached
file_extensions = [".mp3", ".wav", ".mp4"]  # same order as gui, values are 0, 1, 2
download_status = ["Download info will be displayed here"]
finished = []


# url_download_que.put("https://www.youtube.com/watch?v=8x8C4at_J_8") #  TESTE OM QUE FUNKER

class MyLogger(object):
    def debug(self, msg):
        print(msg, "debuggg")
        update_download_status(msg)
        # Gui.App.write_download_prog_textbox(object, msg)
        pass

    def warning(self, msg):
        print(msg, "warning")

    def error(self, msg):
        print(msg, "error")
        # os.system('youtube-dl --rm-cache-dir')
        update_download_status("#SYSTEM cache deleted")
        print("NÅ ER CACHE SLETTET NICEE DENNE FUNKER")


'''def test(entry_url, file_type_value):
    print("called test", entry_url)
    time.sleep(5)
    test = "https://www.youtube.com/watch?v=8x8C4at_J_8"  # only test
    que_url(test)  # inserted url
    que_url(test)  # inserted url
    que_url(test)  # inserted url
    que_url(test)  # inserted url
    que_url(test)  # inserted url
    que_url(test)  # inserted url
    que_url(test)  # inserted url
    que_url(test)  # inserted url

    print("test - qsize", url_download_que.qsize())
    file_type = get_file_type_value(file_type_value)
    download_que(file_type)
'''


def check_url_entry(url):
    if "https://www.youtube.com" in url:
        print("check_url_entry Passed")
        return True  # check of domain name
    else:
        update_download_status("Not an youtube URL"), print("Not an youtube URL")


def que_url(url):
    print("called que url", url)
    url = url.replace(' ', '')  # removes potential whitespace
    if check_url_entry(url):
        global url_download_que
        url_download_que.put(url)
    pass


def get_file_type_value(file_type_value):
    print("called get_file_type_value", file_type_value)
    value = file_type_value.get()
    file_type = file_extensions[value]
    # print(file_type)
    return file_type


def yt_downloader(url, file_type):  # uncomplete resten ligg på andre filen
    print("Called yt_downloader (sleep 5)")
    video_url = str(url)
    video_info = youtube_dl.YoutubeDL().extract_info(url=video_url, download=False)

    print("video info", video_info)
    filename = f"{video_info['title']}{file_type}"
    update_msg = "started downloading...", filename
    update_download_status(update_msg)
    time.sleep(1)

    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filename,
        'logger': MyLogger()
    }

    print("FILENAME:   ", filename)
    finished.append(filename)
    print("filename finshied: ", finished)
    return ("FILENAME:   ", filename), finished


def download_que(file_type):
    global url_download_que
    que = url_download_que
    while que.qsize() > 0:
        url = que.get()
        update_msg = "started downloading... ", url, " as ", file_type
        update_download_status(update_msg)
        yt_downloader(url, file_type)
        update_msg = "Complete"
        update_download_status(update_msg)

        print("en while loop")
        # write ut noe info her
        # Gui.App().updater()


def update_progress_que(progress_que_change):
    global progress_que
    progress_que += progress_que_change
    return progress_que


def update_finished_number(finished_update):
    print("update_finshied_number er called")
    global finished_display_number
    finished_display_number += finished_update
    print(finished_display_number)
    return finished_display_number


def download_handler(entry_url, file_type_value):
    print("Called Download_handler", entry_url)
    if not check_url_entry(entry_url):  # url check
        return "URL domain check ERROR, check supported domain"
    update_progress_que(1)  # add one to display number of downloads in gui
    file_type = get_file_type_value(file_type_value)
    update_msg = "started downloading... ", entry_url, " as ", file_type
    update_download_status(update_msg)
    try:
        download = yt_downloader(entry_url, file_type)
    except:
        # checks if the download var is assigned, if it not assigned an Error accured in yt_downloader()
        if 'download' not in locals():
            update_msg = f"{'Something went wrong with the yt_downloader, please check URL entry: '}\n{entry_url}"
    else:
        update_finished_number(1)
        update_msg = "Complete"
    finally:
        update_progress_que(-1)
        update_download_status(update_msg)


def update_download_status(msg):
    global download_status
    download_status.clear()
    download_status.append(msg)
    pass
