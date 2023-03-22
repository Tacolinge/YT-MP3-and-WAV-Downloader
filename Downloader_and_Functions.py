import youtube_dl
import os

#  global variables to store data and pass update-info to the Gui
progress_que = 0
finished_display_number = 0
file_extensions = [".mp3", ".wav", ".mp4"]  # same order as gui, values are 0, 1, 2
download_status = ["Download info will be displayed here"]  # used for the bottom textbox in Gui
finished = []  # used for the top textbox in Gui


# url_download_que.put("https://www.youtube.com/watch?v=8x8C4at_J_8") #  TESTE OM QUE FUNKER

class MyLogger(object):
    def debug(self, msg):  # show download  % and ETA
        update_download_status(msg)

    def warning(self, msg):
        print(msg, "warning")

    def error(self, msg):
        print(msg, "error")
        os.system('youtube-dl --rm-cache-dir')  # this deals with the 403 forbidden error
        update_download_status("-System cache deleted, please try the url again")
        print("-System cache deleted, please try the url again")
        # future work, add an exception here so the file gets downloaded without user involvement




def check_url_entry(url):
    if "https://www.youtube.com" in url:
        return True  # check of domain name
    else:
        update_download_status("Not an youtube URL"), print("Not an youtube URL")


def get_file_type_value(file_type_value):
    value = file_type_value.get()
    file_type = file_extensions[value]
    return file_type


def yt_downloader(url, file_type):
    video_url = str(url)
    video_info = youtube_dl.YoutubeDL().extract_info(url=video_url, download=False)

    filename = f"{video_info['title']}{file_type}"
    update_msg = "started downloading...", filename
    update_download_status(update_msg)
    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filename,
        'logger': MyLogger()
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])
    finished.append(filename)
    print("filename finished: ", finished)
    return ("FILENAME:   ", filename), finished


def update_progress_que(progress_que_change):
    global progress_que
    progress_que += progress_que_change
    return progress_que


def update_finished_number(finished_update):
    global finished_display_number
    finished_display_number += finished_update
    return finished_display_number


def update_download_status(msg):
    global download_status
    download_status.clear()
    download_status.append(msg)
    pass


def url_cleanup(url):
    url = url.replace(' ', '')  # removes potential whitespace and paragraphs
    url = url.replace('\n', '')
    return url


def download_handler(entry_url, file_type_value):
    entry_url = url_cleanup(entry_url)
    if not check_url_entry(entry_url):  # url check
        return "URL domain check ERROR, check supported domain"
    update_progress_que(1)  # add one to display number of downloads in gui
    file_type = get_file_type_value(file_type_value)
    update_msg = "started downloading... ", entry_url, " as ", file_type
    update_download_status(update_msg)
    try:
        download = yt_downloader(entry_url, file_type)
    except:
        # checks if download variable is assigned, if it not assigned an Error accrued in yt_downloader()
        if 'download' not in locals():
            update_msg = f"{'Something went wrong with the yt_downloader, please check URL entry: '}\n{entry_url}"
    else:
        update_finished_number(1)
        update_msg = "Complete"
    finally:
        update_progress_que(-1)
        update_download_status(update_msg)



