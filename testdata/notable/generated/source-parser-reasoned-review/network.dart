import 'package:http/http.dart' as http;
import 'dart:convert';
Future run(http.Client client) async { var r = await client.get(Uri.parse('https://api.example/map')); return jsonDecode(r.body); }
var value = base64Url.decode(text);
var query = Uri.encodeQueryComponent(value);
