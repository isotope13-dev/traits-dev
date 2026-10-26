function decode() {
    var character = String.fromCharCode;
    var numbers = [80, 79, 78, 77];
    var result = '';
    for (var i = 0; i < numbers.length; i++) result += character(numbers[i] ^ 5);
    return result;
}
