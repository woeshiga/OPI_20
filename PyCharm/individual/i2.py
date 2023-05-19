#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import click
import os.path
import sys

LETTERS = 'eyuioa'


def load_words(file_name: str) -> dict:
    with open(file_name, 'r', encoding='utf-8') as f:
        return json.load(f)


def add_words(file_name: str, word: dict) -> None:
    with open(file_name, 'r', encoding='utf-8') as f:
        content_json = json.load(f)
    content_json.append(word)
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(content_json, f)


def update_json(file_name: str) -> list:
    words = load_words(file_name)
    for item in words:
        for letter in item["word"]:
            if letter in LETTERS:
                item["result"] = True
            else:
                item["result"] = False
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(words, f)
    return words


def display_json(words):
    if words:
        line = '+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20
        )
        print(line)
        print(
            "| {:^4} | {:^30} | {:^20} |".format(
                "№",
                "Слово",
                "Результат"
            )
        )
        print(line)

        for idx, word in enumerate(words, 1):
            print(
                "| {:^4} | {:^30} | {:^20} |".format(
                    idx,
                    word.get('word', ''),
                    word.get('result', ''),
                )
            )
        print(line)
    else:
        print("Список пуст.")


@click.command()
@click.argument("filename")
@click.option("-w", "--word", required=True, type=str)
@click.option("-r", "--result", required=True, type=int)
def add(filename, word, result):
    word = {
            "word": word,
            "result": result
        }
    add_words(
        filename,
        word
    )

@click.command()
@click.argument("filename")
def display(filename):
    if os.path.exists(filename):
        words = load_words(filename)
    else:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(list(), f)
            words = list()

    display_json(words)

@click.command()
@click.argument("filename")
def update(filename):
    update_json(filename)

@click.group()
def main():
    pass

main.add_command(add)
main.add_command(update)
main.add_command(display)


if __name__ == '__main__':
    main()
