from packageA.moduleA import funcA
from packageB.moduleB import funcB
from packageC.moduleC import funcC


def main(args=None):
    print(funcA(funcB(funcC("main"))))


if __name__ == "__main__":
    main()
