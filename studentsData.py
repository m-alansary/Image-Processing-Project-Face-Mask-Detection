students = {}
maskedStudents = {}
attendance = {}
currentId = 0
currentMaskedId = 0

def add_student(name):
    global currentId
    students[currentId] = name
    currentId += 1

def add_masked_student(name):
    global currentMaskedId
    maskedStudents[currentMaskedId] = name
    currentMaskedId += 1


def get_student(id):
    return students[id]

def get_masked_student(id):
    return maskedStudents[id]

def get_students():
    return students

def attend_studnet(id, ts):
    attendance[ts] = id
