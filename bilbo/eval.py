#-*- coding: utf-8 -*-
#!/usr/bin/python3

from collections import OrderedDict
import statistics
import csv 


class Evaluation:
    """Evaluation class"""
    def __init__(self, gold, predicted, option="fine"):
        self.gold = gold
        self.predicted = predicted
        self.option = option
        self.matrix = None 
        self.all_label = None 
        self.imap = None 

    def get_unique_label(self):
        """
        return a list of unique label from the gold and predicted lists 
        """
        if self.option == "large":
            labels = set(self.gold + self.predicted)
            labels.remove("c")
            labels.remove("bibl")
            labels.remove("hi")
            self.all_label = sorted(labels)
        else:
            self.all_label = sorted(set(self.gold + self.predicted))
        return sorted(set(self.gold + self.predicted))

    def get_confusion_matrix(self):
        """
        Generate the confusion matrix
        populate matrix with the confusion matrix
        populate imap 
        """
        unique = self.get_unique_label()
        matrix = [[0 for _ in unique] for _ in unique]
        imap   = {key: i for i, key in enumerate(unique)}
        # Generate Confusion Matrix
        for p, a in zip(self.predicted, self.gold):
            matrix[imap[p]][imap[a]] += 1
        
        self.matrix = matrix
        self.imap = imap 
        return matrix

    def get_true_positive(self, label):
        """
        return the true positive from the matrix 
        """
        loc = self.matrix[self.imap[label]][self.imap[label]]
        return loc

    def get_row_sum(self, label):
        """
        return the sum of a given row 
        """
        row = sum(self.matrix[self.imap[label]][:])
        return row

    def get_col_sum(self, label):
        """
        return the sum of a given column
        """
        col = sum([row[self.imap[label]] for row in self.matrix])
        return col

    def get_precision_for_labels(self):
        """
        return a dict with the precition of each label 
        :return: dict (label, precision)
        """
        precisions = dict()
        for lab in self.all_label:
            precision = self.get_precision_for_label(lab)
            precisions[lab] = precision
        return OrderedDict(sorted(precisions.items(), key=lambda t: t[0]))

    def get_precision_for_label(self, label):
        """
        param label : a given label
        return the precision for a given label 
        """
        tp = self.get_true_positive(label)
        row = self.get_row_sum(label)
        fp  = row - tp
        precision = tp / (tp + fp) if tp > 0 else 0.0
        return precision

    def get_recall_for_labels(self):
        """
        return a dict with the recall of each label 
        :return: dict (label, recall)
        """
        recalls = dict()
        for lab in self.all_label:
            recall = self.get_recall_for_label(lab)
            recalls[lab] = recall
        return OrderedDict(sorted(recalls.items(), key=lambda t: t[0]))

    def get_recall_for_label(self, label):
        """
        param label : a given label
        return the recall for a given label 
        """
        col = self.get_col_sum(label)
        tp = self.get_true_positive(label)
        fn  = col - tp 
        recall = tp / (tp + fn) if tp > 0 else 0.0
        return recall 

    def get_count_for_label(self, label): 
        """
        param label : a given label
        return the number of occurences for a given label 
        """
        tp = self.get_true_positive(label)
        col = self.get_col_sum(label)
        fn  = col - tp 
        pos  = tp + fn
        return pos

    def get_count_for_labels(self):
        """
        return a dict with the number of occurences for each label 
        :return: dict (label, count)
        """
        counts = dict()
        for lab in self.all_label:
            count = self.get_count_for_label(lab)
            counts[lab] = count
        return OrderedDict(sorted(counts.items(), key=lambda t: t[0]))

    def get_f_measure_for_labels(self, beta :float=1):
        """
        Returns F1 score for all labels. See http://en.wikipedia.org/wiki/F1_score

        :param beta: the beta parameter higher than 1 prefers recall,\n 
                     lower than 1 prefers precision

        :return: dict (label, F1)
        """
        f_measure = dict()

        precision_for_labels = self.get_precision_for_labels()
        recall_for_labels = self.get_recall_for_labels()

        for label in self.all_label:
            p = precision_for_labels.get(label)
            r = recall_for_labels.get(label)
            fm = 0.0
            if (p + r) > 0:
                fm = (1.0 + (beta * beta)) * ((p * r) / ((beta * beta * p) + r))
            f_measure[label] = fm
        return OrderedDict(sorted(f_measure.items(), key=lambda t: t[0]))

    def get_macro_f_measure(self):
        """
        :return: the mean f-measure for the whole document 
        """
        macro_p = statistics.mean(self.get_precision_for_labels().values())
        macro_r = statistics.mean(self.get_recall_for_labels().values())

        if macro_p > 0 and macro_r > 0: 
            return (2 * macro_p * macro_r) / (macro_p + macro_r) 
        else:
            return 0.0

    def get_macro_precision(self):
        return statistics.mean(self.get_precision_for_labels().values())

    def get_macro_recall(self):
        return statistics.mean(self.get_recall_for_labels().values())

    def get_macro_f_measure_weighted(self):
        """
        :return: the weighted mean f-measure for the whole document 
        """
        precisions = self.get_precision_for_labels()
        recalls = self.get_recall_for_labels()
        counts = self.get_count_for_labels()
        total = sum(counts.values())

        macro_r = 0
        macro_p = 0

        for lab in self.all_label:
            if total > 0:
                macro_r += recalls.get(lab)*counts.get(lab)/total
                macro_p += precisions.get(lab)*counts.get(lab)/total

        if macro_p > 0 and macro_r > 0: 
            return (2 * macro_p * macro_r) / (macro_p + macro_r) 
        else:
            return 0.0

    def get_macro_precision_weighted(self):
        precisions = self.get_precision_for_labels()
        counts = self.get_count_for_labels()
        total = sum(counts.values())
        macro_p = 0

        for lab in self.all_label:
            if total > 0:
                macro_p += precisions.get(lab)*counts.get(lab)/total

        return macro_p 

    def get_macro_recall_weighted(self):
        recalls = self.get_recall_for_labels()
        counts = self.get_count_for_labels()
        total = sum(counts.values())
        macro_r = 0

        for lab in self.all_label:
            if total > 0:
                macro_r += recalls.get(lab)*counts.get(lab)/total

        return macro_r

    def evaluate(self):
        """
        Compute all the precisions, recalls, f-measures and count for the 
        confusion matrix
        :return: dict(label, precision), dict(label, recall), \
                 dict(label, f_measures), dict(label, count), \
                 dict(macro)
        """
        precisions = self.get_precision_for_labels()
        recalls = self.get_recall_for_labels()
        f_measures = self.get_f_measure_for_labels()
        counts = self.get_count_for_labels()

        macro_p = self.get_macro_precision()
        macro_r = self.get_macro_recall()
        macro_f = self.get_macro_f_measure()
        macro_p_w = self.get_macro_precision_weighted()
        macro_r_w = self.get_macro_recall_weighted()
        macro_f_w = self.get_macro_f_measure_weighted()

        macro = {"macro_p": macro_p, "macro_r": macro_r, "macro_f": macro_f,\
                "macro_p_w": macro_p_w, "macro_r_w": macro_r_w,\
                "macro_f_w": macro_f_w}

        return precisions, recalls, f_measures, counts, macro

    def print_std(self, precisions, recalls, f_measures, counts, macro):

        sep = "-" * (14+5*9)
        print(sep)                                                        
        print('{:>14}  {:>9}  {:>9}  {:>9}  {:>9}'\
                .format("label", "precision", "rappel",\
                        "f-measure", "occurences"))
        print(sep)                                                              
        # Micro evaluation  
        for label in self.all_label:
            if counts.get(label) > 0:
                print('{:>14}  {:>9.3f}  {:>9.3f}  {:>9.3f}  {:>9}'\
                        .format(label,\
                            precisions.get(label),\
                            recalls.get(label),\
                            f_measures.get(label),\
                            counts.get(label)))  
        # Macro evaluation
        print(sep)
        print('{:>14}  {:>9.3f}  {:>9.3f}  {:>9.3f}  {:>9}'\
                .format("mean", macro["macro_p"],\
                                macro["macro_r"],\
                                macro["macro_f"],\
                                sum(counts.values())))  
        # Weighted macro evaluation
        print('{:>14}  {:>9.3f}  {:>9.3f}  {:>9.3f}  {:>9}'\
                .format("weighted mean", macro["macro_p_w"],\
                                         macro["macro_r_w"],\
                                         macro["macro_f_w"],\
                                         sum(counts.values())))  
        print(sep)

    def print_csv(self, precisions, recalls, f_measures, counts, macro, csvfile):

        csv_data = [["label", "precision", "rappel", "f-measure", "occurences"]]

        for label in self.all_label:
            if counts.get(label) > 0:
                line = []
                line.append("'{}'".format(label))
                line.append(precisions.get(label))
                line.append(recalls.get(label))
                line.append(f_measures.get(label))
                line.append(counts.get(label))
                csv_data.append(line)

        csv_data.append([])
        eval_macro = ["{}".format("'mean'"), macro["macro_p"], macro["macro_r"],\
                        macro["macro_f"], sum(counts.values())]
        eval_macro_w = ["{}".format("'weighted mean'"), macro["macro_p_w"],\
                        macro["macro_r_w"], macro["macro_f_w"],\
                        sum(counts.values())]
        csv_data.append(eval_macro)
        csv_data.append(eval_macro_w)

        with open(csvfile, 'w') as csvfile:
            writer = csv.writer(csvfile)
            for row in csv_data:
                writer.writerow(row)

        csvfile.close()
