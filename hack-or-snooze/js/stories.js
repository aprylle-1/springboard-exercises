"use strict";

// This is the global list of the stories, an instance of StoryList
let storyList;

/** Get and show stories when site first loads. */

async function getAndShowStoriesOnStart() {
  storyList = await StoryList.getStories();
  $storiesLoadingMsg.remove();

  putStoriesOnPage();
}

/**
 * A render method to render HTML for an individual Story instance
 * - story: an instance of Story
 *
 * Returns the markup for the story.
 */

function generateStoryMarkup(story) {
  // console.debug("generateStoryMarkup", story);
  const hostName = story.getHostName();
  //changing HTML depending if a user is logged in or not
  if(currentUser){
    //checking if currentUser has favorites -> if yes, button will show remove from Favorites instead of Add to Favorites
    if(currentUser.favorites.some(faveStory => {
      return faveStory.storyId === story.storyId
      })){
      return $(`
    <li id="${story.storyId}">
      <a href="${story.url}" target="a_blank" class="story-link">
        ${story.title}
      </a>
      <small class="story-hostname">(${hostName})</small>
      <small class="story-author">by ${story.author}</small>
      <small class="story-user">posted by ${story.username}</small>
      <div class='all-stories-actions'>
      <small class="story-user"><button class="all-stories-btn">Remove from Favorites</button></small>
      <small class="story-user"><button class="all-stories-btn">Remove Story</button></small>
      </div>
    </li>
      `);
      }
      return $(`
        <li id="${story.storyId}">
        <a href="${story.url}" target="a_blank" class="story-link">
         ${story.title}
         </a>
        <small class="story-hostname">(${hostName})</small>
        <small class="story-author">by ${story.author}</small>
        <small class="story-user">posted by ${story.username}</small>
        <div class='all-stories-actions'>
        <small class="story-user"><button class="all-stories-btn">Add to Favorites</button></small>
        <small class="story-user"><button class="all-stories-btn">Remove Story</button></small>
        </div>
      </li>
    `);
  }
  //no buttons if no user is logged in
  return $(`
  <li id="${story.storyId}">
    <a href="${story.url}" target="a_blank" class="story-link">
      ${story.title}
    </a>
    <small class="story-hostname">(${hostName})</small>
    <small class="story-author">by ${story.author}</small>
    <small class="story-user">posted by ${story.username}</small>
    <div class='all-stories-actions'>
    </div>
  </li>
`);
}

function generateFavoriteStoryMarkup(story) {
  // console.debug("generateStoryMarkup", story);

  const hostName = story.getHostName();
  return $(`
      <li id="${story.storyId}">
        <a href="${story.url}" target="a_blank" class="story-link">
          ${story.title}
        </a>
        <small class="story-hostname">(${hostName})</small>
        <small class="story-author">by ${story.author}</small>
        <small class="story-user">posted by ${story.username}</small>
        <small><button>Remove Favorite</button></small>
      </li>
    `);
}

/** Gets list of stories from server, generates their HTML, and puts on page. */

function putStoriesOnPage() {
  console.debug("putStoriesOnPage");

  $allStoriesList.empty();

  // loop through all of our stories and generate HTML for them
  for (let story of storyList.stories) {
    const $story = generateStoryMarkup(story);
    $allStoriesList.append($story);
  }

  $allStoriesList.show();
}

/* this creates a story object based on user unit */
function getStoryDetails() {
  console.log('submit a new story')
  const $storyAuthor = $('#submit-author').val()
  const $storyTitle = $('#submit-title').val()
  const $storyUrl = $('#submit-url').val()
  const story = {
    author : $storyAuthor,
    title : $storyTitle,
    url : $storyUrl
  }
  return story

}

/* this calls the async post function to post a new user story, if successful, storyList will be updated using getAndShowStoriesOnStart, page will then be updated to show the new generated story*/

async function submitStoryDetails(story){
  await StoryList.addStory(currentUser, story);
  await getAndShowStoriesOnStart();
  putStoriesOnPage();
  $submitStoryForm.hide();
  console.log('successfully added a new story')
}

const $btnSubmitNewStory = $("#btn-submit-new-story")

$btnSubmitNewStory.on('click', function (e) {
  e.preventDefault()
  const story = getStoryDetails();
  submitStoryDetails(story);
})

//gets story Id based on clicked element
function getStoryId (element){
  const storyId = element.id
  return storyId;
}

//gets currentUsers favorites and creates HTML for it
function putFavoriteStoriesOnPage () {
  $favoriteStoriesList.empty();
  for (let story of currentUser.favorites) {
    const $story = generateFavoriteStoryMarkup(story)
    $favoriteStoriesList.append($story);
  }
}

/* on clicl of button, function getStoryId gets that Id of favorited story and then calls saveFavorite, checkForRememberedUser is called to refrest currentUser value */
$allStoriesList.on('click', async function(event){
  if (event.target.tagName === 'BUTTON' && event.target.textContent === 'Add to Favorites'){
    console.dir(event.target);
    console.log('Add to Favorites')
    const storyId = getStoryId(event.target.parentElement.parentElement.parentElement);
    if (currentUser.favorites.some(story => {
      return story.storyId === storyId
    })) {
      alert('Story Already Added')
    }
    else{
      await User.saveFavorite(currentUser.loginToken, currentUser.username, storyId);
      alert('Added to Favorites')
      event.target.textContent = 'Remove from Favorites';
    }
  }
  else if (event.target.tagName === 'BUTTON' && event.target.textContent === 'Remove Story'){
    try{
      console.log('Remove Story');
      const element = event.target.parentElement.parentElement.parentElement
      const storyId = getStoryId(element);
      await StoryList.removeStory(currentUser.loginToken, storyId);
      element.remove();
    }
    catch(error){
      //added error handling when user that is login is trying to remove an article that's not theirs
      console.log(error)
      alert('You are not allowed to remove this story')
    }
  }
  else if (event.target.tagName === 'BUTTON' && event.target.textContent === 'Remove from Favorites'){
    try{
      console.log('this works');
      // console.log('Remove Story');
      const element = event.target.parentElement.parentElement.parentElement
      const storyId = getStoryId(element);
      await User.deleteFavorite(currentUser.loginToken, currentUser.username, storyId);
      alert('Removed from Favorites!')
      event.target.textContent = 'Add to Favorites';
    }
    catch(error){
      //added error handling when user that is login is trying to remove an article that's not theirs
      console.log(error)
    }
  }
})

$favoriteStoriesSection.on('click', async function(event){
  if(event.target.tagName === 'BUTTON'){
    console.log(currentUser.favorites.length)
    const storyId = getStoryId(event.target.parentElement.parentElement);
    await User.deleteFavorite(currentUser.loginToken, currentUser.username, storyId);
    alert('Removed from Favorites!')
    event.target.parentElement.parentElement.remove();
    console.log(currentUser.favorites.length);
    }
})