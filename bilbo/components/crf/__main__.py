"""crf module"""
from bilbo.libs.opts import Parser
import bilbo.components.crf.crf as c
from bilbo.utils.bilbo_logger import get_logger



if __name__ == "__main__":
    args = Parser.parse_arguments()
    verbosity = args.verbose
    logger = get_logger(name=__name__, verbosity=args.verbose)

    cfg_crf = args.cfgcrf
    input_file = args.input


    data_crf = []
    f = open(input_file, "r")
    for line in f:
        data_crf.append(line)

    crf = c.Crf(cfg_crf)

    if args.train:
        crf.train(data_crf)
    elif args.tag:
        res_label = crf.predict(data_crf)
        if args.verbose:
            for res in res_label:
                for r in res:
                    print(r[0], r[1])
                print('')
    elif args.evaluate:
        crf.evaluate(data_crf)
    else:
        print("Error: Mauvais mode: choisir l'option -T / -t [train / test]")
