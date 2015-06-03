__author__ = 'Matias'

from textanalysis.texts import CaseReportLibrary

class_labels = {}

relabel = 0

with open('classification/data/class.txt', 'r') as infile:
    for line in infile.read().split("\n")[:-1]:
        pmcid, cls = line.split(" ")
        class_labels[pmcid] = cls

if relabel:
    count = 0
    for cs in CaseReportLibrary():
        count += 1
        pmcid = cs.get_pmcid()
        if pmcid in class_labels.keys() and class_labels[pmcid] == "1":
            print count, class_labels[pmcid], cs.title
            choice = raw_input("Diagnosis(1), Test(2), Treatment(3), Drug reactions(4), Surgery adverse effect(5), Imaging(6) --- None(0) --- Quit(q)")
            class_labels[pmcid] = choice
            print ">>>"
            print ""
        if count > len(class_labels):
            break
    print len([class_labels[pmcid] for pmcid in class_labels if class_labels[pmcid] == '1'])

else:
    count = 0
    for cs in CaseReportLibrary():
        count += 1
        pmcid = cs.get_pmcid()
        if pmcid in class_labels.keys():
            continue

        print count, cs.title
        choice = raw_input("Diagnosis(1), Test(2), Treatment(3), Drug reactions(4), Surgery adverse effect(5), Imaging(6) --- None(0) --- Quit(q)")
        print ""

        if choice in ["1", "2", "3", "0"]:
            class_labels[pmcid] = choice
        elif choice == "q":
            break

with open('classification/data/class.txt', 'w') as outfile:
    for pmcid in class_labels.keys():
        outfile.write("%s %s\n" % (pmcid, class_labels[pmcid]))