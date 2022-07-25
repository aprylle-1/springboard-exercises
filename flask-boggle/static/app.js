const $btnSubmitWord = $("#btn-submit-word")
const $submittedWord = $("#submitted-word")
const $messageBoard = $("#message")
const $score = $("#score")
const $highScore = $('#high-score')
const $timesPlayed = $('#times-played')
$btnSubmitWord.on('click', async function(event) {
    event.preventDefault()
    $messageBoard.html("")
    if (getSubmittedWord()){
        const submittedWord = getSubmittedWord()
        response  = await checkValidWord(submittedWord)
        $submittedWord.val("")
        result = response['data']['result']
        const message = resultMsg(result)
        const score = getScore(result, submittedWord)
        displayScore(score)
        $messageBoard.html(`${message}`)
    }
})

async function checkValidWord (word){
    console.log(word)
    const res = await axios.get("http://127.0.0.1:5000/check-word", {params : {'word' : word}})
    return res
}

async function updateStats() {
    let score = parseInt($score.html())
    const res = await axios.post("http://127.0.0.1:5000/update-stats", {params: {'score': score}})
    return res.data
}

async function getStats () {
    const res = await axios.get("http://127.0.0.1:5000/get-stats")
    return res.data
}

function updateStatsHtml(stats) {
    const highScore = stats['high_score']
    const timesPlayed  = stats['times_played']
    $highScore.html(highScore)
    $timesPlayed.html(timesPlayed) 
}

function getSubmittedWord(){
    const submittedWord = $submittedWord.val()
    return submittedWord
}

function getScore(result, word){
    let score = parseInt($score.html())
    if (result === 'ok'){
        score += word.length
    }
    return score
}

function displayScore (score){
    $score.html(score)
}

function resultMsg(result){
    if (result === "ok"){
        return 'Valid Word!'
    }
    else if (result === "not-on-board"){
        return 'Valid Word! Not on board'
    }
    else{
        return "Not a Word!"
    }
}

function endGame(){
    let score = parseInt($score.html())
    alert(`Game Over! Your score is ${score}`)
}