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


def read_csv(year: int) -> Iterator[Tuple[str, int]]:
    path = join(DATA_DIR, f'{year}.csv')
    with open(path) as f:
        for (i, line) in enumerate(f):
            if i == 0:
                continue

            name, gender, count = line.strip().split(',')
            yield (name.title(), int(count))


def read_2021_h1() -> Iterator[Tuple[str, int]]:
    path = join(DATA_DIR, f'2021-h1.csv')
    with open(path) as f:
        for (i, line) in enumerate(f):
            if i == 0:
                continue

            name, count, gender = line.strip().split(',')
            if gender.strip().lower() == 'k':
                yield (name.title(), int(count))


def _main():
    data_by_name = {}

    for (year, year_data) in [
        (2018, read_2018()),
        (2019, read_csv(2019)),
        (2020, read_csv(2020)),
        (2021, read_2021_h1()),
    ]:
        for (name, children) in year_data:
            if name not in data_by_name:
                data_by_name[name] = NameData(name, {})

            data_by_name[name].children_by_year[year] = children

    total_children = sum(nd.total_children for nd in data_by_name.values())

    print('pozycja,imię,liczba,udział,jedna na')

    for (i, data) in enumerate(sorted(data_by_name.values(), key=lambda nd: -nd.total_children), start=1):
        popularity = data.total_children / total_children
        one_per = int(round(1.0 / popularity))
        print(f'{i},{data.name},{data.total_children},{popularity},{one_per}')


if __name__ == '__main__':
    _main()
