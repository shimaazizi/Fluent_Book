# with dict
class MyDict(dict):
    def __setitem__(self, key, value):
        print(f"setting {key} to {value}")
        self[key] = value


my_dict = MyDict()
#my_dict[1] = 'a'


# with UserDict 
import collections 
class MyUserDict(collections.UserDict):
    def __setitem__(self, key, value):
        print(f"setting {key} to {value}")
        self.data[key] = value

my_user_dict = MyUserDict()
my_user_dict[1] = 0
print(my_user_dict)