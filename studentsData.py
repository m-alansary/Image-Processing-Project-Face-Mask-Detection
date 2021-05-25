students = {}
attendance = {}
currentId = 0

def add_student(name):
    global currentId
    students[currentId] = name
    currentId += 1


def get_student(id):
    return students[id]

def get_students():
    return students

def attend_studnet(id, ts):
    attendance[ts] = id
