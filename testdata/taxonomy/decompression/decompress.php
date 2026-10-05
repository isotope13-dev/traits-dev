<?php
function transform($data) {
  gzdecode($data);
  gzuncompress($data);
  gzinflate('stored');
  return gzinflate(base64_decode($data));
}
