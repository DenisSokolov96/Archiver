import File
from Compress import *
from Decompress import *


def compress_data(chunks_list, options):
    """Основная логика выполнения алгоритма сжатия Хаффмана"""
    if not chunks_list: return False
    freqs = quick_sort(list(build_frequency_table(chunks_list)))
    root_node = create_tree(freqs)
    codes_table = build_codes_table_by_tree(root_node)
    codes_table_serialize = serialize_codes(codes_table)
    codes_table_serialize_len = len(codes_table_serialize).to_bytes(4, 'big')
    compressed_bytes = create_compressed_bytes(chunks_list, codes_table)
    File.write_bytes(options["file_path"] + options['postfix_file'],
                     codes_table_serialize_len + codes_table_serialize + compressed_bytes)
    return True


def decompress_data(options):
    """Основная логика выполнения алгоритма распаковки файла"""
    path_to_file = options['file_path']
    codes_table_serialize, compressed_data = File.read_compress_file(path_to_file)
    codes_table = deserialize_codes(codes_table_serialize)
    chunks_list = decompressed_chunks_list(compressed_data, codes_table, options['chunk_size'])
    new_path_to_file = path_to_file.removesuffix(options['postfix_file'])
    old_postfix = '.' + new_path_to_file.split('.')[-1]
    new_path_to_file = new_path_to_file[:-len(old_postfix)] + options['suffix_file'] + new_path_to_file[-len(old_postfix):]
    File.write_chunks(new_path_to_file, chunks_list)
    return True
