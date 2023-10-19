$(document).ready(function(){
    // hide results and alert divs
    $("#results").hide()
    $("#alert").hide()

    $("#checkInForm").submit((e)=>{
        e.preventDefault()
        $("#checkButton").html("Checking...")

        $.ajax({
            url: '',
            type: 'POST',
            data: $("#checkInForm").serialize(),
            contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
            success: function (response) {
                if (response.error){
                    $("#alert").removeClass("alert-success")
                    $("#alert").addClass("alert-danger")
                    $("#alert").text(response.error)
                    $("#alert").show()
                    $("#results").hide()
                }
                else {
                    $("#alert").hide()
                    $("#results").show()
                    $("#resultsLink").empty()
                    response.map((item, i)=> {
                        $("#resultsLink").append(`<a href='/assessment/${item}' class='link'>${item}</a>`)
                        if (i != response.length - 1){
                            $("#resultsLink").append(", &nbsp;")
                        }
                    })
                }
            },
            error: function (error){
                $("#alert").removeClass("alert-success")
                $("#alert").addClass("alert-danger")
                $("#alert").text("Something went wrong. Please try again later.")
                $("#alert").show()
            },
            complete: function(){
                $("#checkButton").html("Check In")
            }
        });
        
    })
})
