
var float_numbers = document.getElementsByClassName("float_rounded");
for (i = 0; i < float_numbers.length; i++) {
    var currentValue = float_numbers[i].innerHTML;
    var newValue = currentValue.substring(0, currentValue.indexOf(".") + 3);
    float_numbers[i].innerHTML = newValue.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

var integer_numbers = document.getElementsByClassName("integer_comma");
for (i = 0; i < float_numbers.length; i++) {
    var currentValue = integer_numbers[i].innerHTML;
    integer_numbers[i].innerHTML = currentValue.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

