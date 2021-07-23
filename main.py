#!/usr/bin/env python
# encoding: utf-8

from dataclasses import dataclass
from os.path import dirname, join, realpath
from typing import Dict, Iterator, Tuple


CURRENT_DIR = dirname(realpath(__file__))
DATA_DIR = join(CURRENT_DIR, 'dane')


@dataclass
class NameData:
    name: str
    children_by_year: Dict[int, int]

    @property
    def total_children(self) -> int:
        return sum(self.children_by_year.values())


def read_2018() -> Iterator[Tuple[str, int]]:
    path = join(DATA_DIR, '2018.txt')
    with open(path) as f:
        for line in f:
            name, count = line.strip().split(' - ')
            yield (name.title(), int(count))


def _main():
    data_by_name = {}

    for (year, year_data) in [
        (2018, read_2018()),
    ]:
        for (name, children) in year_data:
            if name not in data_by_name:
                data_by_name[name] = NameData(name, {})

            data_by_name[name].children_by_year[year] = children

    total_children = sum(nd.total_children for nd in data_by_name.values())

    print('pozycja,imię,liczba,udział')

    for (i, data) in enumerate(sorted(data_by_name.values(), key=lambda nd: -nd.total_children), start=1):
        print(f'{i},{data.name},{data.total_children},{data.total_children / total_children}')


if __name__ == '__main__':
    _main()
