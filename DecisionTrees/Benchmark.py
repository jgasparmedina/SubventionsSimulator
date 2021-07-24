from DecisionTrees import ID3, CART, C45, DataGenerator, SubventionsData, AttributesData
import argparse, sys, time


def argParser(args):
    """
    Function to parse a list of arguments and validate if they fulfill the required specifications
    :param args: list of arguments
    :return: a namespace with the processed and validated arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--training', action = 'store', type = int, help = 'Training set size: number of elements to training Decision Trees', required = True)
    parser.add_argument('-c', '--classification', action = 'store', type = int, help = 'Classification set size: number of elements to classify')
    parser.add_argument('-a', '--attempts', action = 'store', type = int, help = 'Attempts: number of simulations to execute. Each simulation represents a new training data set')
    parser.add_argument('-m', '--methods', nargs = '+', action = 'store', help = 'Methods: methods to create and test Decision Trees.Methods available are: ID3, C45 and CART.If no defined, '
                                                                                 'all methods will be processed', required = True)
    parser.add_argument('-x', '--cross', action = 'store', type = int, help = 'Cross-validation: a cross-validation will be computed for each methods splitting the training set in n slices')
    parser.add_argument('-s', '--step', action = 'store', type = int,
                        help = 'Step size: if you want to generate each Decision Tree from 0 to training size set increasing the number of training elements '
                               'sequentially by steps size elements')
    parser.add_argument('-o', '--output', action = 'store', help = 'Output: file output to dump results of the benchmark')
    return parser.parse_args(args)


def getSubSet(dataset, start, end, extract = False, toDict = False):
    """
    Returns data subset from start to end positions or the original dataset without that subset. Results can be returned as a list of dicts.
    :param dataset: Global dataset from which extracts the subset
    :param start: start index
    :param end: end index
    :param extract: if True returs the origial dataset without the subset specified.
    :param toDict: if True returns a list of dicts.
    :return: subset between start and end positions or original dataset without subset specified in dataframe format or list of dicts
    """
    if end > len (dataset.index):
        end = len (dataset.index)
    if start > len (dataset.index):
        start = len (dataset.index)

    if not extract:
        subset = dataset.iloc[start:end].reset_index(drop = True)
    else:
        subset = dataset.drop([i for i in range (start, end)]).reset_index(drop = True)
    if not toDict:
        return subset
    else:
        elements = []
        for i in range (len (subset.index)):
            element = {}
            for column in subset.columns.values:
                element[column] = subset[column][i]
            elements.append(element)
        return elements


if __name__ == '__main__':
    """
    Command line script to execute decision trees scenarios and retrieving some metrics 
    """
    args = argParser(sys.argv[1:])

    # Checking parameters
    if args.step and args.step > args.training:
        args.step = args.training
    step = args.step if args.step else args.training

    attempts = args.attempts if args.attempts else 1

    if args.cross:
        attempts = 1
    else:
        if not args.classification:
            print ("You must to indicate -c or -x parameter")
            sys.exit(1)

    # Generating iterations
    iterations = [step * i for i in range(1, int(args.training / step) + 1)]
    if iterations:
        if iterations[-1] < args.training:
            iterations.append(args.training)
    else:
        iterations = [args.training]

    fileout = None
    if args.output:
        try:
            fileout = open(args.output, "w")
            fileout.write("METHOD;ATTEMPT;TRAINING ELEMENTS;TREE CREATION TIME;TREE DEPTH;TREE CLASSIFICATION TIME;HITS;TOTAL ATTEMPTS;ACCURACY\n")
        except Exception as e:
            print("Error opening file %s: %s" % (args.output, e))
            fileout = None

    for attempt in range (attempts):
        # Generating classification data
        generator = DataGenerator.DataGenerator(AttributesData.ATRIBUTOS, SubventionsData.AYUDAS)
        start = time.time()

        if args.classification:
            print("Creating %s elements for classification..." % args.classification, end = "")
            classificationData = generator.generateData(args.classification, classified = True)
            end = time.time()
            print("OK! (%f seconds)" % (end - start))
        # Generating training data
        start = time.time()
        print("Creating %s elements for training..." % args.training, end = "")
        trainingData = generator.generateDataSet(args.training, classified = True)
        end = time.time()
        print("OK! (%f seconds)" % (end - start))

        for iteration in iterations:
            if not args.cross:
                print("Starting training for %s elements..." % iteration)
                dataset = getSubSet(trainingData, 0, iteration)
                treeTime = 0.0
                classTime = 0.0
                for method in args.methods:
                    if method == 'ID3':
                        print("Creating ID3 decision tree for %s elements..." % iteration, end = '')
                        start = time.time()
                        tree = ID3.ID3(dataset)
                        end = time.time()
                        treeTime = end - start
                        print("OK! (%s seconds) --> %s levels" % (treeTime, tree.getTreeDepth()))
                    elif method == 'C45':
                        print("Creating C45 decision tree for %s elements..." % iteration, end = '')
                        start = time.time()
                        tree = C45.C45(dataset)
                        end = time.time()
                        treeTime = end - start
                        print("OK! (%s seconds) --> %s levels" % (treeTime, tree.getTreeDepth()))
                    elif method == 'CART':
                        print("Creating CART decision tree for %s elements..." % iteration, end = '')
                        start = time.time()
                        tree = CART.CART(dataset)
                        end = time.time()
                        treeTime = end - start
                        print("OK! (%s seconds) --> %s levels" % (treeTime, tree.getTreeDepth()))
                    else:
                        print("Error: method %s is not supported! Skipping iteration." % method)
                        continue
                    print("Applying decision tree to classification set data...", end = '')
                    start = time.time()
                    hits = 0
                    for element in classificationData:
                        classification = tree.classify(element)
                        if element['CLASS'] == classification:
                            hits += 1
                    end = time.time()
                    classTime = end - start
                    accuracy = (hits / args.classification) * 100
                    print("OK! (%s seconds) --> Accuracy %f" % (classTime, accuracy))
                    if fileout:
                        fileout.write("%s;%d;%d;%f;%d;%f;%d;%d;%f\n" % (method, attempt + 1, iteration, treeTime, tree.getTreeDepth(), classTime, hits, args.classification, accuracy))
            else:
                sliceSize = int (args.training / args.cross)
                slices = [sliceSize * i for i in range(0, args.cross + 1)]
                if len(slices) > 2:
                    if slices[-1] < args.training:
                        slices.append(args.training)
                else:
                    print ("Not enough slices to compute cross validation... Skipping!")
                    continue
                for slice in range (1, len (slices)):
                    print("Starting crossing validation for scenario %d: classificationSubset is (%d, %d) ..." % (slice, slices[slice - 1], slices[slice]))
                    classificationData = getSubSet(trainingData, slices[slice - 1], slices[slice], toDict = True)
                    dataset = getSubSet(trainingData, slices[slice - 1], slices[slice], extract = True)
                    treeTime = 0.0
                    classTime = 0.0
                    size = len (dataset.index)
                    for method in args.methods:
                        if method == 'ID3':
                            print("Creating ID3 decision tree for %s elements..." % size, end = '')
                            start = time.time()
                            tree = ID3.ID3(dataset)
                            end = time.time()
                            treeTime = end - start
                            print("OK! (%s seconds) --> %s levels" % (treeTime, tree.getTreeDepth()))
                        elif method == 'C45':
                            print("Creating C45 decision tree for %s elements..." % size, end = '')
                            start = time.time()
                            tree = C45.C45(dataset)
                            end = time.time()
                            treeTime = end - start
                            print("OK! (%s seconds) --> %s levels" % (treeTime, tree.getTreeDepth()))
                        elif method == 'CART':
                            print("Creating CART decision tree for %s elements..." % size, end = '')
                            start = time.time()
                            tree = CART.CART(dataset)
                            end = time.time()
                            treeTime = end - start
                            print("OK! (%s seconds) --> %s levels" % (treeTime, tree.getTreeDepth()))
                        else:
                            print("Error: method %s is not supported! Skipping iteration." % method)
                            continue
                        print("Applying decision tree to classification set data...", end = '')
                        start = time.time()
                        hits = 0
                        for element in classificationData:
                            classification = tree.classify(element)
                            if element['CLASS'] == classification:
                                hits += 1
                        end = time.time()
                        classTime = end - start
                        accuracy = (hits / len(classificationData)) * 100
                        print("OK! (%s seconds) --> Accuracy %f" % (classTime, accuracy))
                        if fileout:
                            fileout.write("%s;%d;%d;%f;%d;%f;%d;%d;%f\n" % (method, slice, size, treeTime, tree.getTreeDepth(), classTime, hits, sliceSize, accuracy))
    if fileout:
        try:
            fileout.close()
        except Exception as e:
            print("Error closing file %s: %s" % (args.output, e))
