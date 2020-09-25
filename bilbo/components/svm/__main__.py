"""SVM module"""
from bilbo.libs.opts import Parser
import bilbo.components.svm.svm as s 
from bilbo.utils.bilbo_logger import get_logger

if __name__ == "__main__":
    args = Parser.parse_arguments()
    verbosity = args.verbose
    logger = get_logger(name=__name__, verbosity=args.verbose)
    cfg_svm = args.cfg

    data_svm = args.input

    svm = s.Svm(cfg_svm)

    if args.train:
        svm.train(data_svm)
    elif args.tag:
        res = svm.predict(data_svm)
        if args.verbose:
            print(res)
    elif args.evaluate:
        res = svm.evaluate(data_svm)
    else:
        print("Error: Mauvais mode: choisir l'option -T / -t [train / test]")


