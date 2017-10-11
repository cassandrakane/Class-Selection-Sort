# Class Selection Sort Program

import csv

class Student:
    # constants for class size range
    MAX_CLASS_SIZE = 16
    MIN_CLASS_SIZE = 10

    # constants for class score calculations
    FIRST_IMPORTANCE = 40
    SECOND_IMPORTANCE = 30
    GENDER_IMPORTANCE = 20
    
    LARGE_CLASS_IMPORTANCE = -100
    SMALL_CLASS_IMPORTANCE = 40
    NOT_SELECETD_CLASS_IMPORTANCE = -100
    NO_PREFERENCE_IMPORTANCE = 0
    
    def __init__(self, name, gender, first, second, third):
        self.name = name
        self.gender = gender
        self.first = first
        self.second = second
        self.third = third

    def is_male(self):
        return self.gender == 'Male'

    def is_female(self):
        return self.gender == 'Female'

    def is_other_gender(self):
        return (not self.is_male() and not self.is_female())

    def calculate_class_score(self, klass, klass_name):
        score = 0
        
        # prioritize class size
        if len(klass) > self.MAX_CLASS_SIZE: # deprioritize large class
            return self.LARGE_CLASS_IMPORTANCE
        if len(klass) < self.MIN_CLASS_SIZE: # prioritize small class
            score += self.SMALL_CLASS_IMPORTANCE
        score += 2 * (self.MAX_CLASS_SIZE - len(klass))**2 # prioritize smaller classes within range

        # prioritize first/second/third choice
        if klass_name == self.first: # prioritize first choice
            score += self.FIRST_IMPORTANCE
        elif klass_name == self.second: # prioritize second choice
            score += self.SECOND_IMPORTANCE
        elif self.first == "No Preference" or self.second == "No Preference" or self.third == "No Preference": # no prioritization for no preference
            score += self.NO_PREFERENCE_IMPORTANCE
        elif klass_name != self.third: # deprioritize non choice
            return self.NOT_SELECETD_CLASS_IMPORTANCE
        
        # prioritize gender balance
        males = len([1 for student in klass if student.is_male()]) # number of males
        females = len([1 for student in klass if student.is_female()]) # number of females
        if males > females:
            if self.is_male():
                score -= self.GENDER_IMPORTANCE # deprioritize males in male-heavy class
            else:
                score += self.GENDER_IMPORTANCE # prioritize females in male-heavy class
        elif females > males:
            if self.is_male():
                score += self.GENDER_IMPORTANCE # prioritize males in female-heavy class
            else:
                score -= self.GENDER_IMPORTANCE # deprioritize females in female-heavy class
    
        return score

# get data from csv
firstLine = True
students = []
with open('ClassSelectionData.csv', newline='') as f:
    reader = csv.reader(f)
    for student_row in reader:
        if firstLine: # skip first line (labels)
            firstLine = False
            continue
        students.append(Student(student_row[1], student_row[2], student_row[3], student_row[4], student_row[5]))

# count classes
klass_names = []
for student in students:
    klass_names.extend([student.first, student.second, student.third])
for klass_name in klass_names:
    if klass_name == "No Preference":
        klass_names.remove(klass_name)

klass_names_final = list(set(klass_names))

# first sort
klasses = []
for class_name in klass_names_final:
    klasses.append([])
for student in students:
    scores = []
    for i, klass in enumerate(klasses):
        scores.append(student.calculate_class_score(klass, klass_names_final[i])) # get scores for each student in each class

    klasses[scores.index(max(scores))].append(student) # choose class with highest score for student in class

# resort (rearrange students and reevaluate scores)
for i in range(100):
    for klass_out in klasses:
        temp_class = klass_out[:]
        for t,student in enumerate(temp_class):
            klass_out.pop(0)
            scores = []
            for i,klass in enumerate(klasses):
                scores.append(student.calculate_class_score(klass, klass_names_final[i]))            
            klasses[scores.index(max(scores))].append(student)

# print classes in output file
outfile = open("classes_output.txt", "w") # clear previous text
outfile.close()
outfile = open("classes_output.txt", "a")
outfile.write("SORTED CLASSES (M/F/O)")
for i, klass in enumerate(klasses):
    outfile.write("\n\n\n{} ({}/{}/{})\n".format(klass_names_final[i], len([1 for student in klass if student.is_male()]), len([1 for student in klass if student.is_female()]), len([1 for student in klass if student.is_other_gender()])))
    for student in klasses[i]:
        student_choice = 0
        if student.first == klass_names_final[i] or student.first == "No Preference":
            student_choice = 1
        elif student.second == klass_names_final[i] or student.second == "No Preference":
            student_choice = 2
        elif student.third == klass_names_final[i] or student.third == "No Preference":
            student_choice = 3
        outfile.write("\n" + student.name + " (" + student.gender + ") - " + str(student_choice))
outfile.write("\n\n")
outfile.close()
