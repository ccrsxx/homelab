import subprocess
from typing import Literal

SoundFile = Literal['internet-up.wav', 'internet-down.wav']


def play_sound(sound_file: SoundFile) -> None:
    subprocess.run(
        [
            'ssh',
            '-i',
            '/home/ccrsxx/.ssh/homelab-automation.key',
            'ccrsxx@ubuntu',
            'pw-play',
            '--volume 10',
            f'/home/ccrsxx/sounds/{sound_file}',
        ]
    )
