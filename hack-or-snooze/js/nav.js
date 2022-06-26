"use strict";

/******************************************************************************
 * Handling navbar clicks and updating navbar
 */

/** Show main list of all stories when click site name */

function navAllStories(evt) {
  console.debug("navAllStories", evt);
  hidePageComponents();
  putStoriesOnPage();
}

$body.on("click", "#nav-all", navAllStories);

/** Show login/signup on click on "login" */

function navLoginClick(evt) {
  console.debug("navLoginClick", evt);
  hidePageComponents();
  $loginForm.show();
  $signupForm.show();
}

$navLogin.on("click", navLoginClick);

/** When a user first logins in, update the navbar to reflect that. */

function updateNavOnLogin() {
  console.debug("updateNavOnLogin");
  $(".main-nav-links").show();
  $navLogin.hide();
  $navLogOut.show();
  $navUserProfile.text(`${currentUser.username}`).show();
  $navSubmit.show();
  $navFavorites.show();
}

/* When user clicks on Submit the Submit form must Show */
function navSubmitClick(){;
  $allStoriesList.hide();
  $submitStoryForm.show()
  $favoriteStoriesSection.hide();
}

$navSubmit.on('click', navSubmitClick)

function navFavoritesClick(){
  $allStoriesList.hide(),
  $favoriteStoriesSection.show();
  $submitStoryForm.hide();
}

$navFavorites.on('click', function(e){
  e.preventDefault();
  putFavoriteStoriesOnPage();
  navFavoritesClick();
});

