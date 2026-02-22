import hashlib


def read_chunks(file_path, chunk_size):
    """Читает исходный файл фрагментами заданной длины, по умолчанию = 4096"""
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            yield chunk


def read_compress_file(file_path):
    """Читает запакованный файл"""
    with open(file_path, 'rb') as f:
        len_bytes = f.read(4)
        if not len_bytes:
            return None, None
        codes_table_len = int.from_bytes(len_bytes, 'big')
        codes_table_serialize = f.read(codes_table_len)
        compressed_data = f.read()
    return codes_table_serialize, compressed_data


def write_bytes(file_name: str, data: bytes):
    """Записывает массив байт в файл"""
    with open(file_name, 'wb') as f:
        f.write(data)


def write_chunks(file_name: str, chunks_list: list):
    """Записывает распакованный текст в файл фрагментами"""
    with open(file_name, 'wb') as f:
        for chunk in chunks_list:
            f.write(chunk)


def get_file_hash(file_path, chunk_size=4096):
    """Получить файл для сравнения по хэш"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        return f"Error: {e}"
