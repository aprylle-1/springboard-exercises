"use strict";

const $showsList = $("#shows-list");
const $episodesArea = $("#episodes-area");
const $searchForm = $("#search-form");
const $episodesList = $("#episodes-list")


/** Given a search term, search for tv shows that match that query.
 *
 *  Returns (promise) array of show objects: [show, show, ...].
 *    Each show object should contain exactly: {id, name, summary, image}
 *    (if no image URL given by API, put in a default image URL)
 */

async function getShowsByTerm(term) {
  // const $searchQuery = $('#search-query')
  const res = await axios.get('http://api.tvmaze.com/search/shows', { params:{
      "q" : term
  }})
  const shows = res.data;
  return shows
}


/** Given list of shows, create markup for each and to DOM */

function populateShows(shows) {
  $showsList.empty();
  let $show = ""
  for (let show of shows) {
    if (show.show.image != null){
      $show = $(
        `<div data-show-id="${show.show.id}" class="Show col-md-12 col-lg-6 mb-4">
         <div class="media">
           <img 
              src="${show.show.image.original}" 
              alt="${show.show.name}" 
              class="w-25 mr-3">
           <div class="media-body">
             <h5 class="text-primary">${show.show.name}</h5>
             <div><small>${show.show.summary}</small></div>
             <button class="btn btn-primary btn-sm Show-getEpisodes">
               Episodes
             </button>
           </div>
         </div>  
       </div>
      `);
    }
    else{
      $show = $(
        `<div data-show-id="${show.show.id}" class="Show col-md-12 col-lg-6 mb-4">
         <div class="media">
           <img
              src="https://static.tvmaze.com/images/no-img/no-img-portrait-text.png"
              alt="${show.show.name}" 
              class="w-25 mr-3">
           <div class="media-body">
             <h5 class="text-primary">${show.show.name}</h5>
             <div><small>${show.show.summary}</small></div>
             <button class="btn btn-outline-primary btn-sm Show-getEpisodes">
               Episodes
             </button>
           </div>
         </div>  
       </div>
      `);
    }
    $showsList.append($show);  }
}


/** Handle search form submission: get shows from API and display.
 *    Hide episodes area (that only gets shown if they ask for episodes)
 */

async function searchForShowAndDisplay() {
  const term = $("#search-query").val();
  console.log(term)
  const shows = await getShowsByTerm(term);
  console.log(shows);

  $episodesArea.hide();
  populateShows(shows);
}

$searchForm.on("submit", async function (evt) {
  evt.preventDefault();
  await searchForShowAndDisplay();
})


/** Given a show ID, get from API and return (promise) array of episodes:
 *      { id, name, season, number }
 */
const showList = document.getElementById('shows-list');
showList.addEventListener('click', function(event){
  if (event.target.nodeName == 'BUTTON'){
    $episodesList.html("");
    const episode = event.target.parentElement.parentElement.parentElement;
    const episodeId = episode.dataset.showId;
    getEpisodesOfShow(episodeId);
  }
})
async function getEpisodesOfShow(id) {
  const res = await axios.get(`http://api.tvmaze.com/shows/${id}/episodes`)
  const episodes = (res.data)
  populateEpisodes(episodes)
  $episodesArea.show();
}

/** Write a clear docstring for this function... */

function populateEpisodes(episodes) {
  for (let episode of episodes){
    let $episode = $(`
    <li>${episode.name} - Season: ${episode.season} Episode: ${episode.number}</li>
    `)
    $episodesList.append($episode);
  }
}
