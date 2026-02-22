from collections import deque

from Node import Node


def build_frequency_table(chunks_list):
    """Считает частоту символов во всех накопленных блоках"""
    freq_dict = {}
    for chunk in chunks_list:
        for char in chunk:
            freq_dict[char] = freq_dict.get(char, 0) + 1

    freqs = []
    for symbol, k in freq_dict.items():
        node = Node()
        node.symbol = symbol
        node.k = k
        freqs.append(node)
    return freqs


def quick_sort(sort_list: list[Node]):
    """Реализация быстрой сортировки по возрастанию, применяется для упорядочивания списка узлов с частотами символов"""
    if len(sort_list) <= 1:
        return sort_list
    pivot_node = sort_list[len(sort_list) // 2]
    left, middle, right = [], [], []
    for node in sort_list:
        if node.k < pivot_node.k:
            left.append(node)
        elif node.k == pivot_node.k:
            middle.append(node)
        elif node.k > pivot_node.k:
            right.append(node)
    return quick_sort(left) + middle + quick_sort(right)


def create_tree(freqs: list[Node]):
    """Постройка дерева Хаффмана (алгоритм основан на двух очередях)"""
    queue_freqs1 = deque(freqs)
    queue_freqs2 = deque()
    while len(queue_freqs1) + len(queue_freqs2) > 1:
        left_node = get_min_freq(queue_freqs1, queue_freqs2)
        right_node = get_min_freq(queue_freqs1, queue_freqs2)
        new_node = Node()
        new_node.k = left_node.k + right_node.k
        new_node.left = left_node
        new_node.right = right_node
        queue_freqs2.append(new_node)
    return queue_freqs2.popleft()


def get_min_freq(queue_freqs1: deque[Node], queue_freqs2: deque[Node]):
    """Получить узел с минимальной частотой из двух очередей"""
    if not queue_freqs1:
        return queue_freqs2.popleft()
    elif not queue_freqs2:
        return queue_freqs1.popleft()

    if queue_freqs1[0].k <= queue_freqs2[0].k:
        return queue_freqs1.popleft()
    else:
        return queue_freqs2.popleft()


def build_codes_table_by_tree(node: Node, current_code="", codes=None):
    """Построить таблицу символ - код по дереву Хаффмана"""
    if codes is None: codes = {}
    if node is None: return codes
    if node.is_leave():
        codes[node.symbol] = current_code
        return codes
    build_codes_table_by_tree(node.left, current_code + "0", codes)
    build_codes_table_by_tree(node.right, current_code + "1", codes)
    return codes


def create_compressed_bytes(chunks_list: bytearray, codes_table: dict) -> bytearray:
    """Упаковывает байты в битовую последовательность на основе таблицы Хаффмана"""
    compressed_body = bytearray([0])
    current_byte = 0
    bits_filled = 0
    for chunk in chunks_list:
        for byte_val in chunk:
            code = codes_table[byte_val]
            for bit in code:
                current_byte = (current_byte << 1) | (1 if bit == '1' else 0)
                bits_filled += 1
                if bits_filled == 8:
                    compressed_body.append(current_byte)
                    current_byte = 0
                    bits_filled = 0
    if bits_filled > 0:
        padding = 8 - bits_filled
        current_byte <<= padding
        compressed_body.append(current_byte)
        compressed_body[0] = padding
    else:
        compressed_body[0] = 0
    return compressed_body


def serialize_codes(codes_table: dict) -> bytes:
    """Сериализация таблицы частот: Ключи — числа (байты), значения — строки '0101'"""
    result = bytearray()
    for byte_val, code in codes_table.items():
        result.append(byte_val)
        code_bytes = code.encode('ascii')
        result.append(len(code_bytes))
        result.extend(code_bytes)
    return bytes(result)
