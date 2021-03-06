"use strict";

// So we don't have to keep re-finding things on page, find DOM elements once:

const $body = $("body");

const $storiesLoadingMsg = $("#stories-loading-msg");
const $allStoriesList = $("#all-stories-list");
const $favoriteStoriesList = $("#favorite-stories-list")
const $favoriteStoriesSection = $("#favorite-stories")

const $loginForm = $("#login-form");
const $signupForm = $("#signup-form");
const $submitStoryForm = $("#submit-new-story-form")

const $navLogin = $("#nav-login");
const $navUserProfile = $("#nav-user-profile");
const $navLogOut = $("#nav-logout");
const $navSubmit = $("#nav-submit")
const $navFavorites = $("#nav-favorites")

/** To make it easier for individual components to show just themselves, this
 * is a useful function that hides pretty much everything on the page. After
 * calling this, individual components can re-show just what they want.
 */

function hidePageComponents() {
  const components = [
    $allStoriesList,
    $loginForm,
    $signupForm,
    $submitStoryForm,
    $favoriteStoriesSection
  ];
  components.forEach(c => c.hide());
}

/* Will hide components that are not to be seen on initial load -> this is for when a user is logged in
They should not be able to click on submit and favorites on the nav-bar
Submit Form and Fave Section is  hidden as well
*/
function hidePageComponentsOnInitialLoad(){
  const components = [
    $navSubmit,
    $submitStoryForm,
    $navFavorites,
    $favoriteStoriesSection
  ]
  components.forEach( c => c.hide())
}

/** Overall function to kick off the app. */
async function start() {
  console.debug("start");

  // "Remember logged-in user" and log in, if credentials in localStorage
  hidePageComponentsOnInitialLoad();
  await checkForRememberedUser();
  await getAndShowStoriesOnStart();

  // if we got a logged-in user
  if (currentUser) updateUIOnUserLogin();
}

// Once the DOM is entirely loaded, begin the app

console.warn("HEY STUDENT: This program sends many debug messages to" +
  " the console. If you don't see the message 'start' below this, you're not" +
  " seeing those helpful debug messages. In your browser console, click on" +
  " menu 'Default Levels' and add Verbose");
$(start);
