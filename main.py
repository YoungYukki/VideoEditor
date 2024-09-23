import os
import json
import shutil
import subprocess
from typing import List


class Editor:
    work_path = 'source'
    cut_config_path = 'cut.json'

    def __init__(self) -> None:
        self.check()
        self.get_config()
        self.cut()
        self.concat()

    def check(self):
        if not os.path.exists(self.work_path):
            print('不存在的工作目录')
            exit(1)
        if not os.path.exists(self.cut_config_path):
            print(f'不存在{self.cut_config_path}')
            exit(2)

    def get_config(self):
        with open(self.cut_config_path, 'r') as f:
            self.cut_config: List = json.load(f)

    def cut(self):
        temp_path = os.path.join(self.work_path, 'temp')
        self.temp_path = temp_path
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
        os.makedirs(temp_path)
        count = 0
        for frag in self.cut_config:
            video = os.path.join(self.work_path, frag['video'])
            start = frag['start']
            end = frag['end']
            cmd = [
                'ffmpeg', '-i', video,
                '-ss', start, '-to', end,
                '-vcodec', 'copy', '-acodec', 'copy',
                os.path.join(
                    temp_path,
                    f'output_temp_{str(count).zfill(2)}.mp4'
                )
            ]
            subprocess.run(args=cmd, shell=True)
            count += 1

    def concat(self):
        videos = [
            f"file '{video}'" for video in os.listdir(self.temp_path)
        ]
        video_list = os.path.join(self.temp_path, 'video_list.txt')
        with open(video_list, 'w') as f:
            f.write('\n'.join(videos))
        cmd = [
            'ffmpeg', '-f', 'concat', '-i',
            video_list, '-c', 'copy', 'output.mp4'
        ]
        subprocess.run(args=cmd, shell=True)
        shutil.rmtree(self.temp_path)


if __name__ == '__main__':
    Editor()
