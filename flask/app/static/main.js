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
                    // Handle error
                    $("#alert").removeClass("alert-success");
                    $("#alert").addClass("alert-danger");
                    $("#alert").text(response.error);
                    $("#alert").show();
                    $("#results").hide();
                } else {
                    // Check the current language and set the message accordingly
                    var language = $("#language").val(); // Assuming you have a language selector with ID 'language'
                    var messagePrefix = language === "sw" ? "Huenda ukawa nadalili za " : "You might be showing signs of ";
            
                    // Display the predicted condition
                    if (response.predicted_condition) {
                        $("#predictedCondition").html(`<strong>${messagePrefix}${response.predicted_condition}.</strong>`);
                    }
            
                    // Display the recommended assessments
                    if (response.recommended_assessments && response.recommended_assessments.length > 0) {
                        $("#results").show();
                        $("#resultsLink").empty();
                        response.recommended_assessments.forEach((item, i) => {
                            $("#resultsLink").append(`<a href='/assessment/${item}' class='link'>${item}</a>`);
                            if (i != response.recommended_assessments.length - 1){
                                $("#resultsLink").append(", &nbsp;");
                            }
                        });
                    } else {
                        $("#results").hide();
                    }
            
                    // Scroll to page bottom
                    $('html, body').animate({
                        scrollTop: $(document).height()
                    }, 500);
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

    // deal with theme switching
    themeState = localStorage.getItem("theme", "dark")
    if (themeState == "dark"){
        darkThemeOn()
    }
    else{
        darkThemeOff()
    }

    $("#themeSwitch").click(()=>{
        themeState = localStorage.getItem("theme", "dark")
        if (themeState == "dark"){
            darkThemeOff()
        }
        else{
            darkThemeOn()
        }
    })

    // detect language change
    $("#language").change(()=>{
        switchLang($("#language").val());
    })
})

function darkThemeOn(){
    localStorage.setItem("theme", "dark");
    $("#themeIcon").removeClass("bi-brightness-high-fill").addClass("bi-moon-stars-fill");
    $("body").removeClass("theme-light").addClass("theme-dark"); // Add 'theme-dark' class
}

function darkThemeOff(){
    localStorage.setItem("theme", "light");
    $("#themeIcon").removeClass("bi-moon-stars-fill").addClass("bi-brightness-high-fill");
    $("body").removeClass("theme-dark").addClass("theme-light"); // Remove 'theme-dark' class
}


function switchLang(lang){
    $.get(`/lang/${lang}`, (data)=>{
        location.reload()
    })
}

document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    const categories = new Set();

    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            const category = this.getAttribute('data-category');

            if (this.checked) {
                categories.add(category);
            } else {
                categories.delete(category);
            }

            checkboxes.forEach(function(otherCheckbox) {
                if (!categories.has(otherCheckbox.getAttribute('data-category'))) {
                    otherCheckbox.disabled = categories.size > 0;
                } else {
                    otherCheckbox.disabled = false;
                }
            });
        });
    });
});
