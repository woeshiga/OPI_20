#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import argparse
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


def update_json(file_name: str, words: list) -> list:
    for item in words:
        for letter in item["word"]:
            if letter in LETTERS:
                item["result"] = True
            else:
                item["result"] = False
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(words, f)
    return words


def display(words):
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


def main(command_line=None):
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    parser = argparse.ArgumentParser("words")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new word"
    )
    add.add_argument(
        "-w",
        "--word",
        action="store",
        required=True,
        help="The word instance"
    )

    add.add_argument(
        "-r",
        "--result",
        action="store",
        required=True,
        help="Handler result"
    )

    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all words"
    )

    _ = subparsers.add_parser(
        "update",
        parents=[file_parser],
        help="Update values"
    )

    args = parser.parse_args(command_line)

    if os.path.exists(args.filename):
        words = load_words(args.filename)
    else:
        with open(args.filename, "w", encoding="utf-8") as f:
            json.dump(list(), f)
            words = list()

    if args.command == "add":
        word = {
            "word": args.word,
            "result": args.result
        }
        add_words(
            args.filename,
            word
        )
    elif args.command == "display":
        display(words)
    elif args.command == "update":
        update_json(args.filename, words)


if __name__ == '__main__':
    main()
