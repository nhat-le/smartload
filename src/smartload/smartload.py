import scipy.io
import numpy as np
import os
import mat73
import pickle

def loadmat(filename):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    try:
        data = scipy.io.loadmat(filename, struct_as_record=False, squeeze_me=True)
        return _check_keys(data)
    except:
        data = mat73.loadmat(filename)
        return data

def _check_keys(dict):
    '''
    checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries
    '''
    for key in dict:
        if isinstance(dict[key], scipy.io.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
        elif isinstance(dict[key], np.ndarray) and len(dict[key]) > 0 and isinstance(dict[key][0], scipy.io.matlab.mio5_params.mat_struct):
            dict[key] = [_todict(subelem) for subelem in elem]
    return dict

def _todict(matobj):
    '''
    A recursive function which constructs from matobjects nested dictionaries
    '''
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, scipy.io.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        elif isinstance(elem, np.ndarray) and len(elem) > 0 and isinstance(elem[0], scipy.io.matlab.mio5_params.mat_struct):
            dict[strg] = [_todict(subelem) for subelem in elem]
        else:
            dict[strg] = elem
    return dict


def load_pickle(path):
    '''
    Smart loading of pickle object
    :param path: str: path to the picle file
    :return: contents of the pickle file
    '''
    data = pickle.load(open(path, 'rb'))
    return data

def save_pickle(data, path):
    '''
    Save data to a pickle file
    :param data: the data to be saved
    :param path: the path to save the data to
    :return: 1 if saved successfully
    '''
    # Check that path does not exist
    if os.path.exists(path):
        raise IOError('Path exists')
    pickle.dump(data, open(path, 'wb'))
    return 1




if __name__ == '__main__':
    filepath = '/Users/minhnhatle/Dropbox (MIT)/Sur/2p1/Feb2021/e54blockworldrolling_022321/regionData_e54_022321pix.mat'
    loadmat(filepath)

