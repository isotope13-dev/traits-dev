var formatter = new ActiveXObject("System.Runtime.Serialization.Formatters.Binary.BinaryFormatter");
var stream = new ActiveXObject("System.IO.MemoryStream");
formatter.Serialize(stream, {value: 1});
