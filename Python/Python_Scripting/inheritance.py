# - Python inheritance provides code reusability, readability, and scalability.
# - Reduce code repetition. You can define all the methods and attributes in
#   the parent class that are accessible by the child classes.
# - By dividing the code into multiple classes, identifying bugs in 
# applications is easier.


class MainClass:
    def message_main(self):
        print('Welcome to Main Class')


class Child(MainClass):
    def message_child(self):
        print('Welcome to Child Class')
        print('This is inherited from Main')


class ChildDerived(Child):
    def message_derived(self):
        print('Welcome to Derived Class')
        print('This is inherited from Child')


if __name__ == '__main__':
    child_derived_obj = ChildDerived()
    child_derived_obj.message_main()
    child_derived_obj.message_child()
    child_derived_obj.message_derived()
    print(issubclass(ChildDerived, Child))              # True
    print(issubclass(ChildDerived, MainClass))          # True
    print(issubclass(Child, MainClass))                 # True
    print(issubclass(MainClass, ChildDerived))          # False
    print(isinstance(child_derived_obj, Child))         # True
    print(isinstance(child_derived_obj, MainClass))     # True
    print(isinstance(child_derived_obj, ChildDerived))  # True