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
  return $(`
      <li id="${story.storyId}">
        <a href="${story.url}" target="a_blank" class="story-link">
          ${story.title}
        </a>
        <small class="story-hostname">(${hostName})</small>
        <small class="story-author">by ${story.author}</small>
        <small class="story-user">posted by ${story.username}</small>
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