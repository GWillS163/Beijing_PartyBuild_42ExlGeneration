
# open the file path and read the file contents
def read_file_content(path):
    with open(path, 'r', encoding='utf-8') as file:
        content = file.readlines()
    return content


def retrieve_file(file, string=''):
    other_content = []
    inrule_content = []
    # print the line included specific string
    for line in file:
        if string in line:
            inrule_content.append(line)
        else:
            other_content.append(line)
    # print inrule_content by line
    for line in inrule_content:
        print(line, end='')
    return other_content



# input content to the file
def write_file(path, content):
    with open(path, 'a') as file:
        file.write(content)
        file.write('\n')


if __name__ == '__main__':
    remains = read_file_content('no_community.txt')
    inputs = ''
    while True:
        remains = retrieve_file(remains, inputs)
        print("current inputs:", inputs)
        inputs = input("Please input the string you want to search: ")

