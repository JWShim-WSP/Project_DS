const float_numbers = document.getElementsByClassName("float_rounded");
for (i = 0; i < float_numbers.length; i++) {
    let currentValue = float_numbers[i].innerHTML;
    let newValue = currentValue.substring(0, currentValue.indexOf(".") + 3);
    float_numbers[i].innerHTML = newValue.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

const integer_numbers = document.getElementsByClassName("integer_comma");
for (i = 0; i < integer_numbers.length; i++) {
    let currentValue = integer_numbers[i].innerHTML;
    console.log(currentValue)
    integer_numbers[i].innerHTML = currentValue.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

const date_strings = document.getElementsByClassName("date_string");
for (i = 0; i < date_strings.length; i++) {
    let currentDate = date_strings[i].innerHTML;
    date_strings[i].innerHTML = currentDate.split(',')[0] + ',' + currentDate.split(',')[1];
}
