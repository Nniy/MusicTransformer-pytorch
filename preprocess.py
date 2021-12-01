import pickle
import os
import sys
from progress.bar import Bar
import utils
from .processor import encode_midi


def preprocess_midi(path, aug):
    return encode_midi(path, aug)


def preprocess_midi_files_under(midi_root, save_dir, aug):
    midi_paths = list(utils.find_files_by_extensions(midi_root, ['.mid', '.midi']))
    os.makedirs(save_dir, exist_ok=True)
    out_fmt = '{}-{}.data'

    for path in Bar('Processing').iter(midi_paths):
        print(' ', end='[{}]'.format(path), flush=True)

        try:
            data = preprocess_midi(path, aug)
        except KeyboardInterrupt:
            print(' Abort')
            return
        except EOFError:
            print('EOF Error')
            return

        with open('{}/{}.pickle'.format(save_dir, path.split('/')[-1]), 'wb') as f:
            pickle.dump(data, f)


if __name__ == '__main__':
    if sys.argv[3] == "aug":
        aug = True
    else:
        aug = False
    preprocess_midi_files_under(
        midi_root=sys.argv[1],
        save_dir=sys.argv[2],
        aug=aug
    )
