import MangaDexPy, os, time
from MangaDexPy import downloader

if not os.path.exists("manga"):
    os.mkdir("manga")

while True:
    anime_link = input("Enter manga link: ").split("/")
    anime_id = anime_link[4]
    anime_name = anime_link[5].split("?")[0]
    print(anime_name, anime_id)

    print(f"\nLeave blank to keep this as {anime_name}")
    folder_name = input(f"Input manga name: ")
    if not folder_name:
        folder_name = anime_name

    if not os.path.exists(f"manga/{folder_name}"):
        os.mkdir(f"manga/{folder_name}")

    print("Logging in")
    cli = MangaDexPy.MangaDex()
    cli.login("rapidslayer101", "smokester1/")
    print("Logged in")


    def download_manga(manga_id: str):
        print("Colleting anime data")
        manga = cli.get_manga(manga_id)
        manga.get_chapters()
        chapters = manga.get_chapters()
        chapters = [x for x in chapters if x.language == "en"]
        chapter_data = {}
        non_chapter_count = 0
        page_count_total = 0
        for chapter in chapters:
            try:
                chapter_num = float(chapter.chapter)
            except TypeError:
                non_chapter_count -= 1
                chapter_num = non_chapter_count
            page_count_total += int(len(chapter.pages))
            chapter_data.update({float(chapter_num): chapter})

        chapter_data = dict(sorted(chapter_data.items(), key=lambda item: item[0]))
        chapter_num_list = list(chapter_data.keys())
        chapters = list(chapter_data.values())
        print(len(chapter_num_list), chapter_num_list)
        print(f"Attempting download of {len(chapters)} chapters of {anime_name}, {page_count_total} total pages")

        timer = time.time()
        page_count = 0
        skipped_chapters = []
        chapters_have = []
        for ch_num in range(len(chapters)):
            try:
                page_count += len(chapters[ch_num].pages)
                if not os.path.exists(f"manga/{folder_name}/chapter-{chapter_num_list[ch_num]}"):
                    os.mkdir(f"manga/{folder_name}/chapter-{chapter_num_list[ch_num]}")
                    downloader.threaded_dl_chapter(chapters[ch_num],
                                                   f"manga/{folder_name}/chapter-{chapter_num_list[ch_num]}")
                path, dirs, files = next(os.walk(f"manga/{folder_name}/chapter-{chapter_num_list[ch_num]}"))
                file_count = len(files)
                if len(chapters[ch_num].pages) != file_count:
                    if len(chapters[ch_num].pages) > 0:
                        print(f"[Pre-downloaded] Chapter page number error, re-downloading")
                    print(f"Downloading chapter {chapter_num_list[ch_num]} - {len(chapters[ch_num].pages)} "
                          f"pages ({page_count}/{page_count_total}) "
                          f"{round((page_count / page_count_total) * 100, 2)}% "
                          f"{round(time.time() - timer, 2)}s")
                    downloader.threaded_dl_chapter(chapters[ch_num],
                                                   f"manga/{folder_name}/chapter-{chapter_num_list[ch_num]}")
                    path, dirs, files = next(os.walk(f"manga/{folder_name}/chapter-{chapter_num_list[ch_num]}"))
                    file_count = len(files)
                    if len(chapters[ch_num].pages) != file_count:
                        print(f"Page number invalid for chapter {chapter_num_list[ch_num]}")
                        input()
                    else:
                        if len(chapters[ch_num].pages) == 0:
                            print(f"No pages in chapter {chapter_num_list[ch_num]} this chapter will be skipped")
                            os.rmdir(f"manga/{folder_name}/chapter-{chapter_num_list[ch_num]}")
                            skipped_chapters.append(chapter_num_list[ch_num])
                        else:
                            print(f"Chapter {chapter_num_list[ch_num]} - {len(chapters[ch_num].pages)} verified ")
                            chapters_have.append(chapter_num_list[ch_num])
                else:
                    if len(chapters[ch_num].pages) == 0:
                        print(f"No pages in chapter {chapter_num_list[ch_num]} this chapter will be skipped")
                        os.rmdir(f"manga/{folder_name}/chapter-{chapter_num_list[ch_num]}")
                        skipped_chapters.append(chapter_num_list[ch_num])
                    else:
                        print(f"[Pre-downloaded] Chapter {chapter_num_list[ch_num]}"
                              f" - {len(chapters[ch_num].pages)} verified ")
                        chapters_have.append(chapter_num_list[ch_num])
            except Exception as e:
                print(f"error downloading chapter {chapter_num_list[ch_num]}", e)
                input("ERROR, hit enter to ignore")
        print("\nDownloading/verification complete")
        print(f"Skipped {skipped_chapters}")
        chapter_prob_missing = []
        chapter_missing = 0
        while chapter_missing < float(chapters_have[-1]):
            chapter_missing += 1
            if not float(chapter_missing) in chapters_have:
                chapter_prob_missing.append(float(chapter_missing))
        print(f"Chapters probably missing {skipped_chapters}")
        print(f"Chapters on drive {chapters_have}")
    download_manga(anime_id)
    print("\nManga downloaded, looping script")
