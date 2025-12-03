import math
import os
import numpy as np
from PIL import Image
import random

NUMBER_OF_PIXELS = 28 * 28
IMAGE_SIZE = 28


def get_chars(filename):
    """
    Reads the classes of characters
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))

    try:
        with open(os.path.join(dir_path, '..', filename)) as file:
            chars = [line[0] for line in file]

        return chars

    except FileNotFoundError:
        print("File %s was not found." % filename)
        raise
    except Exception as e:
        print("Something terrible happened: %s", str(e))
        raise


def get_images(filename):
    """
    Reads the images (black pixel is 1, white pixel is 0 in the input)
    Trasnforms (0, 1) values to (-1.0, 1.0)
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    vectors = []

    try:
        with open(os.path.join(dir_path, '..', filename)) as file:
            for line in file:
                vectors.append([1.0 if float(v) == 1 else -1.0 for v in line.strip().split(',')])

        return vectors

    except FileNotFoundError:
        print("File %s was not found." % filename)
        raise
    except Exception as e:
        print("Something terrible happened: %s", str(e))
        raise


class NearestNeighbor:
    def __init__(self, images, chars):
        self.data = [{'vector': v, 'char': c} for v, c in zip(get_images(images), get_chars(chars))]

    def classify(self, x, train_examples):
        closest_dist = float('inf')
        closest_label = None

        for e in train_examples:
            dist = math.sqrt(sum((xi - yi) ** 2 for xi, yi in zip(x, e['vector'])))
            if dist < closest_dist:
                closest_dist = dist
                closest_label = e['char']

        return closest_label

    def test(self, target_char=None, opposite_char=None):
        train_examples = self.data[:5000]
        test_examples = self.data[5000:]

        if target_char and opposite_char:
            train_examples = [e for e in train_examples if e['char'] in (target_char, opposite_char)]
            test_examples = [e for e in test_examples if e['char'] in (target_char, opposite_char)]

        correct = 0
        for e in test_examples:
            predicted = self.classify(e['vector'], train_examples)
            if predicted == e['char']:
                correct += 1

        return float(correct) / len(test_examples)


class Perceptron:
    """ Perceptron
        :attr data: list of objects that represent images
    """

    def __init__(self, images, chars):
        idata = get_images(images)
        cdata = get_chars(chars)

        self.data = [{'vector': v, 'char': c} for (v, c) in zip(idata, cdata)]
        random.seed()

    def train(self, target_char, opposite_char, steps):
        w = [0.0] * len(self.data[0]['vector'])
        train_examples = self.data[:5000]
        train_examples = [e for e in train_examples if e['char'] in (target_char, opposite_char)]

        for step in range(steps):
            e = random.choice(train_examples)
            x = np.array(e['vector'])
            y = 1 if e['char'] == target_char else -1

            z = np.dot(w, x)

            if z >= 0 and y == -1:
                w -= x
            elif z < 0 and y == 1:
                w += x

        self.weights = w

    def test(self, target_char, opposite_char):
        """Tests the learned perceptron with the last 1000 x,y pairs.
        (Note that this only counts those ones that belong either to the plus or minus classes.)

        :param target_char: the target character we are trying to distinguish
        :param opposite_char: the opposite character
        :return: the ratio of correctly classified characters
        """
        success = 0
        examples = self.data[5000:]

        examples = [e for e in examples if e['char'] in (target_char, opposite_char)]

        for e in examples:
            z = np.dot(e['vector'], self.weights)
            if (z >= 0 and e['char'] == target_char) or (z < 0 and e['char'] == opposite_char):
                success += 1

        return float(success) / len(examples)

    def save_weights(self, filename):
        """Draws a 28x28 grayscale picture of the weights

        :param filename: Name of the file where weights will be saved
        """
        pixels = [.01 + .98 / (1.0 + float(math.exp(-w))) for w in self.weights]

        Image.fromarray(np.array(pixels).reshape(IMAGE_SIZE, IMAGE_SIZE), mode = "L").save(filename)
