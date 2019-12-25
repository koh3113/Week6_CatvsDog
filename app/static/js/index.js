function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
    
        reader.onload = function (e) {
            $('#blah')
                .attr('src', e.target.result)
                .attr('style', 'text-align: center')
                .width(400)
                .height(250);
        };
    
        reader.readAsDataURL(input.files[0]);
    }
    }

function reset(){
    document.location.href = "/";
}