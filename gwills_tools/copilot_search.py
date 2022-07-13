
# define a function can find file in system by name and return the path
def find_file(file_name):
    import os
    for root, dirs, files in os.walk("."):
        if file_name in files:
            return os.path.join(root, file_name)
    return None


if __name__ == '__main__':
    print(find_file("testTxt.txt"))
