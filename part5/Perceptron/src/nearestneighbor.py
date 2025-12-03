import math
import random

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
