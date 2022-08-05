
# open the file path and recursion print content
def print_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = {}
        for line in f:
            line = line.strip()
            if line == '\n' or not line:
                continue
            lines = line.split(' ')
            if lines[1]:
                data[lines[0]] = lines[1]
            for i in lines:
                print(i, end='\t')
            print()
    print(data)

if __name__ == "__main__":
    print_file_content('raw/integration.txt')