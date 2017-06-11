#!/usr/bin/env python
from packageA.moduleA import funcA
from packageB.moduleB import funcB
from packageC.moduleC import funcC


def main():
    print(funcA(funcB(funcC("Do something more"))))


if __name__ == "__main__":
    main()
