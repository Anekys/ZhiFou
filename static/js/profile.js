function BindCheckBoxSelect() {
    $('input[type=checkbox][name=select]').change(function () {
        if ($(this).is(':checked')) {
            $('input[name=password]').attr("type","text")
        } else {
            $('input[name=password]').attr("type","password")
        }
    });
}

$(function () {
    BindCheckBoxSelect();
})