import pygame
from Event import *
from Creature import *

class AudioPlayer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.sounds = {}
        self.channels = []
        # 初始化 8 个音频通道，可以根据需要调整通道数量
        for i in range(8):
            self.channels.append(pygame.mixer.Channel(i))

    def load_sound(self, sound_name, file_path):
        pygame.mixer.init()
        # 加载音频文件并存储在 sounds 字典中
        self.sounds[sound_name] = pygame.mixer.Sound(file_path)

    def play_sound(self, sound_name, loop_times=-1):
        # 找到一个未使用的通道并播放音频
        for channel in self.channels:
            if not channel.get_busy():
                channel.play(self.sounds[sound_name], loops=loop_times)
                break

    def pause_sound(self):
        # 暂停所有正在播放的音频
        for channel in self.channels:
            if channel.get_busy():
                channel.pause()

    def unpause_sound(self):
        # 取消暂停所有暂停的音频
        for channel in self.channels:
            if channel.get_busy():
                channel.unpause()

    def stop_sound(self):
        # 停止所有正在播放的音频
        for channel in self.channels:
            if channel.get_busy():
                channel.stop()

    def switch_sound(self, sound_name):
        # 停止正在播放的音频并播放新的音频
        self.stop_sound()
        self.play_sound(sound_name)

audio_player = AudioPlayer()
audio_player.load_sound("begin", "music/begin.mp3")
audio_player.load_sound("begin2", "music/begin2.mp3")
audio_player.load_sound("begin3", "music/begin3.mp3")