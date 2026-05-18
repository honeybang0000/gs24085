class SchoolMember:
    def __init__(self):
        self.name = '경기과학고'
    def introduce(self):
        print("안녕하세요!")
class Teacher(SchoolMember):
    pass
class Student(SchoolMember):
    def __init__(self):
        self.ID = '2600000'
        # super().__init__()

    def introduce(self):
        # super().introduce()
        print("반갑습니다!")
t = Teacher()
print(t.name)
s = Student()
print(s.name)
s.introduce()