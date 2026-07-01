from setuptools import setup, find_packages

setup(
    name='beat_addicts',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'torch>=2.1.0',
        'torchaudio>=2.1.0',
        'transformers>=4.31.0',
        'tokenizers>=0.13.3',
        'torchmetrics>=1.2.1',
        'sentence-transformers>=2.2.2',
        'peft>=0.10.0',
        'librosa>=0.10.0',
        'soundfile>=0.12.1',
        'pydub>=0.25.1',
        'diffusers>=0.16.0',
        'click>=8.1.0'
    ],
    entry_points={
        'console_scripts': [
            'beat-addicts=beat_addicts.cli:generate_song'
        ]
    }
)