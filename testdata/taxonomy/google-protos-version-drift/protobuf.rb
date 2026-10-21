require 'google/protobuf'
pool = Google::Protobuf::DescriptorPool.generated_pool
pool.add_serialized_file(descriptor_data)
parsed = Google::Protobuf::FileDescriptorProto.decode(descriptor_data)
