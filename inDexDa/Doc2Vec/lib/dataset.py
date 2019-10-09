import json
import random
import torch.utils.data as data


class Dataset(data.Dataset):
    def __init__(self, train=True, min_thresh=10, max_thresh=None,
                 train_test_split=0.8):
        '''
        Reads dataset from a json file. Normalizes and tokenizes the dataset as well as
         removes uncommon words (to better handle them in machine learning applications).

        :params  training_data(list of lists)     : samples for training
                 testing_data(list of lists)      : samples for testing
                 min_thresh(int)                  : minimum word count threshold
                 max_thresh(int)                  : maximum word count threshold
                 train_test_split(float)          : train test split
                 train(bool)                      : using training data
        '''
        self.train = train
        self.train_test_split = train_test_split
        self.all_samples = self.get_dataset()

        self.partition_dataset(self.all_samples)

    def get_dataset(self):
        dataset = []
        with open('/home/parker/code/datadex/inDexDa/Doc2Vec/log/dataset.json', 'r') as f:
            contents = f.read()
            try:
                raw = json.loads(contents)
                for paper in raw:
                    dataset.append([paper['Text'], paper['Target']])
            except ValueError:
                print('Not able to parse json file to dictionary.\n')

        return dataset

    def partition_dataset(self, dataset):
        # Split dataset into testing and training samples
        random.seed(100)
        random.shuffle(dataset)

        if self.train:
            self.data = dataset[:int(len(dataset) * self.train_test_split)]
        else:
            self.data = dataset[int(len(dataset) * self.train_test_split):]

    def __getitem__(self, index):
        return self.data[index][0], self.data[index][1]

    def __len__(self):
        return len(self.data)


if __name__ == '__main__':
    dataset = Dataset()