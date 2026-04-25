from io import BytesIO

from avro.io import BinaryDecoder, BinaryEncoder, DatumReader, DatumWriter



def serialize_avro(data, schema):
    """Serialize data using Avro."""
    writer = DatumWriter(schema)
    bytes_writer = BytesIO()
    encoder = BinaryEncoder(bytes_writer)
    writer.write(data, encoder)
    raw_bytes = bytes_writer.getvalue()
    return raw_bytes


def deserialize_avro(data, schema):
    """Deserialize data using Avro."""
    bytes_reader = BytesIO(data)
    decoder = BinaryDecoder(bytes_reader)
    reader = DatumReader(schema)
    return reader.read(decoder)