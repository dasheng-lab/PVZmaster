import pygame


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

    def play_sound(self, sound_name, loop_times=-1, self_volume=1.0):
        # 找到一个未使用的通道并播放音频
        for channel in self.channels:
            if not channel.get_busy():
                channel.play(self.sounds[sound_name], loops=loop_times)
                channel.set_volume(self_volume)
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
audio_player.load_sound("暂停", "music/暂停.ogg")
audio_player.load_sound("种植物", "music/种植物2.ogg")
audio_player.load_sound("选中植物", "music/选中卡槽植物.ogg")
audio_player.load_sound("阳光不够", "music/卡槽阳光不够提示音.ogg")
audio_player.load_sound("失败音效1", "music/僵尸吃掉了你的脑子！.ogg")
audio_player.load_sound("失败音效2", "music/失败音效.ogg")
audio_player.load_sound("失败音效3", "music/失败音频3.MP3")
audio_player.load_sound("铲子", "music/铲子.ogg")
audio_player.load_sound("收集阳光", "music/收集阳光.ogg")
audio_player.load_sound("旗帜僵尸", "music/旗帜僵尸出现.ogg")
audio_player.load_sound("最后一波", "music/一大波僵尸即将来临.ogg")
audio_player.load_sound("豌豆击中1", "music/豌豆击中1.ogg")
audio_player.load_sound("豌豆击中2", "music/豌豆击中2.ogg")
audio_player.load_sound("豌豆击中3", "music/打到路障 橄榄球.ogg")
audio_player.load_sound("报纸破碎", "music/报纸破碎.ogg")
audio_player.load_sound("二爷生气", "music/二爷生气.ogg")
audio_player.load_sound("二爷生气2", "music/二爷生气2.ogg")
audio_player.load_sound("啃坚果", "music/啃坚果.ogg")
audio_player.load_sound("啃植物", "music/啃植物.ogg")
audio_player.load_sound("头掉了", "music/头掉了.ogg")
audio_player.load_sound("失败音效1", "music/僵尸吃掉了你的脑子！.ogg")
audio_player.load_sound("失败音效2", "music/失败音效.ogg")
audio_player.load_sound("呻吟1", "music/呻吟.ogg")
audio_player.load_sound("呻吟2", "music/呻吟2.ogg")
audio_player.load_sound("呻吟3", "music/呻吟3.ogg")
audio_player.load_sound("豌豆击中4", "music/豌豆打铁器.ogg")
audio_player.load_sound("产生钻石", "music/产生钻石.ogg")
audio_player.load_sound("产生币", "music/金币银币掉落.ogg")
audio_player.load_sound("选中", "music/选中卡槽植物.ogg")
audio_player.load_sound("种植物", "music/种植物.ogg")
audio_player.load_sound("铲植物", "music/种植物2.ogg")
audio_player.load_sound("铲子", "music/铲子.ogg")
audio_player.load_sound("收集阳光", "music/收集阳光.ogg")
audio_player.load_sound("豌豆发射", "music/豌豆发出.ogg")
audio_player.load_sound("一大波", "music/合成音效.MP3")
audio_player.load_sound("第一波", "music/僵尸第一波进攻.ogg")
audio_player.load_sound("旗帜僵尸", "music/旗帜僵尸出现.ogg")
audio_player.load_sound("最后一波", "music/最后一波.ogg")
audio_player.load_sound("通关音乐", "music/通关音乐.ogg")
audio_player.load_sound("僵尸叫", "music/僵尸呻吟12.ogg")
audio_player.load_sound("窝瓜怀疑", "music/窝瓜怀疑.ogg")
