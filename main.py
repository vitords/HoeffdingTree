import csv
from hoeffdingtree import *

def open_dataset(filename, class_index, probe_instances=100):
    """ Open and initialize a dataset in CSV format.
    The CSV file needs to have a header row, from where the attribute names will be read, and a set
    of instances containing at least one example of each value of all nominal attributes.

    Args:
        filename (str): The name of the dataset file (including filepath).
        class_index (int): The index of the attribute to be set as class.
        probe_instances (int): The number of instances to be used to initialize the nominal 
            attributes. (default 100)

    Returns:
        Dataset: A dataset initialized with the attributes and instances of the given CSV file.
    """
    if not filename.endswith('.csv'):
        raise TypeError(
            'Unable to open \'{0}\'. Only datasets in CSV format are supported.'
            .format(filename))
    with open(filename) as f:
        fr = csv.reader(f)
        headers = next(fr)

        att_values = [[] for i in range(len(headers))]
        instances = []
        try:
            for i in range(probe_instances):
                inst = next(fr)
                instances.append(inst)
                for j in range(len(headers)):
                    try:
                        inst[j] = float(inst[j])
                        att_values[j] = None
                    except ValueError:
                        inst[j] = str(inst[j])
                    if isinstance(inst[j], str):
                        if att_values[j] is not None:
                            if inst[j] not in att_values[j]:
                                att_values[j].append(inst[j])
                        else:
                            raise ValueError(
                                'Attribute {0} has both Numeric and Nominal values.'
                                .format(headers[j]))
        # Tried to probe more instances than there are in the dataset file
        except StopIteration:
            pass

    attributes = []
    for i in range(len(headers)):
        if att_values[i] is None:
            attributes.append(Attribute(str(headers[i]), att_type='Numeric'))
        else:
            attributes.append(Attribute(str(headers[i]), att_values[i], 'Nominal'))

    dataset = Dataset(attributes, class_index)
    for inst in instances:
        for i in range(len(headers)):
            if attributes[i].type() == 'Nominal':
                inst[i] = int(attributes[i].index_of_value(str(inst[i])))
        dataset.add(Instance(att_values=inst))
    
    return dataset

def main():
    filename = 'dataset_file.csv'
    dataset = open_dataset(filename, 1, probe_instances=10000)
    vfdt = HoeffdingTree()
    
    # Set some of the algorithm parameters
    vfdt.set_grace_period(50)
    vfdt.set_hoeffding_tie_threshold(0.05)
    vfdt.set_split_confidence(0.0001)
    # Split criterion, for now, can only be set on hoeffdingtree.py file.
    # This is only relevant when Information Gain is chosen as the split criterion
    vfdt.set_minimum_fraction_of_weight_info_gain(0.01)

    vfdt.build_classifier(dataset)
    
    # Simulate a data stream
    with open(filename) as f:
        stream = csv.reader(f)
        # Ignore the CSV headers
        next(stream)
        for item in stream:
            inst_values = list(item)
            for i in range(len(inst_values)):
                if dataset.attribute(index=i).type() == 'Nominal':
                    inst_values[i] = int(dataset.attribute(index=i)
                        .index_of_value(str(inst_values[i])))
                else:
                    inst_values[i] = float(inst_values[i])
            new_instance = Instance(att_values=inst_values)
            new_instance.set_dataset(dataset)
            vfdt.update_classifier(new_instance)
    print(vfdt)

if __name__ == '__main__':
    main()

