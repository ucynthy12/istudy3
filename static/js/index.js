$(window).scroll(function (){
  $('nav').toggleClass('scrolled',$(this).scrollTop() > 100);
});

// mine

$(document).ready(function () {
  // ***************************start signup  ******************************//

  $(".signUp").on("click", function () {
    $(this)
      .width("90%")
      .css({
        cursor: "default",
        background: 'url("https://i.postimg.cc/ncdKhBq9/signUpBg.jpg")',
        backgroundSize: "cover"
      });
    $(".signIn").width("10%").css("background", " rgba(238, 238, 238 , 0.2)");
    $(".signUpUser").fadeOut(0);
    $(".signInUser").fadeIn().css({ width: "50%" });
    $(".signUp form").fadeIn();
    $(".signIn form").fadeOut(0);
  });

  // ***************************end signup  ******************************//

  // ***************************start signin  ******************************//

  $(".signIn").on("click", function () {
    $(".signUpUser").fadeIn().css({ width: "50%" });
    $(".signInUser").fadeOut(0);
    $(this)
      .width("90%")
      .css({
        cursor: "default",
        background: 'url("https://i.postimg.cc/P5PWpJM3/signInBg.jpg")',
        backgroundSize: "cover"
      });
    $(".signUp").width("10%").css("background", " rgba(238, 238, 238 , 0.2)");
    $(".signIn form").fadeIn();
    $(".signUp form").fadeOut(0);
    // ***************************handel responsive ******************************//
    if (window.matchMedia("(max-width:768px)").matches) {
      $(this).css({ "background-position": "87% 0%" });
    }
  });

  // ***************************end signin  ******************************//

  // ***************************start changing width  ******************************//

  $(".signIn").hover(function () {
    $(".signUp").addClass("otherWidth");
  });
  $(".signIn").mouseleave(function () {
    $(".signUp").removeClass("otherWidth");
  });

  // ***************************end changing width  ******************************//

  // ***************************start form ******************************//

  // **************************** watch password ****************************//
  $(".eye").on("click", function () {
    if ($(this).hasClass("fa-eye")) {
      $(this).removeClass("fa-eye").addClass("fa-eye-slash");
      $(".password").attr("type", "text");
    } else {
      $(this).removeClass("fa-eye-slash").addClass("fa-eye");
      $(".password").attr("type", "password");
    }
  });
  // **************************** form validation ****************************//

  //email validation
  let emailValidation = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
  $("#signUpEmail").on("blur", function () {
    if ($(this).val().match(emailValidation)) {
      $(this).css("borderBottom", "2px solid #99043D");
      $(".errEmailSignUp").css("display", "none");
    } else {
      $(this).css("borderBottom", "2px solid #ea160b");
      $(".errEmailSignUp").css("display", "block");
    }
  });
  $("#signInEmail").on("blur", function () {
    if ($(this).val().match(emailValidation)) {
      $(this).css("borderBottom", "2px solid #99043D");
      $(".errEmailSignIn").css("display", "none");
    } else {
      $(this).css("borderBottom", "2px solid #ea160b");
      $(".errEmailSignIn").css("display", "block");
    }
  });
  //password validation
  let passwordValidation = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[a-z0-9A-z]/;
  $("#signUpPassword").on("blur", function () {
    if (
      $(this).val().match(passwordValidation) &&
      $(this).val().length >= 6 &&
      $(this).val().length <= 12
    ) {
      $(this).css("borderBottom", "2px solid #99043D");
      $(".errPasswordSignUp").css("display", "none");
    } else {
      $(this).css("borderBottom", "2px solid #ea160b");
      $(".errPasswordSignUp").css("display", "block");
    }
  });
  //phone validation
  $("#signUpPhone").on("blur", function () {
    if ($(this).val().length == 11) {
      $(this).css("borderBottom", "2px solid #99043D");
      $(".errPhoneSignUp").css("display", "none");
    } else {
      $(this).css("borderBottom", "2px solid #ea160b");
      $(".errPhoneSignUp").css("display", "block");
    }
  });
  // ***************************end form ******************************//
});
