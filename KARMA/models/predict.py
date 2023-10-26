from sklearn.externals import joblib

import location
import map

__author__ = 'Mansi'


class Predictor(object):
    def __init__(self, model, labels):
        self.model = model
        self.labels = labels

    def predict(self, lat, long):
        x, y = location.to_x(lat), location.to_y(long)
        prediction = model.predict([(x, y)])[0]
        return self.labels[prediction]


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'model',
        help='Model file generated by train.py'
    )
    parser.add_argument(
        'label',
        help='Label file'
    )
    parser.add_argument(
        'coordinate', nargs='+',
        help='Coordinate(s) to predict, in the format "lat,long"'
    )
    args = parser.parse_args()

    model = joblib.load(args.model)

    label_map = map.read_file(args.label)
    label_map = {v: k for k, v in label_map.items()}
    predictor = Predictor(model, label_map)

    for coord in args.coordinate:
        lat, long = [float(i) for i in coord.split(',')]
        print(predictor.predict(lat, long))