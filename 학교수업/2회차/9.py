class Parent:
    def __init__(self):
        print("부모 초기화")

class Child(Parent):
    def __init__(self):
        print("자식 초기화")

c = Child()