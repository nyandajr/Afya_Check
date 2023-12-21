$(document).ready(function() {
    // hide results and alert divs
    $("#results").hide();
    $("#alert").hide();

    var lang = $("#checkInContainer").data('lang'); // Get the current language

    // Messages for different languages
    var messages = {
        en: {
            symptomMessage: 'Based on your symptoms, you might be showing signs of ',
            recommendation: 'We recommend taking the following assessments for a more comprehensive evaluation.'
        },
        sw: {
            symptomMessage: 'Kulingana na dalili zako, unaweza kuwa unaonyesha dalili za ',
            recommendation: 'Tunapendekeza ufanye tathmini zifuatazo kwa tathmini kamili zaidi.'
        }
    };

    $("#checkInForm").submit((e) => {
        e.preventDefault();
        $("#checkButton").html(lang === "sw" ? "Inatathmini..." : "Checking...");

        $.ajax({
            url: '', // Update with your endpoint
            type: 'POST',
            data: $("#checkInForm").serialize(),
            contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
            success: function(response) {
                if (response.error) {
                    $("#alert").removeClass("alert-success").addClass("alert-danger").text(response.error).show();
                    $("#results").hide();
                } else {
                    $("#alert").hide();

                    const predictedCondition = response.predicted_condition;
                    const recommendedAssessments = response.recommended_assessments;

                    let resultsMessage = `${messages[lang].symptomMessage}<strong>${predictedCondition}</strong>. ${messages[lang].recommendation}`;
                    $("#resultsContent").html(resultsMessage); // Dynamically set the message
                    
                    $("#resultsLink").empty(); // Clear previous content
                    recommendedAssessments.forEach(assessment => {
                        $("#resultsLink").append(`<a href='/assessment/${assessment}' class='link'>${assessment}</a><br>`);
                    });

                    $("#results").show(); // Show the results div

                    // scroll to page bottom
                    $('html, body').animate({
                        scrollTop: $(document).height()
                    }, 500);
                }
            },
            error: function (error) {
                $("#alert").removeClass("alert-success").addClass("alert-danger").text("Something went wrong. Please try again later.").show();
            },
            complete: function() {
                $("#checkButton").html(lang === "sw" ? "Tathmini" : "Check In");
            }
        });  
    });
});

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


function darkThemeOn(){
    localStorage.setItem("theme", "dark")
    $("#themeIcon").removeClass("bi-moon-stars-fill")
    $("#themeIcon").addClass("bi-brightness-high-fill")
    $("body").removeClass("theme-light")
}

function darkThemeOff(){
    localStorage.setItem("theme", "light")
    $("#themeIcon").addClass("bi-moon-stars-fill")
    $("#themeIcon").removeClass("bi-brightness-high-fill")
    $("body").addClass("theme-light")
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
