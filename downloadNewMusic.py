from playMusic import download_audio

def downloadNewMusic():
    name = input("Enter the name of the file you want the music to be in: ")
    url = input("Enter the URL of the music you want to download: ")
    download_audio(url,1, name)
    print("Music downloaded!\n-----------------------\n")

downloadNewMusic()