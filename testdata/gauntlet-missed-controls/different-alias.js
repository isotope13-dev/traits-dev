function transform() {
    var character = String.fromCharCode;
    var numbers = [80, 79, 78, 77];
    var result = '';
    for (var i = 0; i < numbers.length; i++) result += stringify(numbers[i] ^ 5);
    return character(result.length);
}
