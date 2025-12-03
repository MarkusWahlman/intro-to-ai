from perceptron import Perceptron
from perceptron import NearestNeighbor

IMGS_FILE = 'mnist-x.data'
CHARS_FILE = 'mnist-y.data'


def main():
    """
    Implement the perceptron algorithm in the Perceptron class. After that you can try out the
    values of different number pairs by changing the values of the 'target_char' and
    'opposite_char' variables.
    """
    perc = Perceptron(IMGS_FILE, CHARS_FILE)
    perc.train('7', '5', 100)
    print("Perc: ", perc.test('7', '5'))
    perc.save_weights('weights.bmp')

    nn = NearestNeighbor(IMGS_FILE, CHARS_FILE)
    accuracy = nn.test(target_char='7', opposite_char='5')
    print("Acc: ", accuracy)

if __name__ == '__main__':
    main()
