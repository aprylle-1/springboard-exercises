async function getGif(){
    //Not sure if there's a way to get this using GET but documentation said I had to sign up
    const apiKey = 'IedB885ZFyidlBbeHr5z513CKiErhtFx'
    const res = await axios.get('https://api.giphy.com/v1/gifs/search', {params :{
        "q" : 'cheeseburger',
        "api_key" : apiKey
    }})
    return res.data.data[0].url;
}

function createGif(res){
    const gifNumber = getRandomNumber(res.data.data);
    console.log(res.data.data[gifNumber].images.original.url);
    const url = res.data.data[gifNumber].images.original.url
    // console.log(url);
    const gifContainer = document.createElement('div');
    gifContainer.classList.add('gif')
    const gif = document.createElement('img');
    gif.src = url;
    gifContainer.append(gif);
    return gifContainer
}

function getRandomNumber(arr){
    const arrLength = arr.length;
    const randomNumber = Math.round(Math.random() * arrLength);
    return randomNumber;
}
function getSearchValue(){
    const search = document.getElementById('gif-name')
    console.log(search.value)
    return search.value;
}

async function postGif(search){
    try{
        const apiKey = 'IedB885ZFyidlBbeHr5z513CKiErhtFx'
        const res = await axios.get('https://api.giphy.com/v1/gifs/search', {params :{
            "q" : search,
            "api_key" : apiKey
        }})
        const gifs = document.querySelector('#gifs')
        const gif = createGif(res);
        console.log(res);
        // console.log(gif);
        gifs.append(gif);
    }catch{
        alert(`Sorry! Couldn't find a GIF like that!`)
        const search = document.getElementById('gif-name')
        search.value = "";
    }
}

const btnSearch = document.getElementById('search-gif');
btnSearch.addEventListener('click', function(event){
    event.preventDefault();
    const search = getSearchValue();
    postGif(search);
})

const btnRemove = document.getElementById('remove-images');
btnRemove.addEventListener('click', function(event){
    event.preventDefault()
    const gifs = document.querySelector('#gifs');
    gifs.innerHTML = "";
    const search = document.getElementById('gif-name')
    search.value = "";
})