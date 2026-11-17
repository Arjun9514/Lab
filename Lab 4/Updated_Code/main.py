from game import DotsAndBoxes


def main():
    print('=== Dots and Boxes ===')
    print('1. Human vs Human')
    print('2. Human vs Computer')
    while True:
        try:
            choice = input('Choose mode (1 or 2): ').strip()
        except EOFError:
            print('\nInput ended. Exiting.')
            return
        if choice in ('1', '2'):
            DotsAndBoxes(vs_computer=(choice == '2')).run()
            return
        print('Please enter 1 or 2.')


if __name__ == '__main__':
    main()
