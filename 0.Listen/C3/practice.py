#!/usr/bin/env python
import os
import sys
import termios
import tty
import requests
from pydub import AudioSegment
from pydub.playback import play
from multiprocessing import Process
import json
import contextlib
import argparse

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def _play_audio(word):
    audio_file = f"./audio/{word}.mp3"
    if not os.path.exists(audio_file):
        url = f"https://dict.youdao.com/dictvoice?audio={word}&type=1"
        response = requests.get(url)
        with open(audio_file, 'wb') as file:
            file.write(response.content)
    audio = AudioSegment.from_mp3(audio_file)
    devnull = os.open(os.devnull, os.O_WRONLY)
    original_stdout = os.dup(1)
    original_stderr = os.dup(2)
    os.dup2(devnull, 1)
    os.dup2(devnull, 2)
    try:
        play(audio)
    finally:
        os.dup2(original_stdout, 1)
        os.dup2(original_stderr, 2)
        os.close(devnull)
        os.close(original_stdout)
        os.close(original_stderr)

def play_audio(word):
    p = Process(target=_play_audio, args=(word,))
    p.start()

def word_practice(word, explanation='Current word', repeat=3):
    length = len(word)
    display = ['_'] * length
    index = 0
    first_try = True
    correct_count = 1
    retry_count = 0
    play_audio(word)
    
    try:
        while True:
            print(f"\r{explanation}: ", end='', flush=True)
            if not first_try:
                print(f"\033[91m[{correct_count}] {' '.join(display)}\033[0m", end='', flush=True)
            else:
                print(' '.join(display), end='', flush=True)
            
            char = getch()
            if len(char) != 1:
                continue
            
            if char == word[index].lower():
                display[index] = char
                index += 1
                if index == length:
                    if first_try:
                        break  # 第一次尝试成功，直接返回
                    else:
                        correct_count += 1
                        if correct_count > repeat:
                            break  # 达到10次正确输入，返回
                        else:
                            index = 0
                            display = ['_'] * length
                            play_audio(word)
            else:
                if first_try:
                    first_try = False
                    retry_count = 1
                else:
                    retry_count += 1
                correct_count = 1
                display = ['_'] * length
                index = 0
                play_audio(word)
        print(f"\r{explanation}: ", ' '.join(display), end='', flush=True)
        print("\r")
    except KeyboardInterrupt:
        print("\nExiting program.")

def load_incorrect_words():
    try:
        with open('incorrect_words.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return [{"word": item["name"], "explanation": ', '.join(item["trans"])} for item in data]
    except FileNotFoundError:
        print("Error: incorrect_words.json file not found.")
        return []
    except json.JSONDecodeError:
        print("Error: incorrect_words.json file is not a valid JSON.")
        return []

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='practice')
    parser.add_argument('number', nargs='?', type=int, default=1, help='number')
    args = parser.parse_args()
    number = args.number
    dictArr = load_incorrect_words()
    if not dictArr:
        print("No words to practice. Please make sure incorrect_words.json exists and is not empty.")
    else:
        for item in dictArr:
            for i in range(number):
                # print(f"{item["word"]},{item['explanation']}")
                word_practice(item["word"], item["explanation"], 3)
