$(document).ready(function() {
  // Get the current language from data attribute
  var lang = $("#checkInContainer").data('lang');

  // Define message objects for different languages
  var messages = {
    en: {
      symptomMessage: 'Based on your symptoms, you might be showing signs of ',
      recommendation: 'We recommend taking the following assessments for a more comprehensive evaluation.',
    },
    sw: {
      symptomMessage: 'Kulingana na dalili zako, unaweza kuwa unaonyesha dalili za ',
      recommendation: 'Tunapendekeza ufanye tathmini zifuatazo kwa tathmini kamili zaidi.',
    },
  };

  // Handle form submission
  $("#checkInForm").submit((e) => {
    e.preventDefault();

    // Show spinner and update button text
    $("#spinnerContainer").show();
    $("#buttonText").text(lang === "sw" ? "Inatathmini..." : "Processing...");

    // Send AJAX request
    $.ajax({
      url: '', // Replace with your actual endpoint URL
      type: 'POST',
      data: $("#checkInForm").serialize(),
      contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
      success: function(response) {
        if (response.error) {
          // Show error message and hide results
          $("#alert").removeClass("alert-success").addClass("alert-danger").text(response.error).show();
          $("#results").hide();
        } else {
          // Hide alert and handle response data
          $("#alert").hide();

          const predictedCondition = response.predicted_condition;
          const recommendedAssessments = response.recommended_assessments;

          // Build and display results message with translation
          let resultsMessage = `${messages[lang].symptomMessage}<strong>${predictedCondition}</strong>. ${messages[lang].recommendation}`;
          $("#resultsContent").html(resultsMessage);

          // Clear and populate recommended assessments list
          $("#resultsLink").empty();
          recommendedAssessments.forEach(assessment => {
            $("#resultsLink").append(`<a href='/assessment/${assessment}' class='link'>${assessment}</a><br>`);
          });

          // Show results and scroll to bottom
          $("#results").show();
          $('html, body').animate({
            scrollTop: $(document).height()
          }, 500);
        }

        setTimeout(function() {
          $("#spinnerContainer").hide();
          $("#buttonText").text(lang === "sw" ? "Tathmini" : "Check");
        }, 2500); // 2-second delay
      },
      error: function(error) {
        // Handle AJAX errors
        $("#alert").removeClass("alert-success").addClass("alert-danger").text("Something went wrong. Please try again later.").show();
        $("#spinnerContainer").hide();
        $("#buttonText").text(lang === "sw" ? "Kagua tena" : "Check In");
      }
    });
  });

  // Logic for handling checkbox changes
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
});



// Function to activate dark theme
function activateDarkTheme() {
  document.body.classList.add('dark-theme'); // Add the dark-theme class to the body
  localStorage.setItem('theme', 'dark'); // Update local storage
}

// Function to deactivate dark theme
function deactivateDarkTheme() {
  document.body.classList.remove('dark-theme'); // Remove the dark-theme class from the body
  localStorage.setItem('theme', 'light'); // Update local storage
}

// Initial theme check and setting
let themeState = localStorage.getItem('theme'); // Get the current theme state from local storage
if (themeState === 'dark') {
  activateDarkTheme();
} else {
  deactivateDarkTheme();
}

// Theme switch button click event
document.getElementById('themeSwitch').addEventListener('click', () => {
  themeState = localStorage.getItem('theme'); // Get the current theme state from local storage
  if (themeState === 'dark') {
    deactivateDarkTheme();
  } else {
    activateDarkTheme();
  }
});

// detect language change
$("#language").change(() => {
  switchLang($("#language").val());
});

function activateDarkTheme() {
  localStorage.setItem("theme", "dark");
  $("#themeIcon").removeClass("bi-moon-stars-fill").addClass("bi-brightness-high-fill");
  $("body").removeClass("theme-light");
}

function deactivateDarkTheme() {
  localStorage.setItem("theme", "light");
  $("#themeIcon").addClass("bi-moon-stars-fill").removeClass("bi-brightness-high-fill");
  $("body").addClass("theme-light");
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

// Function to validate age as the user types
document.getElementById("age").addEventListener("input", function () {
  var ageInput = this.value;
  var ageError = document.getElementById("age-error");
  
  if (ageInput < 13 || ageInput > 99) {
      ageError.style.display = "block";
      this.setCustomValidity("Invalid age");
  } else {
      ageError.style.display = "none";
      this.setCustomValidity("");
  }
});

// Toggle password visibility
function togglePasswordVisibility(inputId) {
  var passwordField = document.getElementById(inputId);
  var passwordType = passwordField.getAttribute('type');
  if (passwordType === 'password') {
    passwordField.setAttribute('type', 'text');
  } else {
    passwordField.setAttribute('type', 'password');
  }
}

var passwordField = document.getElementById("password");
var confirmPasswordField = document.getElementById("confirm_password");
var passwordLengthError = document.getElementById("password-length-error");
var passwordNumberError = document.getElementById("password-number-error");
var passwordUppercaseError = document.getElementById("password-uppercase-error");
var passwordLowercaseError = document.getElementById("password-lowercase-error");
var passwordConfirmError = document.getElementById("password-confirm-error");

passwordField.addEventListener("input", function () {
  var password = passwordField.value;

  // Check password length
  if (password.length < 6) {
      passwordLengthError.style.display = "block";
  } else {
      passwordLengthError.style.display = "none";
  }

  // Check if password contains at least one number
  if (!/\d/.test(password)) {
      passwordNumberError.style.display = "block";
  } else {
      passwordNumberError.style.display = "none";
  }

  // Check if password contains at least one uppercase letter
  if (!/[A-Z]/.test(password)) {
      passwordUppercaseError.style.display = "block";
  } else {
      passwordUppercaseError.style.display = "none";
  }

  // Check if password contains at least one lowercase letter
  if (!/[a-z]/.test(password)) {
      passwordLowercaseError.style.display = "block";
  } else {
      passwordLowercaseError.style.display = "none";
  }

  // Check if passwords match
  if (password !== confirmPasswordField.value) {
      passwordConfirmError.style.display = "block";
  } else {
      passwordConfirmError.style.display = "none";
  }
});

confirmPasswordField.addEventListener("input", function () {
  // Check if passwords match
  if (passwordField.value !== confirmPasswordField.value) {
      passwordConfirmError.style.display = "block";
  } else {
      passwordConfirmError.style.display = "none";
  }
});

// Logic for handling checkbox changes
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

// Function to switch the logo based on the theme
function switchLogo() {
  const lightLogo = document.getElementById('lightLogo');
  const darkLogo = document.getElementById('darkLogo');
  const themeState = localStorage.getItem('theme');
  
  if (themeState === 'dark') {
      lightLogo.style.display = 'none';
      darkLogo.style.display = 'block';
  } else {
      lightLogo.style.display = 'block';
      darkLogo.style.display = 'none';
  }
}

// Call switchLogo when the page loads
document.addEventListener('DOMContentLoaded', switchLogo);
