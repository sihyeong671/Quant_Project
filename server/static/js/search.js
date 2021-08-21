function search_companyname(){
    if(!$('#company_name').val()){
        alert("회사명을 입력해 주세요.");
        return;
    }
    
    $.ajax({
        type: "POST",
        url: "http://localhost:8000/test/search/",
        data: {
            'company_name' : $('#company_name').val(),
            // 'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function(response){
            $('#search-result').append(result)
        },
    });
}