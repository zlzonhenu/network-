import ipaddress

class Node:

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class radix_tree:

    def __init__(self, address_list):
        self.root = Node(None)
        for i, node in enumerate(address_list):
            self.insert(node, i + 1)
    # insert node each address
    def insert(self, address, index):
        # /0 to root
        if address == '':
            self.root = Node(index)
            return

        tmp = self.root

        for bit in address:

            # go right when bit == 1
            if bit == '1':
                # append node if there is no node
                if tmp.right is None:
                    tmp.right = Node(None)

                tmp = tmp.right

            # go left when bit == 0
            else:
                if tmp.left is None:
                    tmp.left = Node(None)

                tmp = tmp.left

        tmp.key = index

    # searching node
    def search(self, address):
        # return index of root when /0
        if address == '':
            return self.root.key

        # candidate of index
        candidate = self.root.key
        tmp = self.root

        for bit in address:
            # go right when bit == 1
            if bit == '1':
                # end if there is no node
                if tmp.right is None:
                    break

                tmp = tmp.right

            # go left when bit == 0
            else:
                if tmp.left is None:
                    break

                tmp = tmp.left

            # last key of node will be index
            if tmp.key is not None:
                candidate = tmp.key

        return candidate


def read_txt(path):

    # read to list
    with open(path) as f:
        l = f.readlines()

    # delete thing not to need
    for i in range(len(l)):
        if l[i].count(' ') >= 1:
            l[i] = l[i][l[i].find(' ') + 1:]
            l[i] = l[i][:l[i].find(' ')]
        else:
            l[i] = l[i].replace('\n', '')

    l = [s for s in l if s != '']

    return l

def align_address(address):
    '''
    1.4/22   -> 0000000100000100000000
    1.0.5/24 -> 000000010000000000000101
    '''

    # if data has no / or number after / is nothing, data would be processed
    if address.count('/') == 0 or address.find('/') == len(address) - 1:
        address_part = address.replace('/', '')
        mask_part = '32'

    else:
        # divide address and mask by /
        mid = address.find('/')
        address_part = address[:mid]
        mask_part = address[mid + 1:]

    # 例：1.0.4 -> 1.0.4.0
    dot_num = address_part.count('.')
    for j in range(3 - dot_num):
        address_part = address_part + '.0'

    # change 32 bit to decimal number
    address_num = int(ipaddress.ip_address(address_part))
    # change to binary number
    address_str = bin(address_num)
    address_str = address_str.replace('0b', '')
    # insert 0 to be 32 bit
    address_str = '0' * (32 - len(address_str)) + address_str
    # subnet
    address_str = address_str[:int(mask_part)]

    return address_str

# pre-processing to read  address from txt file
def pre_process(path):

    data_list = read_txt(path)
    address_list = []

    for data in data_list:
        address_list.append(align_address(data))

    return address_list, data_list


if __name__ == '__main__':
    # read addresses from txt file
    address_list, _ = pre_process('route.txt')
    # insert radix_tree to all addresses
    RT = radix_tree(address_list)

    # read address for search
    # route_search.txt:
    #  41.74.1.1
    #  66.31.10.3
    #  133.5.1.1
    #  209.143.75.1
    #  221.121.128.1
    search_list, data_list = pre_process('route_search.txt')

    # searching
    for (query, data) in zip(search_list, data_list):
        result_index = RT.search(query)
        print('{}: {}'.format(data, result_index))