import pickle
import os
import sys
from progress.bar import Bar
import utils
from processor import encode_midi


def preprocess_midi(path, aug):
    return encode_midi(path, aug)


def preprocess_midi_files_under(midi_root, save_dir, aug):
    midi_paths = list(utils.find_files_by_extensions(midi_root, ['.mid', '.midi']))
    os.makedirs(save_dir, exist_ok=True)
    out_fmt = '{}-{}.data'

    for path in Bar('Processing').iter(midi_paths):
        print(' ', end='[{}]'.format(path), flush=True)

        try:
            batch = preprocess_midi(path, aug)
        except KeyboardInterrupt:
            print(' Abort')
            return
        except EOFError:
            print('EOF Error')
            return

        for idx, data in batch.items():
            with open('{}/{}-{}.pickle'.format(save_dir, path.split('/')[-1], idx), 'wb') as f:
                pickle.dump(data, f)


if __name__ == '__main__':
    if sys.argv[3] == "aug":
        a = True
    else:
        a = False
    preprocess_midi_files_under(
        midi_root=sys.argv[1],
        save_dir=sys.argv[2],
        aug=a
    )
