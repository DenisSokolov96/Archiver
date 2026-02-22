def deserialize_codes(serialized_data: bytes) -> dict:
    """
    Десериализация таблицы частот из списка байт в словарь
    Десериализация таблицы: [байт_значение][длина_кода][строка_кода]
    Возвращает словарь: {код_строка: байт_значение}
    """
    if not serialized_data: return {}
    codes_table = {}
    pos = 0
    size = len(serialized_data)
    while pos < size:
        byte_val = serialized_data[pos]
        code_len = serialized_data[pos + 1]
        pos += 2
        code = serialized_data[pos: pos + code_len].decode('ascii')
        pos += code_len
        codes_table[code] = byte_val
    return codes_table


def decompressed_chunks_list(compressed_data: bytes, codes_table: dict, chunk_size=4096) -> list:
    """Получить исходный список фрагментов текста исходного файла"""
    if not compressed_data:
        return []
    padding = compressed_data[0]
    body = compressed_data[1:]
    chunks_list = []
    current_chunk = bytearray()
    current_code = ""
    total_bytes = len(body)
    for i in range(total_bytes):
        byte = body[i]
        num_bits = 8
        if i == total_bytes - 1:
            num_bits = 8 - padding
            if num_bits == 0 and padding == 0: num_bits = 8
        for bit_idx in range(7, 7 - num_bits, -1):
            bit = "1" if (byte & (1 << bit_idx)) else "0"
            current_code += bit
            if current_code in codes_table:
                current_chunk.append(codes_table[current_code])
                current_code = ""
                if len(current_chunk) >= chunk_size:
                    chunks_list.append(current_chunk)
                    current_chunk = bytearray()
    if current_chunk:
        chunks_list.append(current_chunk)
    return chunks_list
